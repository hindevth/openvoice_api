"""
Pydantic response models for Voice Cloning API
"""
from pydantic import BaseModel
from typing import Optional, List, Dict, Union

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    device: str
    models_loaded: bool
    timestamp: str

class VoiceExtractionResponse(BaseModel):
    """Voice extraction response"""
    audio_name: str
    embedding_name: Optional[str] = None

class VoiceCloneResponse(BaseModel):
    """Voice cloning response"""
    message: str
    output_file: Optional[str] = None
    output_path: Optional[str] = None
    audio_buffer: Optional[str] = None  # Base64 encoded audio data
    text: str
    language: str
    speaker: str
    speed: float
    reference_audio: Optional[str] = None

class SpeakersResponse(BaseModel):
    """Speakers list response"""
    supported_languages: List[str]
    speakers: Dict[str, List[str]]

class FileListResponse(BaseModel):
    """File list response"""
    files: List[Dict[str, Union[str, int]]]

class ErrorResponse(BaseModel):
    """Error response"""
    error: str
    detail: str
    status_code: int
