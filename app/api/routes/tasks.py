from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.core.database import get_session
from app.models.task import CrawlTask
from app.schemas.task import CrawlTaskRead

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[CrawlTaskRead])
def list_tasks(
    limit: int = 20,
    session: Session = Depends(get_session),
) -> list[CrawlTask]:
    return list(
        session.exec(
            select(CrawlTask).order_by(CrawlTask.created_at.desc()).limit(limit)
        ).all()
    )


@router.get("/{task_id}", response_model=CrawlTaskRead)
def get_task(task_id: int, session: Session = Depends(get_session)) -> CrawlTask:
    task = session.get(CrawlTask, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="task not found")
    return task
