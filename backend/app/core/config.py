from functools import lru_cache
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "College Management System (CMS) API"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # ── Database ──────────────────────────────────────────────────────────────
    # SQLite (local dev):     sqlite+aiosqlite:///./cms.db
    # Supabase / PostgreSQL:  postgresql+asyncpg://postgres.[project-ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres
    DATABASE_URL: str = "sqlite+aiosqlite:///./cms.db"

    # Connection pool — applies only when DATABASE_URL is PostgreSQL
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 5
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 1800  # 30 min — important for Supabase session-mode

    # ── Supabase (optional — for direct Supabase SDK usage / storage) ─────────
    SUPABASE_URL: Optional[str] = None
    SUPABASE_ANON_KEY: Optional[str] = None
    SUPABASE_SERVICE_ROLE_KEY: Optional[str] = None

    # ── Security ──────────────────────────────────────────────────────────────
    JWT_SECRET_KEY: str = "super-secret-development-key-change-in-production-nexus-cms"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # ── CORS ──────────────────────────────────────────────────────────────────
    ALLOWED_ORIGINS: str = "http://localhost:8081,http://127.0.0.1:8081,http://localhost:19006,http://localhost:3000,http://localhost:8082"

    # ── File uploads ──────────────────────────────────────────────────────────
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE_MB: int = 25

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    @property
    def cors_origins(self) -> List[str]:
        if not self.ALLOWED_ORIGINS:
            return ["*"]
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]

    @property
    def is_sqlite(self) -> bool:
        return self.DATABASE_URL.startswith("sqlite")

    @property
    def is_postgres(self) -> bool:
        return "postgresql" in self.DATABASE_URL or "postgres" in self.DATABASE_URL


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
