from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import date
from sqlalchemy import Date, Column


class TrafficBase(SQLModel):
    counter: int = Field(default=1, title='Количество запросов в день')
    average_load: Optional[float] = Field(title='Средняя нагрузка на сеть за день')
    maximum_load: Optional[float] = Field(title='Максимальная нагрузка на сеть за день')
    create_at: date = Field(title='Дата')
    site_id: int = Field(default=None, foreign_key='site.id')


class Traffic(TrafficBase, table=True):
    id: int = Field(default=None, primary_key=True)


class TrafficCreate(TrafficBase):
    pass


class SiteBase(SQLModel):
    # identification: str = Field(sa_column=Column('identification', unique=True), title='Индентификатор сайта')
    # site_name: str = Field(sa_column=Column('site_name', unique=True), title='URL сайта')
    identification: str = Field(title='Индентификатор сайта')
    site_name: str = Field(title='URL сайта')


class Site(SiteBase, table=True):
    id: int = Field(default=None, primary_key=True)
