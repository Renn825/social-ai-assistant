import json
from datetime import date, datetime
from typing import Any

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


def _render_markdown(
    data: dict[str, Any],
    platform: str,
    generated_at: datetime,
) -> str:
    highlights = "\n".join(
        f"- {item}" for item in data.get("highlights", [])
    )
    suggestions = "\n".join(
        f"- {item}" for item in data.get("suggestions", [])
    )
    return f"""# {data.get('title', platform + ' 分析报告')}

生成时间：{generated_at.isoformat()}

## 摘要

{data.get('summary', '暂无摘要')}

## 亮点

{highlights or '- 暂无'}

## 建议

{suggestions or '- 暂无'}
"""


def _render_html(
    data: dict[str, Any],
    platform: str,
    generated_at: datetime,
) -> str:
    highlights = "".join(
        f"<li>{item}</li>" for item in data.get("highlights", [])
    )
    suggestions = "".join(
        f"<li>{item}</li>" for item in data.get("suggestions", [])
    )
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title>{data.get('title', platform + ' 分析报告')}</title>
</head>
<body>
  <h1>{data.get('title', platform + ' 分析报告')}</h1>
  <p>生成时间：{generated_at.isoformat()}</p>
  <h2>摘要</h2>
  <p>{data.get('summary', '暂无摘要')}</p>
  <h2>亮点</h2>
  <ul>{highlights or '<li>暂无</li>'}</ul>
  <h2>建议</h2>
  <ul>{suggestions or '<li>暂无</li>'}</ul>
</body>
</html>
"""


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
    generated_at = datetime.utcnow()
    if request.format == "html":
        content = _render_html(data, request.platform, generated_at)
    else:
        content = _render_markdown(data, request.platform, generated_at)

    report = AnalysisReport(
        title=data.get("title", f"{request.platform} {request.style} 报告"),
        platform=request.platform,
        report_date=report_date,
        format=request.format,
        content=content,
    )
    session.add(report)
    session.commit()
    session.refresh(report)
    return report
