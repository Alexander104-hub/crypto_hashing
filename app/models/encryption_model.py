from pydantic import BaseModel

class TEXT_ENCRYPTION(BaseModel):
    key: str = ''
    tag: str = ''
    nonce: str = ''
    encrypted_text: str = ''

class FILE_ENCRYPTION(BaseModel):
    key: str = ''
    tag: str = ''
    nonce: str = ''
