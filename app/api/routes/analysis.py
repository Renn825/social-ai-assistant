from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlmodel import Session

from app.core.database import get_session
from app.models.analysis_job import AnalysisJob
from app.schemas.analysis_job import AnalysisJobCreate, AnalysisJobRead
from app.schemas.report import ReportRequest
from app.services.ai import LLMClient
from app.services.analysis import create_analysis_job, run_analysis_job
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
    topic = payload.topic
    style = payload.style
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


@router.post("/jobs", response_model=AnalysisJobRead)
def create_job(
    payload: AnalysisJobCreate,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
) -> AnalysisJob:
    job = create_analysis_job(session, payload.note_ids)
    background_tasks.add_task(run_analysis_job, job.id)
    return job


@router.get("/jobs/{job_id}", response_model=AnalysisJobRead)
def get_job(job_id: int, session: Session = Depends(get_session)) -> AnalysisJob:
    job = session.get(AnalysisJob, job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="analysis job not found")
    return job
