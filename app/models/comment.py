from __future__ import annotations

from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel


class PostComment(SQLModel, table=True):
    __tablename__ = "post_comments"

    id: int | None = Field(default=None, primary_key=True)
    post_id: int | None = Field(
        default=None,
        foreign_key="crawl_posts.id",
        index=True,
    )
    content: str
    published_at: datetime | None = None
    sentiment: str | None = None

    post: CrawlPost = Relationship(back_populates="comments")
