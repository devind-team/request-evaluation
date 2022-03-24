from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import date
from sqlalchemy import Date, Column


class TrafficBase(SQLModel):
    counter: int = Field(default=1)
    create_at: date = Field(sa_column=Column('create_at', Date, unique=True))


class Traffic(TrafficBase, table=True):
    id: int = Field(default=None, primary_key=True)


class TrafficCreate(TrafficBase):
    pass
