#!/usr/bin/python3
from app import app
from .test_user import token
from fastapi.testclient import TestClient

""" Testing the comment routes """

client = TestClient(app)
headers = {'Authorization': f"Bearer {token}"}
movie_data = {"title": "The Matrix", "release_date": "1999-03-31", "genre": "Action"}

# Test the create comment endpoint
def test_comment():
    res = client.get(
        "/api/v1/movies/",
            )




    #response = client.post(
    #    '/api/v1/movies/1/comments',
    #    json={'content': 'Interesting read.'},
    #    headers=headers
    #        )

    print(res.json())
