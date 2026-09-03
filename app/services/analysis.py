from datetime import datetime
from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph
from sqlmodel import Session, select

from app.core.config import get_settings
from app.models.analysis_job import AnalysisJob
from app.models.post import CrawlPost
from app.services.ai import LLMClient
from app.services.prompts import load_prompt


class AnalysisState(TypedDict, total=False):
    posts: list[dict[str, Any]]
    summaries: list[dict[str, Any]]
    sentiments: list[dict[str, Any]]
    topics: dict[str, Any]
    insights: dict[str, Any]
    error: str | None


def _post_dict(post: CrawlPost) -> dict[str, Any]:
    return {
        "id": post.id,
        "platform": post.platform,
        "title": post.title,
        "content": post.content,
        "metrics": post.metrics,
        "comments": [comment.content for comment in post.comments],
    }


def _summarize_posts(state: AnalysisState) -> AnalysisState:
    llm = LLMClient()
    system = load_prompt("post_summary.md")
    summaries: list[dict[str, Any]] = []
    for post in state["posts"]:
        user = (
            f"平台：{post.get('platform')}\n"
            f"标题：{post.get('title')}\n"
            f"正文：{post.get('content')}\n"
            f"指标：{post.get('metrics')}\n"
        )
        result = llm.complete_json(
            [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ]
        )
        result["post_id"] = post.get("id")
        result["title"] = post.get("title")
        summaries.append(result)
    return {"summaries": summaries}


def _analyze_comments(state: AnalysisState) -> AnalysisState:
    llm = LLMClient()
    system = load_prompt("sentiment_analysis.md")
    sentiments: list[dict[str, Any]] = []
    for post in state["posts"]:
        for index, comment in enumerate(post.get("comments", [])):
            result = llm.complete_json(
                [
                    {"role": "system", "content": system},
                    {"role": "user", "content": comment},
                ]
            )
            result["post_id"] = post.get("id")
            result["comment_index"] = index
            sentiments.append(result)
    return {"sentiments": sentiments}


def _extract_topics(state: AnalysisState) -> AnalysisState:
    llm = LLMClient()
    system = load_prompt("topic_extraction.md")
    samples = "\n".join(
        f"- {item.get('title')}: {item.get('summary', '')}" for item in state.get("summaries", [])
    )
    user = f"帖子摘要样本：\n{samples or '暂无数据'}"
    topics = llm.complete_json(
        [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]
    )
    return {"topics": topics}


def _build_insights(state: AnalysisState) -> AnalysisState:
    llm = LLMClient()
    system = load_prompt("weekly_report.md")
    user = (
        "分析结果：\n"
        f"摘要：{state.get('summaries', [])}\n"
        f"情感：{state.get('sentiments', [])}\n"
        f"主题：{state.get('topics', {})}\n"
    )
    insights = llm.complete_json(
        [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]
    )
    return {"insights": insights}


def _build_graph():
    graph = StateGraph(AnalysisState)
    graph.add_node("summarize", _summarize_posts)
    graph.add_node("sentiment", _analyze_comments)
    graph.add_node("topics", _extract_topics)
    graph.add_node("insights", _build_insights)
    graph.add_edge(START, "summarize")
    graph.add_edge("summarize", "sentiment")
    graph.add_edge("sentiment", "topics")
    graph.add_edge("topics", "insights")
    graph.add_edge("insights", END)
    return graph.compile()


def create_analysis_job(
    session: Session,
    note_ids: list[int],
) -> AnalysisJob:
    settings = get_settings()
    job = AnalysisJob(
        status="pending",
        note_ids=note_ids,
        model=settings.llm_model,
    )
    session.add(job)
    session.commit()
    session.refresh(job)
    return job


def run_analysis_job(job_id: int) -> None:
    from app.core.database import engine

    with Session(engine) as session:
        job = session.get(AnalysisJob, job_id)
        if job is None:
            return

        job.status = "running"
        session.add(job)
        session.commit()

        posts = session.exec(
            select(CrawlPost).where(CrawlPost.id.in_(job.note_ids))
        ).all()

        if not posts:
            job.status = "failed"
            job.error = "No matching posts found"
            job.completed_at = datetime.utcnow()
            session.add(job)
            session.commit()
            return

        try:
            settings = get_settings()
            state_posts = [_post_dict(post) for post in posts[: settings.analysis_max_items]]
            graph = _build_graph()
            result = graph.invoke({"posts": state_posts, "error": None})
            job.result = {
                "summaries": result.get("summaries", []),
                "sentiments": result.get("sentiments", []),
                "topics": result.get("topics", {}),
                "insights": result.get("insights", {}),
            }
            job.status = "completed"
            job.error = None
        except Exception as exc:  # noqa: BLE001 - task boundary
            job.status = "failed"
            job.error = str(exc)
        finally:
            job.completed_at = datetime.utcnow()
            session.add(job)
            session.commit()
