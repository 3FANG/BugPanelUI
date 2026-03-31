from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    account_id: int
    nickname: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    account_id: int
    nickname: str
    created_at: datetime


class ReportCreate(BaseModel):
    account_id: int
    title: str
    text: str


class ReportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    account_id: int
    title: str
    text: str
    created_at: datetime
