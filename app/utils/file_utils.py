"""
File utility functions
"""
import os
import uuid
import aiofiles
from datetime import datetime
from fastapi import UploadFile
from app.config.settings import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, OUTPUT_FOLDER, logger

def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_unique_filename(filename: str) -> str:
    """Generate unique filename with timestamp and UUID"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    name, ext = os.path.splitext(filename)
    return f"{name}_{timestamp}_{unique_id}{ext}"

async def save_upload_file(upload_file: UploadFile, destination: str) -> None:
    """Save uploaded file asynchronously"""
    async with aiofiles.open(destination, 'wb') as f:
        content = await upload_file.read()
        await f.write(content)

def cleanup_file(filepath: str) -> bool:
    """Remove file if it exists"""
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            logger.info(f"Cleaned up file: {filepath}")
            return True
        return False
    except Exception as e:
        logger.error(f"Error cleaning up file {filepath}: {e}")
        return False

def get_file_info(filepath: str) -> dict:
    """Get file information"""
    if not os.path.exists(filepath):
        return None
    
    stat = os.stat(filepath)
    return {
        'filename': os.path.basename(filepath),
        'size': stat.st_size,
        'created_at': datetime.fromtimestamp(stat.st_ctime).isoformat(),
        'modified_at': datetime.fromtimestamp(stat.st_mtime).isoformat()
    }

async def cleanup_old_files(max_age_hours: int = 24):
    """Clean up files older than specified hours"""
    try:
        current_time = datetime.now().timestamp()
        max_age_seconds = max_age_hours * 3600
        
        for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER]:
            if not os.path.exists(folder):
                continue
                
            for filename in os.listdir(folder):
                filepath = os.path.join(folder, filename)
                if os.path.isfile(filepath):
                    file_age = current_time - os.path.getctime(filepath)
                    if file_age > max_age_seconds:
                        cleanup_file(filepath)
    except Exception as e:
        logger.error(f"Error in cleanup_old_files: {e}")
