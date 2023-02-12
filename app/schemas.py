from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic.types import conint

class Post(BaseModel):
    title: str
    content: str

    published: bool = True

class User(BaseModel):
    email: EmailStr
    password: str

class ResponseUser(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime 

    class Config:
        orm_mode = True

class ResponsePost(Post):
    id: int
    created_at: datetime
    owner_id: int
    owner: ResponseUser

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: str

class Vote(BaseModel):
    post_id: int
    vote_dir: conint(le=1)

class PostOut(BaseModel):
    Post: ResponsePost
    votes: int
    
    class Config:
        orm_mode = True