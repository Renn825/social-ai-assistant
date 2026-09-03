from datetime import datetime

from sqlmodel import Session, select

from app.core.config import get_settings
from app.models.analysis_job import AnalysisJob
from app.models.post import CrawlPost
from app.services.ai import LLMClient


ANALYSIS_SYSTEM_PROMPT = """你是社媒内容分析助手。请分析用户提供的笔记和评论，并只输出 JSON 对象。
JSON 字段必须包含：
- summary: 内容摘要
- sentiment: positive、neutral、negative 之一
- keywords: 关键词数组
- topics: 主题标签数组
- content_suggestions: 内容选题建议数组
- copy_suggestions: 可复用文案建议数组
"""


def _build_user_prompt(post: CrawlPost) -> str:
    comments = "\n".join(
        f"- {comment.content}" for comment in post.comments
    )
    return f"""平台：{post.platform}
标题：{post.title}
正文：{post.content}
点赞数：{post.metrics.get('likes', 0)}
收藏数：{post.metrics.get('favorites', 0)}

评论：
{comments}
"""


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
            llm = LLMClient()
            items = []
            for post in posts:
                data = llm.complete_json(
                    [
                        {"role": "system", "content": ANALYSIS_SYSTEM_PROMPT},
                        {"role": "user", "content": _build_user_prompt(post)},
                    ]
                )
                data["note_id"] = post.id
                data["title"] = post.title
                data["platform"] = post.platform
                items.append(data)

            job.result = {"items": items}
            job.status = "completed"
            job.error = None
        except Exception as exc:  # noqa: BLE001 - task boundary
            job.status = "failed"
            job.error = str(exc)
        finally:
            job.completed_at = datetime.utcnow()
            session.add(job)
            session.commit()
