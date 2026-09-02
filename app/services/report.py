import json
from datetime import date

from sqlmodel import Session, select

from app.models.post import CrawlPost
from app.models.report import AnalysisReport
from app.schemas.report import ReportRequest
from app.services.ai import LLMClient


def _load_posts(session: Session, platform: str, limit: int = 50) -> list[CrawlPost]:
    return list(
        session.exec(
            select(CrawlPost)
            .where(CrawlPost.platform == platform)
            .order_by(CrawlPost.collected_at.desc())
            .limit(limit)
        )
    )


def _build_report_prompt(
    posts: list[CrawlPost], request: ReportRequest
) -> str:
    samples = "\n".join(
        f"- {post.title}: {post.content[:120]}" for post in posts[:20]
    )
    return f"""
请基于下面的社媒内容，生成一份{request.style}分析报告。
平台：{request.platform}
内容样本：
{samples or "暂无数据"}

输出 JSON，包含 title、summary、highlights、suggestions 四个字段。
""".strip()


def generate_report(
    session: Session, request: ReportRequest
) -> AnalysisReport:
    posts = _load_posts(session, request.platform)
    llm = LLMClient()
    data = llm.complete_json(
        [
            {
                "role": "system",
                "content": "你是一名社媒数据分析师，擅长从内容中提炼趋势和建议。",
            },
            {"role": "user", "content": _build_report_prompt(posts, request)},
        ]
    )

    report_date = request.report_date or date.today().isoformat()
    report = AnalysisReport(
        title=data.get("title", f"{request.platform} {request.style} 报告"),
        platform=request.platform,
        report_date=report_date,
        content=json.dumps(data, ensure_ascii=False, indent=2),
    )
    session.add(report)
    session.commit()
    session.refresh(report)
    return report
