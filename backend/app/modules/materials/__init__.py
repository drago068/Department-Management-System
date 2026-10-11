"""
Materials feature module.
"""
from app.modules.materials.models import Material, MaterialDownload
from app.modules.materials.schemas import MaterialItemResponse
from app.modules.materials.service import MaterialService
from app.modules.materials.repository import MaterialRepository
from app.modules.materials.router import router

__all__ = [
    "Material",
    "MaterialDownload",
    "MaterialItemResponse",
    "MaterialService",
    "MaterialRepository",
    "router",
]
