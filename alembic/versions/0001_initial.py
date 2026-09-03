"""initial tables

Revision ID: 0001
Revises:
Create Date: 2026-09-03

"""
from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE IF NOT EXISTS crawl_posts (
        id SERIAL PRIMARY KEY,
        platform VARCHAR NOT NULL,
        post_id VARCHAR NOT NULL,
        title VARCHAR NOT NULL,
        content TEXT NOT NULL,
        author VARCHAR NOT NULL,
        url VARCHAR NOT NULL,
        tags JSON NOT NULL,
        metrics JSON NOT NULL,
        published_at TIMESTAMP NULL,
        collected_at TIMESTAMP NOT NULL,
        content_hash VARCHAR NOT NULL
    )
    """)
    op.execute("""
    CREATE TABLE IF NOT EXISTS post_comments (
        id SERIAL PRIMARY KEY,
        post_id INTEGER REFERENCES crawl_posts(id),
        content TEXT NOT NULL,
        published_at TIMESTAMP NULL,
        sentiment VARCHAR NULL
    )
    """)
    op.execute("""
    CREATE TABLE IF NOT EXISTS analysis_jobs (
        id SERIAL PRIMARY KEY,
        status VARCHAR NOT NULL,
        note_ids JSON NOT NULL,
        model VARCHAR NOT NULL,
        result JSON NULL,
        error TEXT NULL,
        created_at TIMESTAMP NOT NULL,
        completed_at TIMESTAMP NULL
    )
    """)
    op.execute("""
    CREATE TABLE IF NOT EXISTS analysis_reports (
        id SERIAL PRIMARY KEY,
        title VARCHAR NOT NULL,
        platform VARCHAR NOT NULL,
        report_date VARCHAR NOT NULL,
        format VARCHAR NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP NOT NULL
    )
    """)
    op.execute("""
    CREATE TABLE IF NOT EXISTS crawl_tasks (
        id SERIAL PRIMARY KEY,
        platform VARCHAR NOT NULL,
        keyword VARCHAR NOT NULL,
        limit INTEGER NOT NULL,
        status VARCHAR NOT NULL,
        total INTEGER NOT NULL,
        succeeded INTEGER NOT NULL,
        failed INTEGER NOT NULL,
        error TEXT NULL,
        created_at TIMESTAMP NOT NULL,
        started_at TIMESTAMP NULL,
        finished_at TIMESTAMP NULL
    )
    """)


def downgrade() -> None:
    for table in ("crawl_tasks", "analysis_reports", "analysis_jobs", "post_comments", "crawl_posts"):
        op.execute(f"DROP TABLE IF EXISTS {table}")
