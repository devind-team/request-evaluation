import aioschedule as schedule
from os import remove
from asyncio import get_event_loop
from sqlalchemy.future import select
from datetime import date, timedelta
from time import sleep
from generate_word.generate_file import create_report
from send_message.send_email import send_file
from database import engine
from models import Traffic
from settings import CONFIG_EMAIL


async def send_message():
    async with engine.connect() as session:
        get_record = (await session.execute(
            select(Traffic).
            where(Traffic.create_at == date.today() - timedelta(days=1)))).first()
    path_report = create_report(get_record.counter,
                                round(get_record.average_load, 2),
                                round(get_record.maximum_load, 2)
                                )
    await send_file(CONFIG_EMAIL['MAIL_FROM'],
                    CONFIG_EMAIL['MAIL_PASSWORD'],
                    CONFIG_EMAIL['MAIL_FROM'],
                    CONFIG_EMAIL['MAIL_TO'],
                    path_report,
                    CONFIG_EMAIL['MAIL_SERVER'],
                    CONFIG_EMAIL['MAIL_PORT']
                    )
    remove(path_report)
    sleep(1)

schedule.every().day.at('11:00').do(send_message)
# schedule.every(30).seconds.do(send_message)

while True:
    get_event_loop().run_until_complete(schedule.run_pending())
    sleep(1)
