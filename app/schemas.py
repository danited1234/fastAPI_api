from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published:bool = True

class PostCreate(PostBase):
    pass


class Post(PostBase):
    id:int
    created_at:datetime
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email:EmailStr
    password:str
class UserResponse(BaseModel):
    id:int
    email:EmailStr
    class Config:
        from_attributes = True


class Userlogin(BaseModel):
    email : EmailStr
    password : str


class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[str] = None
