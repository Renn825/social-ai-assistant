from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "social-ai-assistant"
    api_key: str = "dev-api-key"
    database_url: str = "postgresql+psycopg://social:social@localhost:5432/social"
    openai_api_key: str = "sk-your-key"
    openai_base_url: str = "https://api.deepseek.com/v1"
    openai_model: str = "deepseek-chat"
    enable_scheduler: bool = False
    log_level: str = "INFO"
    analysis_max_items: int = 20
    report_output_dir: Path = Path("outputs/reports")
    sample_data_dir: Path = Path("data/samples")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
