from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Financial Document Intelligence Platform"
    environment: str = "development"
    database_url: str = "sqlite:///./financial_docs.db"
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    upload_dir: str = "storage/uploads"
    vector_dir: str = "storage/vectors"
    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    reranker_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def cors_origin_list(self) -> list[str]:
        origins = [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]
        # If any wildcard origins are present, allow all origins for simplicity in deployment
        if any("*" in origin for origin in origins):
            return ["*"]
        return origins


@lru_cache
def get_settings() -> Settings:
    return Settings()
