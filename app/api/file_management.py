"""
File management endpoints
"""
import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.models.responses import FileListResponse
from app.config.settings import OUTPUT_FOLDER, logger
from app.utils.file_utils import cleanup_file, get_file_info

router = APIRouter()

@router.get("/download/{filename}")
async def download_file(filename: str):
    """Download generated audio file"""
    try:
        filepath = os.path.join(OUTPUT_FOLDER, filename)
        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail="File not found")
        
        return FileResponse(
            path=filepath,
            filename=filename,
            media_type='audio/wav'
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in download_file: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/cleanup/{filename}")
async def cleanup_file_endpoint(filename: str):
    """Delete specific file"""
    try:
        filepath = os.path.join(OUTPUT_FOLDER, filename)
        if cleanup_file(filepath):
            return {"message": f"File {filename} deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="File not found")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in cleanup_file: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/files", response_model=FileListResponse)
async def list_output_files():
    """List all output files"""
    try:
        files = []
        if os.path.exists(OUTPUT_FOLDER):
            for filename in os.listdir(OUTPUT_FOLDER):
                filepath = os.path.join(OUTPUT_FOLDER, filename)
                if os.path.isfile(filepath):
                    file_info = get_file_info(filepath)
                    if file_info:
                        files.append(file_info)
        
        return FileListResponse(files=files)
        
    except Exception as e:
        logger.error(f"Error in list_output_files: {e}")
        raise HTTPException(status_code=500, detail=str(e))
