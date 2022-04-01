from fastapi import Depends, FastAPI
from fastapi.responses import RedirectResponse
from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from datetime import date, timedelta
from database import get_session
from models import Traffic, TrafficCreate
from generate_word.generate_file import create_report
from send_message.send_email import send_file
from settings import CONFIG_EMAIL
from os import remove

app = FastAPI()


@app.get('/')
async def redirect_page_docs():
    return RedirectResponse('/docs#/')


@app.get('/traffic',
         response_model=list[Traffic])
async def calculate(session: AsyncSession = Depends(get_session)):

    insert_records = insert(Traffic).values(counter=1,
                                            create_at=date.today())
    update_records = insert_records.on_conflict_do_update(constraint='traffic_create_at_key',
                                                          set_=dict(counter=Traffic.counter + 1))
    await session.execute(update_records)
    await session.execute(update(Traffic).
                          where(Traffic.create_at == date.today()).
                          values(average_load=Traffic.counter * 0.0184,
                                 maximum_load=Traffic.counter * 0.0305,
                                 ))
    await session.commit()


@app.post('/traffic')
async def add_traffic(traffic: TrafficCreate,
                      session: AsyncSession = Depends(get_session)):
    traffic = Traffic(counter=traffic.counter,
                      create_at=traffic.create_at)
    session.add(traffic)
    await session.commit()
    await session.refresh(traffic)
    return traffic


@app.get('/email',
         response_model=list[Traffic])
async def send_message(session: AsyncSession = Depends(get_session)):
    get_record = (await session.execute(
        select(Traffic).
        where(Traffic.create_at == date.today() - timedelta(days=1)))).scalar()
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
