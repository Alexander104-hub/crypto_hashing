from pydantic import BaseModel

class TextFile(BaseModel):
    text: str
    filename: str