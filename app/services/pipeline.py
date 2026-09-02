from collections.abc import Iterable

from sqlmodel import Session, select

from app.models.post import CrawlPost
from app.services.crawler import CrawledPost, to_dict


def deduplicate_posts(posts: Iterable[CrawledPost]) -> list[CrawledPost]:
    seen: set[str] = set()
    result: list[CrawledPost] = []
    for post in posts:
        payload = to_dict(post)
        key = payload["content_hash"]
        if key in seen:
            continue
        seen.add(key)
        result.append(post)
    return result


def store_posts(
    session: Session, posts: Iterable[CrawledPost]
) -> tuple[int, int]:
    cleaned = deduplicate_posts(posts)
    inserted = 0
    skipped = 0

    for post in cleaned:
        payload = to_dict(post)
        existing = session.exec(
            select(CrawlPost).where(CrawlPost.content_hash == payload["content_hash"])
        ).first()
        if existing:
            skipped += 1
            continue

        session.add(CrawlPost(**payload))
        inserted += 1

    session.commit()
    return inserted, skipped

