#!/usr/bin/env python3
"""Base authentication"""

from models import storage
from models.users import User
from models.sessions import Session
from bcrypt import hashpw, gensalt
from uuid import uuid4
from datetime import datetime, timedelta

def _hash_pwd(password: str) -> bytes:
    """returns hashed password"""
    return hashpw(password.encode('utf-8'), gensalt())

def _gen_string() -> str:
    """returns a uuid string"""
    return str(uuid4())


class Auth:
    """Base auth"""
    def register_user(self, email: str, name: str, password: str) -> User:
        """register user"""
        user = storage.get_by(User, email=email)
        if user:
            raise ValueError(f"User {email} already exist")
        new_user = User(email, name, _hash_pwd(password))
        new_user.save()

    def check_login(self, email: str, password: str) -> bool:
        """check for valid login"""    
        user = storage.get_by(User, email=email)
        if user:
            return _hash_pwd(password) == user.password_hash
        return False

    def create_session(self, email: str) -> str:
        """Creates a session from the user email"""
        user = storage.get_by(User, email=email)
        if not user:
            return None
        session = Session(user.id)
        session.save()
        return session.id
    
    def get_user_from_session_id(self, session_id: str) -> User:
        """get user from session id"""
        if not session_id:
            return None
        session = storage.get(Session, session_id)
        if not session:
            return None
        user = storage.get(User, session.user_id)
        if not user:
            return None
        return user.to_dict()
    
    def destroy_session(self, session_id: int) -> None:
        """destroy session"""
        if not session_id:
            return None
        session = storage.get(Session, session_id)
        if not session:
            return None
        return session.delete()
    
    def is_session_valid(self, session_id: str) -> bool:
        """check if session is expired"""
        if not session_id:
            return False
        session = storage.get(Session, session_id)
        if not session:
            return False
        tim = session.created_at + timedelta(hours=Session.SESSION_DURATION)
        if tim < datetime.now():
            return True
        return False
