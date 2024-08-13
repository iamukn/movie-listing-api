#!/usr/bin/python3
from fastapi import FastAPI, Depends, HTTPException, status
from db.users_model import User, session
from db.movies_model import Movie, Comment, Rating, movie_session
from schemas.schemas import (
        Login, User_data, Token,
        MovieValidate, MovieUpdate, 
        RatingValidator, CommentsValidator
        )
from sqlalchemy.exc import IntegrityError
from utils.hash_verify import verify_password, hash_password
import uvicorn
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from auth.jwt_utils import create_access_token, verify_token
from db.utils.movies_utils import get_movie, get_all_movies, update_movie, delete_movie, get_comment
from auth.get_user import get_user
from logger.log_conf.log_conf import logger



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    return payload

# instance of fastAPI
app = FastAPI()


""" Endpoint for user registration """
@app.post('/api/v1/signup')
@app.post('/api/v1/signup/')
async def signup(user: User_data):
    # check if user data was received
    if user:
       # hash the password
       new_user = user.dict()
       hash_pwd = hash_password(user.password)
       new_user['password'] = hash_pwd
       
       # add the user to the database
       try:
           session.add(User(**new_user))
           session.commit()
           new_user.pop('password')
           new_user['status_code'] = 201
           logger.info(f'{new_user.get("email")} was successfully registered!')
           return new_user
       except IntegrityError as e:
           session.rollback()
           logger.info(f'Registration denied! User with the  {new_user.get("email")} already exist!')

           raise HTTPException(status_code=400, detail="Email address already exists")

# Json web token generation for authentication
@app.post('/api/v1/auth/token', response_model=Token)
@app.post('/api/v1/auth/token/', response_model=Token)
async def login(user: Login):
    if user:
        # get user
        user_in_db = get_user(user.email)
        if user_in_db:
            verify = verify_password(user.password, user_in_db.password)
            if verify:
                access_token = create_access_token(data={"email": user_in_db.email})
                logger.info(user.email + ' logged in!')
                return {'access_token': access_token, 'token_type': 'bearer', 'status': status.HTTP_200_OK}
    logger.info(f"User {user.email} does not exist!")
    return {'access_token': 'None', 'token_type': 'None', 'status': status.HTTP_404_NOT_FOUND}


""" Movies Endpoint """
# Add a movie

@app.post('/api/v1/movies')
@app.post('/api/v1/movies/')
async def add_movie(movie_data: MovieValidate, current_user: dict = Depends(get_current_user)):
    movie_data = movie_data.dict()
    movie_data['created_by'] = current_user.get('email')
    # create a new movie
    try:
        movie = Movie(title=movie_data['title'], release_date=movie_data['release_date'], genre=movie_data['genre'], created_by=movie_data['created_by'])
        movie_session.add(movie)
        movie_session.commit()
        return movie_data

    except IntegrityError as e:
        movie_session.rollback()
        logger.info(f"An error occurred while creating a movie by {current_user.get('email')}!")
        raise HttpException(
                status_code=400,
                detail='Bad request'
                )


@app.put('/api/v1/movies/{id:int}')
@app.put('/api/v1/movies/{id:int}/')
async def movie_update(id: int, movie_data: MovieUpdate, current_user: dict = Depends(get_current_user)):
    updated = update_movie(id,  movie_data.dict(), current_user.get('email'))
    if updated:
        return {'movie': updated, 'status': status.HTTP_206_PARTIAL_CONTENT}
    return {'status': status.HTTP_400_BAD_REQUEST}

# GET all movies
@app.get('/api/v1/movies')
@app.get('/api/v1/movies/')
async def movies():
    movies = get_all_movies()
    return {'movies': movies}

# GET a movie
@app.get('/api/v1/movies/{id:int}')
@app.get('/api/v1/movies/{id:int}/')
async def get_a_movie(id: int):
    movie = get_movie(id)
    return {'movie': movie}

# DELETE a movie
@app.delete('/api/v1/movies/{id:int}')
@app.delete('/api/v1/movies/{id:int}/')
async def drop_movie(id: int, current_user: dict = Depends(get_current_user)):
    deleted = delete_movie(id, current_user.get('email'))

    if deleted:
        logger.info("{current_user.get('email')} deleted movie with id {id}")
        return {'status': status.HTTP_204_NO_CONTENT}
    return {'status': status.HTTP_400_BAD_REQUEST}

# Rating routes

