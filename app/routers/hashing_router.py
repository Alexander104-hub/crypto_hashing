import json
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from app.utils.hash import file_hashing
from typing import Dict, Any
from app.models.hashing_model import TextFile

router = APIRouter(prefix='/api/hashing', tags=['hashing'])


@router.get("/", response_model=Dict[str, Any])
async def compute_file_hash():
    try:
        hash_func = file_hashing.Hash()
        hash_func.compute_file_hash("files_to_digest")
        with open("./hashes.json", "r") as file:
            hashes = json.load(file)
        return JSONResponse(status_code=status.HTTP_200_OK, content=hashes)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=str(e))
    


@router.post("/save_text")
async def save_text(file: TextFile):
    with open(f"files_to_digest/{file.filename}.txt", 'w+') as f:
        f.write(file.text)
    return JSONResponse(
        content=[{'Сообщение: ': 'Текст успешно сохранен'}],
        status_code=status.HTTP_200_OK,
    )
