from fastapi import APIRouter, status
from fastapi.responses import JSONResponse, FileResponse
from app.utils.hash import file_hashing, hash_diff
from app.models.hashing_model import TextFile

router = APIRouter(prefix='/api/hashing', tags=['hashing'])


@router.get("/", response_model=TextFile)
async def compute_file_hash(filepath: str):
    # Allow user select hash function he needs or wants.
    # https://www.pycrypto.org/doc/#crypto-hash-hash-functions
    try:
        hash_func = file_hashing.Hash()
        hashes = hash_func.compute_file_hash(filepath)
        return JSONResponse(status_code=status.HTTP_200_OK, content=hashes)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=str(e))
    


@router.get("/download_hashes")
async def save_text():
    # Generate checksum for files that will be generated:
    # md5, sha128, sha256
    return FileResponse(path="hashes.json", media_type='application/octet-stream', filename="hashes.json")

@router.get('/compute_diff')
def compute_diff(path1, path2):
    try:
        hashes_diff = hash_diff.HashDiff()
        hash1 = hashes_diff.preprocess_file_with_hashes(path1)
        hash2 = hashes_diff.preprocess_file_with_hashes(path2)
        difference = hashes_diff.compute_diff(hash1, hash2)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=str(e))
    else:
        return JSONResponse(status_code=status.HTTP_200_OK, content=eval(difference))
