import csv
from datetime import datetime
from pathlib import Path
from typing import Any

from sqlmodel import Session, select

from app.core.config import get_settings
from app.models.comment import PostComment
from app.models.post import CrawlPost
from app.services.crawler import CrawledPost, to_dict
from app.services.pipeline import deduplicate_posts


def _to_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def _to_datetime(value: Any) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None


def _split_tags(value: Any) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in str(value).split(";") if item.strip()]


def _load_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _post_from_row(row: dict[str, str]) -> CrawledPost:
    metrics = {
        "likes": _to_int(row.get("likes")),
        "favorites": _to_int(row.get("favorites")),
        "shares": _to_int(row.get("shares")),
    }
    return CrawledPost(
        platform=(row.get("platform") or "xiaohongshu").strip().lower(),
        post_id=(row.get("post_id") or "").strip(),
        title=(row.get("title") or "").strip(),
        content=(row.get("content") or "").strip(),
        author=(row.get("author") or "").strip(),
        url=(row.get("url") or "").strip(),
        tags=_split_tags(row.get("tags")),
        metrics=metrics,
        comments=[],
    )


def import_local_files(
    session: Session,
    posts_file: str,
    comments_file: str,
) -> tuple[int, int, int, int]:
    settings = get_settings()
    sample_dir = Path(settings.sample_data_dir)

    post_rows = _load_csv(sample_dir / posts_file)
    comment_rows = _load_csv(sample_dir / comments_file)

    comments_by_post_id: dict[str, list[dict[str, Any]]] = {}
    for row in comment_rows:
        post_id = (row.get("post_id") or "").strip()
        if not post_id:
            continue
        comments_by_post_id.setdefault(post_id, []).append(
            {
                "content": (row.get("content") or "").strip(),
                "sentiment": (row.get("sentiment") or None),
                "published_at": _to_datetime(row.get("published_at")),
            }
        )

    posts: list[CrawledPost] = []
    for row in post_rows:
        post = _post_from_row(row)
        post.comments = comments_by_post_id.get(post.post_id, [])
        posts.append(post)

    cleaned = deduplicate_posts(posts)
    inserted_posts = 0
    skipped_posts = 0
    imported_comments = 0
    skipped_comments = 0

    for post in cleaned:
        payload = to_dict(post)
        comments = payload.pop("comments", [])
        existing = session.exec(
            select(CrawlPost).where(CrawlPost.content_hash == payload["content_hash"])
        ).first()
        if existing:
            skipped_posts += 1
            continue

        post_model = CrawlPost(**payload)
        session.add(post_model)
        session.flush()
        inserted_posts += 1

        for comment in comments:
            session.add(
                PostComment(
                    post_id=post_model.id,
                    content=comment.get("content", ""),
                    sentiment=comment.get("sentiment"),
                    published_at=comment.get("published_at"),
                )
            )
            imported_comments += 1

    session.commit()
    return inserted_posts, skipped_posts, imported_comments, skipped_comments
