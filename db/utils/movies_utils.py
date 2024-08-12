#!/usr/bin/python3
from db.movies_model import Movie, movie_session, Comment

# fetch all movies
def get_all_movies():
    return movie_session.query(Movie).all()

# fetch a movie
def get_movie(id: int):
    movie = movie_session.query(Movie).filter_by(id=id).first()
    return movie

# update movie
def update_movie(id, movie_data, user_email):
    movie = get_movie(id)
    title = movie_data.get('title')
    genre = movie_data.get('genre')
    release_date = movie_data.get('release_date')

     # check if the movie exists
    if not movie or movie.created_by != user_email:
        return False
    
    if title:
        movie.title = title
    
    if genre:
        movie.genre = genre

    if release_date:
        movie.release_date = release_date

    movie_session.commit()
    movie_session.refresh(movie)
    return movie

# delete a movie
def delete_movie(id, user_email):
    try:
        movie = get_movie(id)
        # check if the movie was created by the current user
        if not movie or movie.created_by != user_email:
            return False

        movie_session.delete(movie)
        movie_session.commit()
        return True
    except Exception as e:
        print(e)
        raise ValueError

def get_comment(id: int):
    comment = movie_session.query(Comment).filter_by(id=id).first()
    return comment
