#!/usr/bin/env python3
"""Membership plans"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from .base import Base, BaseModel


class MembershipPlan(BaseModel ,Base):
    """Membership plan"""
    __tablename__ = "membership_plans"
    name = Column(String(60), nullable=False)
    price = Column(String(60), nullable=False)
    features = Column(Text)
    description = Column(String())
    user = relationship('User', back_populates='membership_plan')

    def __repr__(self):
        return f"<Membership plan> - {self.name}"
