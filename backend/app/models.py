from pydantic import BaseModel
from typing import List, Optional

class BookInput(BaseModel):
    pdf_path: str
    pdf_name: str

class SessionInput(BaseModel):
    pdf_path: str
    start_page: int
    end_page: int
    user_notes: str
    reflection: List[str]
    date: Optional[str] = None

class TextInput(BaseModel):
    text: str
    