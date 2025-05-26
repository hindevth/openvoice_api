"""
Audio utility functions
"""
import base64
import torch
import io
from typing import Tuple, Union
from app.config.settings import logger

def audio_file_to_base64(filepath: str) -> str:
    """Convert audio file to base64 string"""
    try:
        with open(filepath, 'rb') as audio_file:
            audio_data = audio_file.read()
            return base64.b64encode(audio_data).decode('utf-8')
    except Exception as e:
        logger.error(f"Error converting audio file to base64: {e}")
        raise

def base64_to_audio_file(base64_data: str, filepath: str) -> None:
    """Convert base64 string to audio file"""
    try:
        audio_data = base64.b64decode(base64_data)
        with open(filepath, 'wb') as audio_file:
            audio_file.write(audio_data)
    except Exception as e:
        logger.error(f"Error converting base64 to audio file: {e}")
        raise

def embedding_to_base64(embedding_tensor: torch.Tensor) -> str:
    """Convert PyTorch tensor to base64 string"""
    try:
        buffer = io.BytesIO()
        torch.save(embedding_tensor, buffer)
        buffer.seek(0)
        return base64.b64encode(buffer.read()).decode('utf-8')
    except Exception as e:
        logger.error(f"Error converting embedding to base64: {e}")
        raise

def base64_to_embedding(base64_data: str, device: str = 'cpu') -> torch.Tensor:
    """Convert base64 string to PyTorch tensor"""
    try:
        embedding_data = base64.b64decode(base64_data)
        buffer = io.BytesIO(embedding_data)
        buffer.seek(0)
        return torch.load(buffer, map_location=device)
    except Exception as e:
        logger.error(f"Error converting base64 to embedding: {e}")
        raise

def get_audio_buffer_from_file(filepath: str) -> bytes:
    """Get audio buffer from file"""
    try:
        with open(filepath, 'rb') as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error reading audio file {filepath}: {e}")
        raise

def save_audio_buffer_to_file(audio_buffer: bytes, filepath: str) -> None:
    """Save audio buffer to file"""
    try:
        with open(filepath, 'wb') as f:
            f.write(audio_buffer)
    except Exception as e:
        logger.error(f"Error saving audio buffer to file {filepath}: {e}")
        raise
