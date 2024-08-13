#!/usr/bin/python3
from db.users_model import User, session

# fetches a user
def get_user(email):
    # check if email is giveb
    if email:
        # get user 
        user = session.query(User).filter_by(email=email).first()
        if user:
            return user

    return False
