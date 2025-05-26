"""
Health check endpoints
"""
from fastapi import APIRouter
from datetime import datetime

from app.models.responses import HealthResponse
from app.services.voice_service import voice_service
from app.config.settings import DEVICE

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Check API health status"""
    return HealthResponse(
        status="healthy",
        device=DEVICE,
        models_loaded=voice_service.is_models_loaded(),
        timestamp=datetime.now().isoformat()
    )
