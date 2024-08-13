#!/usr/bin/python3
from auth.jwt_utils import create_access_token

# TEST USER
name = "John Doe"
email = "JohnDoe@gmail.com"
password = "password"
token = create_access_token(data={'email': email})
