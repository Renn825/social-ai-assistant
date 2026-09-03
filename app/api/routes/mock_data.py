from fastapi import APIRouter, Depends
from sqlalchemy import delete
from sqlmodel import Session, select

from app.core.database import get_session
from app.models.comment import PostComment
from app.models.post import CrawlPost
from app.schemas.post import CollectRequest
from app.services.crawler import collect_posts
from app.services.pipeline import store_posts

router = APIRouter(tags=["mock-data"])


@router.post("/mock-data/load")
def load_mock_data(session: Session = Depends(get_session)) -> dict[str, int]:
    session.exec(delete(PostComment))
    session.exec(delete(CrawlPost))
    session.commit()

    requests = [
        CollectRequest(platform="xiaohongshu", keyword="AI 工具", limit=3),
        CollectRequest(platform="douyin", keyword="效率工具", limit=2),
    ]
    notes_created = 0
    for request in requests:
        posts = collect_posts(request)
        inserted, _ = store_posts(session, posts)
        notes_created += inserted

    comments_created = len(session.exec(select(PostComment)).all())
    return {
        "notes_created": notes_created,
        "comments_created": comments_created,
    }
