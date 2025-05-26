"""
Voice extraction endpoints
"""
from fastapi import APIRouter, File, UploadFile, HTTPException, Query
from app.models.responses import VoiceExtractionResponse
from app.services.audio_service import audio_service

router = APIRouter()

@router.post("/extract_voice", response_model=VoiceExtractionResponse)
async def extract_voice(
    audio_file: UploadFile = File(...),
):
    """Extract voice embedding from audio file"""
    try:
        result = await audio_service.extract_voice_embedding(
            audio_file=audio_file,
        )
        
        return VoiceExtractionResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
