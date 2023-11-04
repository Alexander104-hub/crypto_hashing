from pydantic import BaseModel

class TEXT_DECRYPTION(BaseModel):
    decrypted_text: str = ''


class PROVIDED_ARGS(BaseModel):
    iv: str = ""
    tag: str = ""
    nonce: str = ""
