from app.models.decryption_model import TEXT_DECRYPTION
from app.utils.decryption import decrypt, decrypt_file
from fastapi import APIRouter, status, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse


router = APIRouter(prefix='/api/decryption', tags=['decryption'])
DECRYPTED_FILE = 'decrypted_file.txt'


@router.get("/", response_model=TEXT_DECRYPTION)
async def decryption_read(ciphertext: str, key: str, tag: str, nonce: str):
    text = decrypt(ciphertext, key, tag, nonce)
    return JSONResponse(
        content=[text],
        status_code=status.HTTP_200_OK,)


@router.post("/decrypt_file", response_model=TEXT_DECRYPTION)
async def upload_encrypted_file(file: UploadFile, key: str, tag: str, nonce: str):
    decrypted_text = decrypt_file(await file.read(), key, tag, nonce)
    with open(DECRYPTED_FILE, 'wb') as f:
        f.write(decrypted_text)
    return JSONResponse(
        content=[{'Decrypted Text': decrypted_text.decode('utf-8')}],
        status_code=status.HTTP_200_OK,
    )

@router.get("/download_decrypted_file")
def download_decrypted_file():
    return FileResponse(path=DECRYPTED_FILE, media_type='application/octet-stream', filename=DECRYPTED_FILE)
