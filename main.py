import asyncio
from fastapi import Depends, FastAPI
from fastapi.responses import RedirectResponse
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import date

from database import get_session
from models import Traffic

app = FastAPI()
counter = 0
lock = asyncio.Lock()


@app.get('/')
async def redirect_page_docs():
    return RedirectResponse('/docs#/')


@app.get('/traffic', response_model=list[Traffic])
async def calculate(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Traffic).where(Traffic.create_at == date.today()))
    results = result.scalars().first()
    print(results)



@app.get("/calculate")
async def calculate1():
    global counter

    async with lock:
        counter += 1

    return {'request': f'{counter}'}
