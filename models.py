"""Модели проекта."""
from datetime import date
from typing import Optional

from sqlalchemy import Column, String
from sqlmodel import Field, SQLModel


class TrafficBase(SQLModel):
    """Базовая модель Traffic."""

    counter: int = Field(default=1, title='Количество запросов в день')
    average_load: Optional[float] = Field(default=0, nullable=False, title='Средняя нагрузка на сеть за день')
    maximum_load: Optional[float] = Field(default=0, nullable=False, title='Максимальная нагрузка на сеть за день')
    create_at: date = Field(nullable=False, title='Дата')
    site_id: int = Field(default=None, foreign_key='site.id', nullable=False)


class Traffic(TrafficBase, table=True):
    """Модель Traffic."""

    id: int = Field(default=None, primary_key=True)  # noqa


class SiteBase(SQLModel):
    """Базовая модель Site."""

    identification: str = Field(
        sa_column=Column('identification', String, unique=True, nullable=False),
        title='Индентификатор сайта'
    )
    site_name: str = Field(sa_column=Column('site_name', String, unique=True, nullable=False), title='URL сайта')
    email_id: int = Field(default=None, foreign_key='email.id', nullable=False)


class Site(SiteBase, table=True):
    """Модель Site."""

    id: int = Field(default=None, primary_key=True)  # noqa


class EmailBase(SQLModel):
    """Базовая модель Email."""

    name: str = Field(nullable=False, title='Список email')


class Email(EmailBase, table=True):
    """Модель Email."""

    id: int = Field(default=None, primary_key=True)  # noqa
