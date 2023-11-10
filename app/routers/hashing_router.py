from fastapi import APIRouter, UploadFile, status, File
from fastapi.responses import JSONResponse, FileResponse
from app.utils.hash import file_hashing, hash_diff
from app.models.hashing_model import TextFile
from typing import List

router = APIRouter(prefix='/api/hashing', tags=['hashing'])


@router.post("/", response_model=TextFile)
async def compute_file_hash(hash_algo: str, files: List[UploadFile]):
    # Allow user select hash function he needs or wants.
    # https://www.pycrypto.org/doc/#crypto-hash-hash-functions
    #https://stackoverflow.com/questions/73442335/how-to-upload-a-large-file-%E2%89%A53gb-to-fastapi-backend 
    try:
        hash_func = file_hashing.Hash()
        hashes = await hash_func.compute_file_hash(files, hash_algo=hash_algo)
        return JSONResponse(status_code=status.HTTP_200_OK, content=hashes)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=str(e))
    


@router.get("/download_hashes")
async def save_text():
    # Generate checksum for files that will be generated:
    # sha128, sha256
    return FileResponse(path="hashes.json", media_type='application/octet-stream', filename="hashes.json")

@router.post('/compute_diff')
async def compute_diff(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    try:
        hashes_diff = hash_diff.HashDiff()
        hash1 = hashes_diff.preprocess_file_with_hashes(await file1.read())
        hash2 = hashes_diff.preprocess_file_with_hashes(await file2.read())
        difference = hashes_diff.compute_diff(hash1, hash2)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=str(e))
    else:
        return JSONResponse(status_code=status.HTTP_200_OK, content=difference)
