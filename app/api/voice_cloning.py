import asyncio
from io import BytesIO
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.models.requests import VoiceCloneRequest
from app.models.responses import SpeakersResponse
from app.services.audio_service import audio_service
from app.services.voice_service import voice_service
from app.config.settings import SUPPORTED_LANGUAGES, logger
from app.utils.file_utils import cleanup_file

router = APIRouter()

@router.post("/clone_voice")
async def clone_voice(request: VoiceCloneRequest):
    """Clone voice using existing embedding file"""
    try:
        output_path = await audio_service.clone_voice_with_embedding(
            text=request.text,
            language=request.language,
            speaker=request.speaker,
            speed=request.speed,
            target_embedding_name=request.target_embedding_name,
        )

        # Read the audio file into a buffer
        with open(output_path, "rb") as audio_file:
            audio_content = audio_file.read()
        
        # Clean up files
        cleanup_file(output_path)
        
        # Create BytesIO buffer from audio content
        buffer = BytesIO(audio_content)
        buffer.seek(0)
        
        # Return streaming response
        return StreamingResponse(
            buffer, 
            media_type="audio/wav", 
            headers={
                "Content-Disposition": f"attachment; filename=cloned_voice.wav"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in clone_voice: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list_speakers", response_model=SpeakersResponse)
async def list_speakers():
    """List available speakers for each language"""
    try:
        speakers_info = {}

        # Get speakers for all languages in parallel
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(
                voice_service.executor,
                voice_service.get_speakers_for_language,
                lang
            )
            for lang in SUPPORTED_LANGUAGES
        ]

        results = await asyncio.gather(*tasks)

        for lang, speakers in zip(SUPPORTED_LANGUAGES, results):
            speakers_info[lang] = speakers

        return SpeakersResponse(
            supported_languages=SUPPORTED_LANGUAGES,
            speakers=speakers_info
        )

    except Exception as e:
        logger.error(f"Error in list_speakers: {e}")
        raise HTTPException(status_code=500, detail=str(e))