@app.post('/api/v1/movies/{id:int}/ratings/')
@app.post('/api/v1/movies/{id:int}/ratings')
async def rating(ratings: RatingValidator, id: int, current_user: dict = Depends(get_current_user)):
    # rate a movie
    ratings = ratings.dict()
    score = ratings.get('score')
    rated_by = current_user.get('email')

    if (score >= 0 and score <= 5) and rated_by:
        try:
            # get a movie
            movie = get_movie(id)
            if movie:
                rate = Rating(score=score, rated_by=rated_by, movie=movie)
                movie_session.add(rate)
                movie_session.commit()
                return {'status_code': 201, 'rating': score}
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "NOT FOUND"
            )
        except IntegrityError as e:
            return "You've rated this movie!"

        except Exception as e:
            if e.status_code == status.HTTP_404_NOT_FOUND:
                logger.info(e.detail)
                return {'detail': 'Movie NOT FOUND', 'status_code': 404}
            logger.info(e)
            return {'detail': "An internal error occurred!", 'status_code': 500}


@app.get('/api/v1/movies/{id:int}/ratings')
@app.get('/api/v1/movies/{id:int}/ratings/')
async def get_ratings(id: int):

    try:
        movie = get_movie(id)
        if movie:
            rating = movie.ratings
            return {'ratings': rating}

        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "NOT FOUND"
                )
    except Exception as e:
        if e.status_code == status.HTTP_404_NOT_FOUND:
            logger.info(f'Movie with id {id} NOT FOUND')
            return {'status': e.status_code, 'detail': e.detail}
        logger.info(e.detail)
        return "An internal error occurred!"

""" Comments route """
# Add a comment to a movie
@app.post('/api/v1/movies/{id:int}/comments')
@app.post('/api/v1/movies/{id:int}/comments/')
async def comments(comment_data: CommentsValidator, id: int, current_user: dict= Depends(get_current_user)):
    # fetch a movie
    try:
        movie = get_movie(id)

        if movie:
            comment_data = comment_data.dict()
            content = comment_data.get('content')
            commenter = current_user.get('email')
            comment = Comment(content=content, commenter=commenter, movie=movie)

            movie_session.add(comment)
            movie_session.commit()
            return {'comment': comment_data}

        raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "NOT FOUND"
            )
    except Exception as e:
        if e.status_code == status.HTTP_404_NOT_FOUND:
            return {'status_code': e.status_code, 'detail': e.detail}
        logger.info(e.detail)
        return "An internal error occurred!"

# Fetch all comments linked to a movie
@app.get('/api/v1/movies/{id:int}/comments')
@app.get('/api/v1/movies/{id:int}/comments/')
async def get_comments(id: int):
    try:
        movie = get_movie(id)
        if movie:
            return movie.comments
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "NOT FOUND"
                )
    except Exception as e:
        if e.status_code == status.HTTP_404_NOT_FOUND:
            return {'status_code': e.status_code, 'detail': e.detail}
        return "An internal error occurred!"

# Nested comments
@app.post('/api/v1/comments/{id:int}')
@app.post('/api/v1/comments/{id:int}/')
async def nested_comments(comment_data: CommentsValidator, id: int, current_user: dict = Depends(get_current_user)):
    try:
        comment = get_comment(id)
        if comment:
            nested = Comment(content=comment_data.content, commenter=current_user.get('email'), movie=comment.movie, parent=comment)

            movie_session.add(nested)
            movie_session.commit()
            movie_session.refresh(comment)
            return {'comments': comment.replies}
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "NOT FOUND"
                )
    except Exception as e:
        if e.status_code == status.HTTP_404_NOT_FOUND:
            return {'status': e.status_code}
        return "An internal error occurred!"

""" Fetch comments and nested comments 
@app.get('/api/v1/comments/')
async def fetch_all_comments():
    comment = movie_session.query(Comment).filter(Comment.parent_id == None).first()
    nested = movie_session.query(Comment).filter(Comment.movie_id==comment.movie_id, Comment.parent_id != None).all()
    return {'comment': comment, 'nested': nested}

@app.get('/api/v1/comments/nested/')
async def fetch_nested_comments():
    comment = movie_session.query(Comment).filter(Comment.id == 2).first()
    nested = movie_session.query(Comment).filter(Comment.parent_id==2).all()
    return {'comment': comment, 'nested': nested}
"""
# dunder
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True, log_level="debug")
