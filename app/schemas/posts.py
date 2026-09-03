from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PostRead(BaseModel):
    id: int
    platform: str
    source_post_id: str
    title: str
    content: str
    author: str | None
    published_at: datetime | None
    like_count: int
    comment_count: int
    collect_count: int

    model_config = ConfigDict(from_attributes=True)


class PostPage(BaseModel):
    items: list[PostRead]
    total: int
    page: int
    page_size: int
