from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Social AI Assistant"
    api_prefix: str = "/api/v1"
    database_url: str = "sqlite:///./data/app.db"
    cors_origins: list[str] = ["*"]

    llm_base_url: str = "https://api.openai.com/v1"
    llm_api_key: str = ""
    llm_model: str = "gpt-4o-mini"

    media_crawler_dir: str = ""
    mock_crawler: bool = True

    schedule_enabled: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="SOCIAL_AI_",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()

