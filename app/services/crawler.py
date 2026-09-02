from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib
import subprocess
from pathlib import Path
from typing import Any

from app.core.config import get_settings
from app.schemas.post import CollectRequest


@dataclass
class CrawledPost:
    platform: str
    post_id: str
    title: str
    content: str
    author: str
    url: str
    tags: list[str]
    metrics: dict[str, Any]


def _content_hash(platform: str, title: str, content: str) -> str:
    raw = f"{platform}:{title}:{content}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _mock_posts(request: CollectRequest) -> list[CrawledPost]:
    platform = request.platform
    keyword = request.keyword
    return [
        CrawledPost(
            platform=platform,
            post_id=f"mock-{platform}-{index}",
            title=f"{keyword}实践案例 {index}",
            content=f"这是一条关于 {keyword} 的模拟内容，用于演示数据清洗、分析与生成流程。",
            author=f"作者{index}",
            url=f"https://example.com/{platform}/{index}",
            tags=[keyword, "AI", "效率工具"],
            metrics={"likes": 100 + index, "comments": 10 + index, "shares": 5 + index},
        )
        for index in range(1, request.limit + 1)
    ]


def _run_media_crawler(request: CollectRequest) -> list[CrawledPost]:
    settings = get_settings()
    crawler_dir = Path(settings.media_crawler_dir)
    if not crawler_dir.exists():
        raise RuntimeError(f"MediaCrawler directory not found: {crawler_dir}")

    # MediaCrawler's CLI differs between versions. This adapter intentionally
    # keeps the external call isolated so you can replace it with the exact
    # command supported by your local clone.
    command = [
        "python",
        "main.py",
        "--platform",
        request.platform,
        "--keyword",
        request.keyword,
        "--count",
        str(request.limit),
    ]
    result = subprocess.run(
        command,
        cwd=crawler_dir,
        capture_output=True,
        text=True,
        timeout=600,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout or "MediaCrawler failed")

    # MediaCrawler usually writes JSON files into its own output directory.
    # Parse them here when wiring the real crawler.
    return []


def collect_posts(request: CollectRequest) -> list[CrawledPost]:
    settings = get_settings()
    if settings.mock_crawler or not settings.media_crawler_dir:
        return _mock_posts(request)
    return _run_media_crawler(request)


def to_dict(post: CrawledPost) -> dict[str, Any]:
    payload = asdict(post)
    payload["published_at"] = datetime.utcnow()
    payload["content_hash"] = _content_hash(
        post.platform, post.title, post.content
    )
    return payload

