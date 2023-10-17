from app.models.decryption_model import TEXT_DECRYPTION
from app.utils.decryption import decrypt
from fastapi import APIRouter, status, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import aiofiles


router = APIRouter(prefix='/api/decryption', tags=['decryption'])


@router.get("/", response_model=TEXT_DECRYPTION)
async def decryption_read(ciphertext: str, key: str, tag: str, nonce: str):
    text = decrypt(ciphertext, key, tag, nonce)
    return JSONResponse(
        content=[text],
        status_code=status.HTTP_200_OK,)


@router.post("/uploadfile/", response_model=TEXT_DECRYPTION)
async def upload_file(file: UploadFile, key: str, tag: str, nonce: str):
    if file.filename.endswith(".txt"):
        async with aiofiles.open(file.filename, 'r') as f:
            ciphertext = await f.read()
        text = decrypt(ciphertext, key, tag, nonce)
        return {"decrypted_text": text}
    else:
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a .txt file.")
