#!/usr/bin/python3
from app import app
from .test_user import token
from fastapi.testclient import TestClient

# headers
headers = {'Authorization': f"Bearer {token}"}

# Sample data for the test
movie_data = {
    "title": "Inception",
    "release_date": "2010-07-16",
    "genre": "Sci-Fi"
    }


# test client instance
client = TestClient(app)
# rate a movie
def test_rating():
    data = {"score": 2}

    create_movie = client.post(
        "/api/v1/movies/",
        json = movie_data,
        headers = headers,
            )

    id = create_movie.json().get('id')

    

    response = client.post(
        f"/api/v1/movies/{id}/ratings/",
        json = data,
        headers = headers
            )

    assert response.json()['status_code'] == 201 and response.status_code == 200

# GET ratings for a movie
def test_get_ratings():
    response = client.get(
        "/api/v1/movies/1/ratings/",
            )

    assert "ratings" in response.json().keys()
    assert response.status_code == 200

# Add Comment 
def test_comment():
    json = {'content': 'Interesting read.'}
    response = client.post(
        '/api/v1/movies/1/comments',
        json={'content': 'Interesting read.'},
        headers=headers
    )
    print(response.json())
    assert 'comment' in response.json().keys()

    assert json['content'] == response.json()['comment']['content']
    assert response.status_code == 200

def test_get_comments():
    response = client.get(
        '/api/v1/movies/1/comments'
        )

    assert response.status_code == 200
    assert type(response.json()) == dict

def test_nested_comments():
    data = {'content': 'Hello from nested'}
    response = client.post(
        "/api/v1/comments/1",
        json=data,
        headers=headers
    )

    res = response.json()

    assert response.status_code == 200
    #assert 'comments' in res.keys()
    
    if res.get('comments'):
        assert res['comments'][0]['content'] == data.get('content')   
