from pydantic import BaseModel

class TextFile(BaseModel):
    filename: str
    hash_algo: str
