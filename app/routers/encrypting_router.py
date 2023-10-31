import os
from app.models.encryption_model import FILE_ENCRYPTION, TEXT_ENCRYPTION
from app.utils.encryption import encrypt, encrypt_file
from fastapi import APIRouter, status, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse


DIR_PATH = 'encryption'

router = APIRouter(prefix='/api/encryption', tags=['encryption'])


@router.get("/", response_model=TEXT_ENCRYPTION)
async def encryption_read(text: str, mode: str, key = None):
    if key and (len(key) < 8 or len(key) > 32 or len(key) % 8 != 0):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,\
                content="Key len must be divisible by 8 and in range from 16 to 32.")
    return JSONResponse(
        content=[encrypt(text, mode, key)], 
        status_code=status.HTTP_200_OK,)


@router.post("/encrypt_file", response_model=FILE_ENCRYPTION)
async def encryption_read_file(mode: str, key = None, file: UploadFile = File(...)):
    # ciphertext, key, tag, nonce = encrypt(await file.read(), mode, key)
    contents = encrypt(await file.read(), mode, key, encrypt_file=True)
    ciphertext = contents['Шифротекст: ']
    encrypted_filename = f"{file.filename}"
    with open(f'{DIR_PATH}/{encrypted_filename}', 'wb') as f:
        f.write(ciphertext.encode())
    return JSONResponse(
        # content=[{'Ключ: ': key, 'Тег: ': tag, 'Одноразовый код: ': nonce}],
        content=[contents],
        status_code=status.HTTP_200_OK,
    )


@router.get("/download_encrypted_file/{filename}")
def download_encrypted_file(filename: str):
    return FileResponse(path=f"{DIR_PATH}/{filename}",\
            media_type='application/octet-stream',\
            filename=f"{filename}")


@router.get("/get_encrypted_files")
def get_files():
    files = os.listdir(f'{DIR_PATH}/')
    return JSONResponse(content=files, status_code=status.HTTP_200_OK)
