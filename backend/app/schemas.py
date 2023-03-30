from pydantic import BaseModel
from typing import Optional

class msglink(BaseModel):
    link: str

class users(BaseModel):
    id: Optional[int] = None
    name: str
    email: str 
    password: str

    class Config:
       orm_mode = True

class links(BaseModel):
    id: Optional[int] = None
    title: str
    link: str
    name: str
    description: str 
    user_id: int

    class Config:
        orm_mode = True

