from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import date
from sqlalchemy import Date, Column


class TrafficBase(SQLModel):
    counter: int = Field(default=1, title='Количество запросов в день')
    minimum_load: float = Field(nullable=True, title='Минимальная нагрузка на сеть за день')
    average_load: float = Field(nullable=True, title='Средняя нагрузка на сеть за день')
    create_at: date = Field(sa_column=Column('create_at', Date, unique=True), title='Дата')


class Traffic(TrafficBase, table=True):
    id: int = Field(default=None, primary_key=True)


class TrafficCreate(TrafficBase):
    pass
