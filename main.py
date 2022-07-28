"""Конфигурация запросов проекта."""
from datetime import date

from fastapi import Depends, FastAPI, Form, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from database import get_session
from models import Email, Site, Traffic
from services.network_load import interest_calculation
from settings import SECRET_KEY

app = FastAPI()

origins = ['*']


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

templates = Jinja2Templates(directory='templates')


@app.get('/')
async def redirect_page_docs() -> RedirectResponse:
    """FastAPI - Swagger UI."""
    return RedirectResponse('/docs#/')


@app.post('/traffic/', response_model=Traffic)
async def calculate(identification: str, session: AsyncSession = Depends(get_session)):
    """Функция на принятие post запроса и обновления счетчика в базе данных."""
    site = (await session.execute(select(Site).where(Site.identification == identification))).first()[0]
    if site is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Запрашиваемый ключ доступа не найден')
    traffic = (await session.execute(select(Traffic).
                                     where(Traffic.site_id == site.id).
                                     where(Traffic.create_at == date.today()))).first()
    if traffic:
        await session.execute(update(Traffic).
                              where(Traffic.id == traffic[0].id).
                              values(id=traffic[0].id,
                                     counter=Traffic.counter+1,
                                     ))
        await session.commit()
        return traffic[0]
    network_load = interest_calculation()
    traffic_id = (await session.execute(insert(Traffic).values(
        counter=1,
        create_at=date.today(),
        site_id=site.id,
        average_load=network_load['average_load'],
        maximum_load=network_load['maximum_load'],
        ))).inserted_primary_key[0]
    await session.commit()
    return (await session.execute(select(Traffic).where(Traffic.id == traffic_id))).first()[0]


@app.get('/traffic/{token_access}', response_model=Site)
async def verify_token_access(token_access: str):
    if token_access == SECRET_KEY:
        return RedirectResponse('/identification_site/')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='У вас нет доступа к запрашиваемой странице')


@app.get('/identification_site/')
async def form_send(request: Request):
    return templates.TemplateResponse('post_identification.html', {'request': request})


@app.post('/identification/', response_model=Site)
async def generate_secret_key(
        website_url: str = Form(...),
        secret_key: str = Form(...),
        list_email: str = Form(...),
        session: AsyncSession = Depends(get_session)):
    verify_site = (await session.execute(select(Site).where(Site.site_name == website_url))).first()
    if verify_site is None:
        email_id = (await session.execute(insert(Email).values(name=list_email))).inserted_primary_key[0]
        await session.commit()
        site_id = (await session.execute(insert(Site).values(site_name=website_url,
                                                             identification=secret_key,
                                                             email_id=email_id))).inserted_primary_key[0]
        await session.commit()
        return JSONResponse(content=jsonable_encoder((await session.execute(select(Site).
                                                                            where(Site.id == site_id))).first()))
    return JSONResponse(content=jsonable_encoder((await session.execute(select(Site).
                                                                        where(Site.site_name == website_url))).first()))


@app.get('/info/{identification_site}', response_model=Traffic, response_class=HTMLResponse)
async def infi_traffic(identification_site: str, request: Request, session: AsyncSession = Depends(get_session)):
    site = (await session.execute(select(Site).where(Site.identification == identification_site))).first()[0]
    if site is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Запрашиваемый ключ доступа не найден')
    traffic_site = (await session.execute(select(Traffic).
                                          where(Traffic.site_id == site.id).
                                          where(Traffic.create_at == date.today()))).first()
    if traffic_site is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Мониторинг сайта {site.site_name} '
                                                                          f'за эту дату не производился')
    return templates.TemplateResponse(
        'statistics.html',
        {
            'request': request,
            'create_at': traffic_site[0].create_at,
            'counter': traffic_site[0].counter,
            'maximum_load': traffic_site[0].maximum_load,
            'average_load': traffic_site[0].average_load,
        }
    )
