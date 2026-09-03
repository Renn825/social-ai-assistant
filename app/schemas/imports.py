from pydantic import BaseModel, Field


class ImportRequest(BaseModel):
    posts_file: str | None = Field(default=None, description="CSV file name under data/samples")
    comments_file: str | None = Field(default=None, description="CSV file name under data/samples")


class ImportResult(BaseModel):
    imported_posts: int
    skipped_posts: int
    imported_comments: int
    skipped_comments: int
