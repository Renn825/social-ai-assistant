from datetime import datetime

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlmodel import Session, select

from app.core.database import get_session
from app.models.post import CrawlPost
from app.models.task import CrawlTask, TaskStatus
from app.schemas.post import CollectRequest, CrawlPostRead
from app.schemas.task import CrawlTaskRead
from app.services.crawler import collect_posts
from app.services.pipeline import store_posts

router = APIRouter(prefix="/posts", tags=["posts"])


def _run_collection(task_id: int) -> None:
    from app.core.database import engine

    with Session(engine) as session:
        task = session.get(CrawlTask, task_id)
        if task is None:
            return

        task.status = TaskStatus.running
        task.started_at = datetime.utcnow()
        session.add(task)
        session.commit()

        request = CollectRequest(
            platform=task.platform,
            keyword=task.keyword,
            limit=task.limit,
        )
        try:
            posts = collect_posts(request)
            inserted, skipped = store_posts(session, posts)
            task.total = len(posts)
            task.succeeded = inserted
            task.failed = skipped
            task.status = TaskStatus.succeeded
        except Exception as exc:  # noqa: BLE001 - task boundary
            task.error = str(exc)
            task.status = TaskStatus.failed
        finally:
            task.finished_at = datetime.utcnow()
            session.add(task)
            session.commit()


@router.get("", response_model=list[CrawlPostRead])
def list_posts(
    platform: str | None = None,
    limit: int = 20,
    session: Session = Depends(get_session),
) -> list[CrawlPost]:
    statement = select(CrawlPost).order_by(CrawlPost.collected_at.desc()).limit(limit)
    if platform:
        statement = statement.where(CrawlPost.platform == platform)
    return list(session.exec(statement).all())


@router.get("/{post_id}", response_model=CrawlPostRead)
def get_post(post_id: int, session: Session = Depends(get_session)) -> CrawlPost:
    post = session.get(CrawlPost, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="post not found")
    return post


@router.post("/collect", response_model=CrawlTaskRead)
def collect(
    payload: CollectRequest,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
) -> CrawlTask:
    task = CrawlTask(
        platform=payload.platform,
        keyword=payload.keyword,
        limit=payload.limit,
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    background_tasks.add_task(_run_collection, task.id)
    return task
