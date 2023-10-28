from app.models.encryption_model import FILE_ENCRYPTION, TEXT_ENCRYPTION
from app.utils.encryption import encrypt, encrypt_file
from fastapi import APIRouter, status, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse
import os


DIR_PATH = 'encryption'

router = APIRouter(prefix='/api/encryption', tags=['encryption'])


@router.get("/", response_model=TEXT_ENCRYPTION)
async def encryption_read(text: str, mode: str, key: str = None, nonce: str = None, iv: str = None):
    return JSONResponse(
        content=[encrypt(text, mode, key, nonce, iv)],
        status_code=status.HTTP_200_OK,)


@router.post("/encrypt_file", response_model=FILE_ENCRYPTION)
async def encryption_read(file: UploadFile = File(...)):
    ciphertext, key, tag, nonce = encrypt_file(await file.read())
    encrypted_filename = f"{file.filename}"
    with open(f'{DIR_PATH}/{encrypted_filename}', 'wb') as f:
        f.write(ciphertext)
    return JSONResponse(
        content=[{'Ключ: ': key, 'Тег: ': tag, 'Одноразовый код: ': nonce}],
        status_code=status.HTTP_200_OK,
    )


@router.get("/download_encrypted_file/{filename}")
def download_encrypted_file(filename: str):
    return FileResponse(path=f"{DIR_PATH}/{filename}", media_type='application/octet-stream', filename=f"{filename}")


@router.get("/get_encrypted_files")
def get_files():
    files = os.listdir(f'{DIR_PATH}/')
    return JSONResponse(content=files, status_code=status.HTTP_200_OK)
