#!/usr/bin/python3

from sqlalchemy import create_engine, Column, Date, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
import datetime

# base instance used in creating the database models
Base = declarative_base()


class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    created_by = Column(String, nullable=False)
    comments = relationship('Comment', back_populates='movie')
    ratings = relationship('Rating', back_populates='movie')

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    commenter = Column(String, nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    movie = relationship('Movie', back_populates='comments')
    # Self-referential relationship for nested comments
    parent_id = Column(Integer, ForeignKey('comments.id'), nullable=True)
    parent = relationship('Comment', remote_side=[id], back_populates='replies')
    replies = relationship('Comment', back_populates='parent', cascade="all, delete-orphan")


class Rating(Base):
    __tablename__ = 'ratings'
    id = Column(Integer, primary_key=True)
    score = Column(Integer, nullable=False)
    rated_by = Column(String, nullable=False, unique=True)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    movie = relationship('Movie', back_populates='ratings')

# Create an SQLite database
engine = create_engine('sqlite:///movies_collection.db')
Base.metadata.create_all(engine)

# Create a new session
Session = sessionmaker(bind=engine)
movie_session = Session()

"""
# Add sample data
movie1 = Movie(title='Movie 1', created_by='ukn@gmail.com', genre='Drama', release_date = '1993-12-12')
comment1 = Comment(content='Great movie!',commenter='ukn@gmail.com', movie=movie1)
rating1 = Rating(score=5, movie=movie1, rated_by='ukn@gmail.com')

movie_session.add(movie1)
movie_session.add(comment1)
movie_session.add(rating1)
movie_session.commit()
"""
