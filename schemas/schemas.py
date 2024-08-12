#!/usr/bin/python3
from pydantic import BaseModel, EmailStr 
from typing import Optional

# User validator
class Login(BaseModel):
    email: EmailStr
    password: str

class User_data(Login):
    name: str

# Token validator
class Token(BaseModel):
    access_token: str
    token_type: str
    status: int

# Movie validator
class MovieValidate(BaseModel):
    title : str
    release_date : str
    genre : str

class MovieUpdate(BaseModel):
    title : Optional[str] = None
    release_date : Optional[str] = None
    genre : Optional[str] = None

# Movie Rating validator
class RatingValidator(BaseModel):
    score : int

# Comment Validator
class CommentsValidator(BaseModel):
    content : str
