"""
Audio processing service
"""
import os
import uuid
import torch
import asyncio
from fastapi import UploadFile, HTTPException

from app.config.settings import OUTPUT_FOLDER, UPLOAD_FOLDER, MAX_FILE_SIZE
from app.utils.file_utils import get_unique_filename, cleanup_file, allowed_file
from app.utils.audio_utils import audio_file_to_base64, embedding_to_base64
from app.services.voice_service import voice_service

class AudioService:
    """Service for audio processing operations"""

    async def extract_voice_embedding(
        self,
        audio_file: UploadFile,
    ) -> dict:
        """Extract voice embedding from uploaded audio file"""
        # Validate file
        if not allowed_file(audio_file.filename):
            raise HTTPException(
                status_code=400,
                detail="File type not supported. Use: wav, mp3, flac, m4a"
            )

        # Check file size
        content = await audio_file.read()
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="File too large. Maximum size is 50MB"
            )

        # Save temporary file
        unique_filename = get_unique_filename(audio_file.filename)
        temp_filepath = os.path.join(UPLOAD_FOLDER, unique_filename)

        # Write content to temp file
        with open(temp_filepath, 'wb') as f:
            f.write(content)

        try:
            # Extract voice embedding in thread pool
            loop = asyncio.get_event_loop()
            target_se, audio_name = await loop.run_in_executor(
                voice_service.executor,
                voice_service.extract_voice_embedding,
                temp_filepath
            )

            result = {
                "audio_name": audio_name
            }

            # Save embedding to file
            unique_id = str(uuid.uuid4())[:8]
            se_filename = f"{unique_id}.pth"
            se_filepath = os.path.join(OUTPUT_FOLDER, se_filename)
            torch.save(target_se, se_filepath)

            result.update({
                "embedding_name": unique_id
            })

            return result

        finally:
            # Clean up temp file
            cleanup_file(temp_filepath)

    async def clone_voice_with_embedding(
        self,
        text: str,
        language: str,
        speaker: str,
        speed: float,
        target_embedding_name: str,
    ) -> str:
        """Clone voice using existing embedding file"""
        path = f"{OUTPUT_FOLDER}/{target_embedding_name}.pth"
        if not os.path.exists(path):
            raise HTTPException(
                status_code=400,
                detail="Target voice embedding file not found"
            )

        if not voice_service.is_models_loaded():
            raise HTTPException(
                status_code=500,
                detail="Models not loaded"
            )

        # Load target voice embedding
        target_se = torch.load(path, map_location=voice_service.device)

        # Prepare paths
        unique_id = str(uuid.uuid4())[:8]
        src_path = os.path.join(OUTPUT_FOLDER, f'tmp_{unique_id}.wav')
        output_path = os.path.join(OUTPUT_FOLDER, f'cloned_voice_{unique_id}.wav')

        try:
            # Generate cloned voice in thread pool
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                voice_service.executor,
                voice_service.generate_cloned_voice,
                text,
                language,
                speaker,
                speed,
                target_se,
                src_path,
                output_path
            )

            return output_path

        finally:
            # Clean up temp file
            cleanup_file(src_path)

# Global audio service instance
audio_service = AudioService()
