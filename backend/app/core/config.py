from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ResearchAI API"
    app_version: str = "0.1.0"
    app_env: str = "development"
    api_v1_prefix: str = "/api/v1"
    frontend_url: str = "http://localhost:5173"
    database_url: str = "postgresql+psycopg://researchai_user:password@localhost:5432/researchai_dev"
    secret_key: str = "change_this_secret_key"
    access_token_expire_minutes: int = 60
    openai_api_key: str = "your_openai_api_key"
    file_storage_path: str = "../storage"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
