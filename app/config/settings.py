"""
Configuration settings for Voice Cloning API
"""
import os
import torch
import logging

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Directories
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs_v2'

# File settings
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac', 'm4a'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

# Model settings
DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"
MAX_WORKERS = 4

# Supported languages
SUPPORTED_LANGUAGES = ['VI', 'EN', 'ZH', 'JP', 'KR']

# Default speakers for each language
DEFAULT_SPEAKERS = {
    "VI": "VI-default",
    "EN": "EN-Default",
    "ZH": "ZH",
    "JP": "JP",
    "KR": "KR"
}

# Create necessary directories
def create_directories():
    """Create necessary directories if they don't exist"""
    directories = [UPLOAD_FOLDER, OUTPUT_FOLDER]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"Directory ensured: {directory}")

# API settings
API_TITLE = "Voice Cloning API"
API_DESCRIPTION = "API for voice cloning using OpenVoice and MeloTTS"
API_VERSION = "2.0.0"

# CORS settings
CORS_ORIGINS = ["*"]
CORS_CREDENTIALS = True
CORS_METHODS = ["*"]
CORS_HEADERS = ["*"]

# File cleanup settings
CLEANUP_INTERVAL_HOURS = 24
