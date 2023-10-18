from pydantic import BaseModel

class TextFile(BaseModel):
    filename: str
