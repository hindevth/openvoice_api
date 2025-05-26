"""
Pydantic request models for Voice Cloning API
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from app.config.settings import DEFAULT_SPEAKERS

class VoiceCloneRequest(BaseModel):
    """Request model for voice cloning with existing embedding"""
    text: str = Field(default="Xin chào, đây là giọng nói được nhân bản", description="Text to convert to speech")
    language: str = Field(default="VI", description="Language code (VI, EN, ZH, JP, KR)")
    speaker: Optional[str] = Field(None, description="Speaker voice to use")
    speed: float = Field(default=0.9, ge=0.1, le=2.0, description="Speech speed")
    target_embedding_name: str = Field(..., description="Name to target voice embedding file")
    
    @field_validator('speaker', mode='before')
    def set_default_speaker(cls, v, values):
        if v is not None:
            return v
        language = values.get('language', 'VI')
        if language in DEFAULT_SPEAKERS and DEFAULT_SPEAKERS[language] is not None:
            return DEFAULT_SPEAKERS[language]
        # Fallback to VI-hue if no default speaker for the language
        return "VI-hue"

class VoiceCloneWithFileRequest(BaseModel):
    """Request model for voice cloning with uploaded audio file"""
    text: str = Field(default="Xin chào, đây là giọng nói được nhân bản", description="Text to convert to speech")
    language: str = Field(default="VI", description="Language code (VI, EN, ZH, JP, KR)")
    speaker: Optional[str] = Field(None, description="Speaker voice to use")
    speed: float = Field(default=0.9, ge=0.1, le=2.0, description="Speech speed")
    return_audio_buffer: bool = Field(default=True, description="Return audio as buffer instead of file path")
    
    @field_validator('speaker', mode='before')
    def set_default_speaker(cls, v, values):
        if v is not None:
            return v
        language = values.get('language', 'VI')
        if language in DEFAULT_SPEAKERS and DEFAULT_SPEAKERS[language] is not None:
            return DEFAULT_SPEAKERS[language]
        # Fallback to VI-hue if no default speaker for the language
        return "VI-hue"
