from typing import Annotated, Any, Dict
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.common import StandardResponse
from app.services.academic_service import AcademicService

router = APIRouter(prefix="/public", tags=["Public Showcase"])


@router.get("/department/showcase", response_model=StandardResponse[Dict[str, Any]])
async def get_department_showcase(db: Annotated[AsyncSession, Depends(get_db)]):
    showcase = await AcademicService.get_showcase(db)
    return StandardResponse(data=showcase, message="Public department showcase retrieved")
