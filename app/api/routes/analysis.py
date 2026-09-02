from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlmodel import Session

from app.core.database import get_session
from app.schemas.report import ReportRequest
from app.services.ai import LLMClient
from app.services.report import _build_report_prompt, _load_posts

router = APIRouter(prefix="/analysis", tags=["analysis"])


class CopyRequest(BaseModel):
    topic: str = Field(default="AI 效率工具")
    style: str = Field(default="小红书")


@router.post("/summarize")
def summarize(
    request: ReportRequest,
    session: Session = Depends(get_session),
) -> dict:
    posts = _load_posts(session, request.platform)
    llm = LLMClient()
    return llm.complete_json(
        [
            {
                "role": "system",
                "content": "你是内容分析助手，请对社媒内容进行总结、情感分析和关键词提取。",
            },
            {"role": "user", "content": _build_report_prompt(posts, request)},
        ]
    )


@router.post("/copy")
def generate_copy(
    payload: CopyRequest,
) -> dict:
    llm = LLMClient()
    topic = payload.get("topic", "AI 效率工具")
    style = payload.get("style", "小红书")
    return llm.complete_json(
        [
            {
                "role": "system",
                "content": "你是社媒内容创作助手，请生成标题、正文要点和标签。",
            },
            {
                "role": "user",
                "content": f"主题：{topic}\n平台风格：{style}\n请输出 JSON。",
            },
        ]
    )
