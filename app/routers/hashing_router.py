import json
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse, FileResponse
from app.utils.hash import file_hashing
from typing import Dict, Any
from app.models.hashing_model import TextFile

router = APIRouter(prefix='/api/hashing', tags=['hashing'])


@router.get("/", response_model=TextFile)
async def compute_file_hash(filepath: str):
    try:
        hash_func = file_hashing.Hash()
        hash_func.compute_file_hash(filepath)
        with open("./hashes.json", "r") as file:
            hashes = json.load(file)
        return JSONResponse(status_code=status.HTTP_200_OK, content=hashes)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=str(e))
    


@router.get("/download_hashes")
async def save_text():
    return FileResponse(path="hashes.json", media_type='application/octet-stream', filename="hashes.json")
