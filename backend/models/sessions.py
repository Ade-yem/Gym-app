#!/usr/bin/env python3
"""Model for sessions"""

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, BaseModel


class Session(Base, BaseModel):
    """Sessions model"""
    __tablename__ = 'sessions'
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    # user = relationship('User', back_populates='session')
