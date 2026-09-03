from datetime import datetime

from pydantic import BaseModel


class PostCommentRead(BaseModel):
    id: int
    content: str
    published_at: datetime | None = None
    sentiment: str | None = None

    model_config = {"from_attributes": True}
