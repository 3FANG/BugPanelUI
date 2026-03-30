from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text

from app.database import Base


class User(Base):
    __tablename__ = "users"

    account_id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(50), unique=True)
    created_at = Column(DateTime, default=datetime.now)

    reports = relationship("Report", back_populates="user")


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey('users.account_id'), nullable=False, index=True)
    
    title = Column(String(200), nullable=False)
    text = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="reports")