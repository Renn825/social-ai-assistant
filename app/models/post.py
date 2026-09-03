from datetime import datetime
from typing import Any

from sqlalchemy import JSON, Column
from sqlmodel import Field, Relationship, SQLModel


class CrawlPost(SQLModel, table=True):
    __tablename__ = "crawl_posts"

    id: int | None = Field(default=None, primary_key=True)
    platform: str = Field(index=True)
    post_id: str = Field(index=True)
    title: str
    content: str = Field(default="")
    author: str = Field(default="")
    url: str = Field(default="")
    tags: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    metrics: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    published_at: datetime | None = None
    collected_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    content_hash: str = Field(default="", index=True)

    comments: list["PostComment"] = Relationship(back_populates="post")
