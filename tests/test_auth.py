#!/usr/bin/python3
from app import app
from fastapi.testclient import TestClient
from .test_user import name, email, password

""" Testing the authentication endpoints """

client = TestClient(app)

# Test the signup endpoint

def test_signup():
    response = client.post('/api/v1/signup',
            json = {"name": name, "email": email, "password": password}
            )
    res_code =  response.json().get('status_code')
    assert response.status_code == 200
    assert res_code == 201


# Test the Token generation endpoint
def test_token_gen():
    response = client.post(
        "/api/v1/auth/token/",
        json = {"email": email, "password": password}
            )

    res_data = response.json()

    assert type(res_data) == dict
    assert res_data['status'] == 200
