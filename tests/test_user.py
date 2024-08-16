#!/usr/bin/python3
from auth.jwt_utils import create_access_token

# TEST USER
name = "Johnjass"
email = "Johoonysee@mail.com"
password = "password"
token = create_access_token(data={'email': email})
