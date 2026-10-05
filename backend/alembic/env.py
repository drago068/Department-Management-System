import asyncio
from logging.config import fileConfig
import os
import sys

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# Prepend backend to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.config import settings
from app.models.base import Base
import app.models  # Load all models so Alembic can detect schema changes

# ── Alembic config ─────────────────────────────────────────────────────────────
config = context.config

# Inject DATABASE_URL from .env (overrides any sqlalchemy.url in alembic.ini)
# Set DB url from settings, escaping % for ConfigParser interpolation
# ConfigParser uses % as an interpolation marker, so %40 → %%40
_db_url = settings.DATABASE_URL.replace("%", "%%")
config.set_main_option("sqlalchemy.url", _db_url)

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# ── Helpers ────────────────────────────────────────────────────────────────────
def _get_context_configure_kwargs() -> dict:
    """
    Returns context.configure() kwargs tuned per dialect:
      - SQLite: render_as_batch=True (required for ALTER TABLE support)
      - PostgreSQL: render_as_batch=False (native ALTER TABLE support)
    """
    kwargs = {
        "target_metadata": target_metadata,
        "compare_type": True,           # Detect column type changes
        "compare_server_default": True, # Detect server default changes
    }
    if settings.is_sqlite:
        kwargs["render_as_batch"] = True
    return kwargs


# ── Offline mode ───────────────────────────────────────────────────────────────
def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode (generates SQL without a DB connection).
    Useful for reviewing migrations or applying them manually in Supabase SQL Editor.
    """
    url = config.get_main_option("sqlalchemy.url")
    # For asyncpg URL, convert to sync psycopg2 URL for offline generation
    sync_url = url.replace("postgresql+asyncpg://", "postgresql://").replace(
        "sqlite+aiosqlite://", "sqlite://"
    )
    context.configure(
        url=sync_url,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        **_get_context_configure_kwargs(),
    )

    with context.begin_transaction():
        context.run_migrations()


# ── Online mode (async) ────────────────────────────────────────────────────────
def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, **_get_context_configure_kwargs())
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Create an async engine and run migrations online."""
    # For Supabase Transaction mode (pgbouncer) — disable prepared statements
    connect_args = {}
    if settings.is_postgres:
        connect_args = {
            "statement_cache_size": 0,
            "prepared_statement_cache_size": 0,
        }

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        connect_args=connect_args,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
