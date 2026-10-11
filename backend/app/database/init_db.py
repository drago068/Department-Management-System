"""
Database initialization and schema migration bootstrap.
"""
import logging
from sqlalchemy.ext.asyncio import AsyncEngine
from app.models.base import Base
import app.models  # Ensure all models are registered with Base.metadata

logger = logging.getLogger(__name__)


async def init_db(engine: AsyncEngine) -> None:
    """
    Initializes tables in database if they do not exist.
    """
    logger.info("Initializing database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables initialized successfully.")
