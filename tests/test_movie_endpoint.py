#!/usr/bin/python3
from app import app, get_current_user
from fastapi.testclient import TestClient
from .test_user import name, email, password, token

# create a testclient instance
client = TestClient(app)

# Sample data for the test
movie_data = {
    "title": "Inception",
    "release_date": "2010-07-16",
    "genre": "Sci-Fi"
    }

# headers for authenticated routes
headers = {"Authorization": f"Bearer {token}"}

# create a movie
def test_add_movie():
    # create a header 
    response = client.post(
            "/api/v1/movies",
            json = movie_data,
            headers = headers
        )

    data = response.json()
    assert response.status_code == 200 
    assert data['title'] == movie_data['title']
    assert type(data) == dict

# test the movie_update endpoint
def test_movie_update():
    response = client.put(
        "/api/v1/movies/1/",
        json = {'title': 'The gods are crazy!!', 'genre': 'comedy'},
        headers = headers
            )

    data = response.json()
    

    assert data['movie']['title'] == 'The gods are crazy!!'
    assert data['movie']['genre'] == 'comedy'
    assert data['status'] == 206


# GET all movies test
def test_movies():
    response = client.get(
        "/api/v1/movies",
            )
    
    assert type(response.json()) == dict
    assert response.status_code == 200
    

# GET a movie test
def test_get_a_movies():
    response = client.get(
            "/api/v1/movies/1/",
            )

    assert type(response.json()) == dict
    assert response.status_code == 200

# DELETE a movie
def test_drop_movie():
    response = client.delete(
        "/api/v1/movies/1/",
        headers = headers
            )

    assert response.json()['status'] == 204
