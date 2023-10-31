from app.models.decryption_model import TEXT_DECRYPTION
from app.utils.decryption import decrypt_cbc, decrypt_eax, decrypt_ebc, decrypt_file
from fastapi import APIRouter, status, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse
import os


router = APIRouter(prefix='/api/decryption', tags=['decryption'])
DIR_PATH = 'decryption'


# @router.get("/", response_model=TEXT_DECRYPTION)
# async def decryption_read(ciphertext: str, key: str, mode: str, tag: str = None, nonce: str = None):
#     text = decrypt(ciphertext, key, tag, nonce)
#     return JSONResponse(
#         content=[text],
#         status_code=status.HTTP_200_OK,)

@router.get("/decrypt_eax", response_model=TEXT_DECRYPTION)
async def decrypt_eax_read(ciphertext: str, key: str, tag: str, nonce: str):
    text = decrypt_eax(ciphertext, key, tag, nonce)
    return JSONResponse(
        content=[text],
        status_code=status.HTTP_200_OK,)

@router.get("/decrypt_cbc", response_model=TEXT_DECRYPTION)
async def decrypt_cbc_read(ciphertext: str, key: str, iv: str):
    text = decrypt_cbc(ciphertext, key, iv)
    return JSONResponse(
        content=[text],
        status_code=status.HTTP_200_OK,)

@router.get("/decrypt_ebc", response_model=TEXT_DECRYPTION)
async def decrypt_ebc_read(ciphertext: str, key: str):
    text = decrypt_ebc(ciphertext, key)
    return JSONResponse(
        content=[text],
        status_code=status.HTTP_200_OK,)

@router.post("/decrypt_file")
async def upload_encrypted_file(mode: str, key: str, iv: str = None, tag: str = None, nonce: str = None, file: UploadFile=File(...)):
    decrypted_text = decrypt_file(await file.read(), mode, key, iv, tag, nonce)
    decrypted_filename = f"{file.filename}"
    # ciphertext = await file.read()
    with open(f"{DIR_PATH}/{decrypted_filename}", 'wb') as f:
        f.write(decrypted_text)
    return JSONResponse(
        content=[],
        status_code=status.HTTP_200_OK,
    )


@router.get("/download_decrypted_file/{filename}")
def download_decrypted_file(filename: str):
    return FileResponse(path=f"{DIR_PATH}/{filename}", media_type='application/octet-stream', filename=f"{filename}")


@router.delete("/delete_decrypted_file/{filename}")
async def delete_decrypted_file(filename: str):
    file_path = f"{DIR_PATH}/{filename}"
    if os.path.exists(file_path):
        os.remove(file_path)
        return JSONResponse(
            content={"message": f"Файл '{filename}' был удален."},
            status_code=status.HTTP_200_OK,
        )
    else:
        raise HTTPException(status_code=404, detail="Файл не найден.")
