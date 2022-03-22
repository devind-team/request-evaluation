from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import date


class TrafficBase(SQLModel):
    request: str
    create_at: date


class Traffic(TrafficBase, table=True):
    id: int = Field(default=None, primary_key=True)
