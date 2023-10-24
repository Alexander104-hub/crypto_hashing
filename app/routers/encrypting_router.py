from app.models.encryption_model import FILE_ENCRYPTION, TEXT_ENCRYPTION
from app.utils.encryption import encrypt, encrypt_file
from fastapi import APIRouter, status, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse


router = APIRouter(prefix='/api/encryption', tags=['encryption'])
CIPFERTEXT_FILE = 'ciphertext.txt'
ENCRYPTED_FILE = 'encrypted_file.txt'

@router.get("/", response_model=TEXT_ENCRYPTION)
async def encryption_read(text: str):
    ciphertext, key, tag, nonce = encrypt(text) 
    with open(CIPFERTEXT_FILE, 'w+') as f:
        f.write(ciphertext)
    return JSONResponse(
        content=[{'Шифротекст: ': ciphertext, 'Ключ: ': key, 'Тег: ': tag, 'Одноразовый код: ': nonce}],
        status_code=status.HTTP_200_OK,)


@router.post("/encrypt_file", response_model=FILE_ENCRYPTION)
async def encryption_read(file: UploadFile = File(...)):
    ciphertext, key, tag, nonce = encrypt_file(await file.read())
    with open(ENCRYPTED_FILE, 'wb') as f:
        f.write(ciphertext)
    return JSONResponse(
        content=[{'Ключ: ': key, 'Тег: ': tag, 'Одноразовый код: ': nonce}],
        status_code=status.HTTP_200_OK,
    )


@router.get("/download_encrypted_file")
def download_file():
    return FileResponse(path=ENCRYPTED_FILE, media_type='application/octet-stream', filename=ENCRYPTED_FILE)
