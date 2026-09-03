from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "social-ai-assistant"
    api_prefix: str = "/api/v1"
    api_key: str = "dev-api-key"
    database_url: str = "postgresql+psycopg://social:social@localhost:5432/social"
    cors_origins: list[str] = ["*"]

    llm_base_url: str = "https://api.deepseek.com/v1"
    llm_api_key: str = "sk-your-key"
    llm_model: str = "deepseek-chat"

    media_crawler_dir: str = ""
    mock_crawler: bool = True
    schedule_enabled: bool = False
    analysis_max_items: int = 20
    report_output_dir: Path = Path("outputs/reports")
    sample_data_dir: Path = Path("data/samples")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
