#!/usr/bin/env python3
"""Gym user model"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, BLOB, ForeignKey, Boolean
from .base import BaseModel, Base
from .sessions import Session


class User(BaseModel, Base):
    """user model"""
    __tablename__ = "users"
    email = Column(String(60), nullable=False, unique=True)
    password_hash = Column(String(60), nullable=False)
    name = Column(String(60), nullable=False)
    picture = Column(BLOB)
    is_verified = Column(Boolean)
    membership_plan_id = Column(String(60), ForeignKey('membership_plans.id'))
    reset_token = Column(String())
    membership_plan = relationship('MembershipPlan', back_populates='user')
    session = relationship('Session', backref='user', uselist=False)

    def __repr__(self):
        return f"<User> - {self.name} - {self.email}"
