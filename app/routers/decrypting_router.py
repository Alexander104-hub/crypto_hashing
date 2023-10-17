from app.models.decryption_model import TEXT_DECRYPTION
from app.utils.decryption import decrypt
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse


router = APIRouter(prefix='/api/decryption', tags=['decryption'])


@router.get("/", response_model=TEXT_DECRYPTION)
async def read_item(ciphertext: str, key: str, tag: str, nonce: str):
    text = decrypt(ciphertext, key, tag, nonce)
    return JSONResponse(
        content=[text],
        status_code=status.HTTP_200_OK,)