from typing import Any, Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audit import AuditLog


class AuditService:
    @staticmethod
    async def log_action(
        db: AsyncSession,
        action: str,
        entity_name: str,
        entity_id: str,
        user_id: Optional[uuid.UUID] = None,
        details: Optional[Any] = None,
        ip_address: Optional[str] = None,
    ) -> AuditLog:
        audit_entry = AuditLog(
            user_id=user_id,
            action=action,
            entity_name=entity_name,
            entity_id=str(entity_id),
            details=details,
            ip_address=ip_address,
        )
        db.add(audit_entry)
        # Flush so it is written within the current transaction
        await db.flush()
        return audit_entry
