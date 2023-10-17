from app.models.encryption_model import TEXT_ENCRYPTION
from app.utils.encryption import encrypt
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse


router = APIRouter(prefix='/api/encryption', tags=['encryption'])


@router.get("/", response_model=TEXT_ENCRYPTION)
async def read_item(text: str):
    ciphertext, key, tag, nonce = encrypt(text)
    return JSONResponse(
        content=[{'Шифротекст: ': ciphertext, 'Ключ: ': key, 'Тег: ': tag, 'Одноразовый код:': nonce}],
        status_code=status.HTTP_200_OK,)