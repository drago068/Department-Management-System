"""
Database session management and engine configuration.
"""
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import (
    engine,
    async_session_maker,
    get_db,
)

# Alias for compatibility with common patterns
async_session_factory = async_session_maker

__all__ = [
    "engine",
    "async_session_maker",
    "async_session_factory",
    "get_db",
]
