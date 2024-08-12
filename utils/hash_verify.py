#!/usr/bin/python3
from passlib.context import CryptContext


# Create a CryptContext object with the algorithm you want to use
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


#verify password

def verify_password(password: str, hash_pwd: str) -> bool:
    return pwd_context.verify(password, hash_pwd)


#hash password

def hash_password(password: str) -> str:

    hashed = pwd_context.hash(password)
    return hashed
