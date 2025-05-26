"""
OpenVoice FastAPI Application
"""
import os
import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Add parent directory to path for imports when running directly
if __name__ == "__main__":
    current_dir = Path(__file__).parent
    parent_dir = current_dir.parent
    sys.path.insert(0, str(parent_dir))

# Try relative imports first, then absolute imports
try:
    from app.config.settings import (
        API_TITLE, API_DESCRIPTION, API_VERSION,
        CORS_ORIGINS, CORS_CREDENTIALS, CORS_METHODS, CORS_HEADERS,
        create_directories, logger
    )
    from app.services.voice_service import voice_service
    from app.utils.file_utils import cleanup_old_files
    from app.api import health, voice_extraction, voice_cloning, file_management
except ImportError:
    from app.config.settings import (
        API_TITLE, API_DESCRIPTION, API_VERSION,
        CORS_ORIGINS, CORS_CREDENTIALS, CORS_METHODS, CORS_HEADERS,
        create_directories, logger
    )
    from app.services.voice_service import voice_service
    from app.utils.file_utils import cleanup_old_files
    from app.api import health, voice_extraction, voice_cloning, file_management

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("OpenVoice FastAPI server starting up")
    create_directories()
    logger.info(f"Using device: {voice_service.device}")
    logger.info(f"Models loaded: {voice_service.is_models_loaded()}")

    yield

    # Shutdown
    logger.info("OpenVoice FastAPI server shutting down")
    voice_service.shutdown()

# Create FastAPI app
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=CORS_CREDENTIALS,
    allow_methods=CORS_METHODS,
    allow_headers=CORS_HEADERS,
)

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(voice_extraction.router, tags=["Voice Extraction"])
app.include_router(voice_cloning.router, tags=["Voice Cloning"])
app.include_router(file_management.router, tags=["File Management"])

# Background task endpoint for cleanup
@app.post("/cleanup_old_files")
async def cleanup_old_files_endpoint():
    """Clean up old files (background task)"""
    try:
        await cleanup_old_files()
        return {"message": "Old files cleanup completed"}
    except Exception as e:
        logger.error(f"Error in cleanup_old_files: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get('PORT', 8000))

    logger.info(f"Starting OpenVoice FastAPI server on port {port}")

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        workers=1  # Single worker due to model loading
    )
