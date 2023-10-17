from app.models.encryption_model import TEXT_ENCRYPTION
from app.utils.encryption import encrypt
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse, FileResponse


router = APIRouter(prefix='/api/encryption', tags=['encryption'])
CIPFERTEXT_FILE = 'ciphertext.txt'


@router.get("/", response_model=TEXT_ENCRYPTION)
async def encryption_read(text: str):
    ciphertext, key, tag, nonce = encrypt(text) 
    with open(CIPFERTEXT_FILE, 'w+') as f:
        f.write(ciphertext)
    return JSONResponse(
        content=[{'Шифротекст: ': ciphertext, 'Ключ: ': key, 'Тег: ': tag, 'Одноразовый код: ': nonce}],
        status_code=status.HTTP_200_OK,)


@router.get("/download_encrypted_text}")
def download_file():
    return FileResponse(path=CIPFERTEXT_FILE, media_type='application/octet-stream', filename=CIPFERTEXT_FILE)
