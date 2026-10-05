from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.core.config import settings

# ── Engine configuration ───────────────────────────────────────────────────────
# SQLite needs check_same_thread=False and no pool size args.
# PostgreSQL (Supabase) uses asyncpg with tuned pool settings.
#
# Supabase connection modes:
#   • Transaction mode (port 6543) – stateless, supports pgbouncer, no prepared stmts
#   • Session mode   (port 5432)  – full PostgreSQL features, single connection per session
#
# We default to Transaction mode (port 6543) which is recommended for serverless/async apps.
# Set prepared_statement_cache_size=0 to disable prepared statements for pgbouncer compat.

if settings.is_sqlite:
    connect_args = {"check_same_thread": False}
    pool_kwargs = {}
else:
    # asyncpg connect_args for Supabase pgbouncer (Transaction mode)
    connect_args = {
        "statement_cache_size": 0,          # Required for pgbouncer in Transaction mode
        "prepared_statement_cache_size": 0,  # Required for pgbouncer in Transaction mode
    }
    pool_kwargs = {
        "pool_size": settings.DB_POOL_SIZE,
        "max_overflow": settings.DB_MAX_OVERFLOW,
        "pool_timeout": settings.DB_POOL_TIMEOUT,
        "pool_recycle": settings.DB_POOL_RECYCLE,
        "pool_pre_ping": True,  # Reconnect on stale connections (important for Supabase)
    }

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG and settings.is_sqlite,  # Only echo SQL in SQLite dev mode
    connect_args=connect_args,
    **pool_kwargs,
)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
