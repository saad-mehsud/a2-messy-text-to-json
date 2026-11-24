from pydantic import BaseModel
from typing import Optional


class Extracted(BaseModel):
    title:str
    company:str
    salary:Optional[str] = None
    location:Optional[str] = None
    skills:list[str]
    message:str|None