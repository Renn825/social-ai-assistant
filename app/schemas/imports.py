from pydantic import BaseModel, Field


class ImportRequest(BaseModel):
    posts_file: str = Field(default="xiaohongshu_posts.csv")
    comments_file: str = Field(default="xiaohongshu_comments.csv")


class ImportResult(BaseModel):
    imported_posts: int
    skipped_posts: int
    imported_comments: int
    skipped_comments: int
