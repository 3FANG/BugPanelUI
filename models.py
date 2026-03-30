from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy import Column, BigInteger, Integer, String, DateTime, ForeignKey, UniqueConstraint

from app.database import Base


class User(Base):
    __tablename__ = "users"

    account_id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(50), unique=True)
    created_at = Column(DateTime, default=datetime.now)
    last_seen_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    tree_cuts = relationship('TreeCut', back_populates='user')


class Battle(Base):
    __tablename__ = 'battles'

    arena_unique_id = Column(BigInteger, primary_key=True)
    battle_time = Column(DateTime, nullable=True)
    map_name = Column(String(100), nullable=True)
    battle_type = Column(Integer, nullable=True)  # Например, random, clan

    tree_cuts = relationship('TreeCut', back_populates='battle')


class TreeCut(Base):
    __tablename__ = 'trees_cuts'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('users.account_id'), nullable=False)
    arena_unique_id = Column(BigInteger, ForeignKey('battles.arena_unique_id'), nullable=False)
    trees_cut = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.now)

    __table_args__ = (UniqueConstraint('account_id', 'arena_unique_id', name='uq_account_arena'),)

    user = relationship('User', back_populates='tree_cuts')
    battle = relationship('Battle', back_populates='tree_cuts')
