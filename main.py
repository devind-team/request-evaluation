import asyncio
from fastapi import Depends, FastAPI
from fastapi.responses import RedirectResponse
from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from datetime import date
from database import get_session
from models import Traffic, TrafficCreate

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
    # await session.execute(update(Traffic).
    #                       where(Traffic.create_at == date.today()).
    #                       values(counter=Traffic.counter + 1))
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
