"""Задача, которая отправляет отчет на email."""
from asyncio import get_event_loop
from datetime import date, timedelta
from os import remove
from time import sleep

import aioschedule as schedule
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker

from database import engine # noqa
from models import Email, Site, Traffic
from services.generate_word import create_report
from services.send_email import generate_message
from settings import CONFIG_EMAIL, NOTIFICATION_SEND_TIME


async def send_message() -> None:
    """Функция отправки письма по email."""
    async with sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)() as session:
        get_records = (await session.execute(select(Traffic).
                                             where(Traffic.create_at == date.today() - timedelta(days=1)))).all()
        for get_record in get_records:
            site = (await session.execute(select(Site).
                                          where(Site.id == get_record[0].site_id))).first()
            email_to = (await session.execute(select(Email).
                                              where(Email.id == site[0].email_id))).first()[0].name
            path_report = create_report(get_record[0].counter,
                                        get_record[0].average_load,
                                        get_record[0].maximum_load,
                                        site[0].site_name)
            await generate_message(
                CONFIG_EMAIL['MAIL_FROM'],
                CONFIG_EMAIL['MAIL_PASSWORD'],
                CONFIG_EMAIL['MAIL_FROM'],
                email_to,
                path_report,
                CONFIG_EMAIL['MAIL_SERVER'],
                CONFIG_EMAIL['MAIL_PORT'],
                site[0].site_name
            )
            remove(path_report)
            sleep(1)


schedule.every().day.at(f'{NOTIFICATION_SEND_TIME}').do(send_message)
# schedule.every(20).seconds.do(send_message) # noqa

while True:
    get_event_loop().run_until_complete(schedule.run_pending())
    sleep(1)
