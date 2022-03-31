from os.path import join
from settings import get_settings
from docxtpl import DocxTemplate
from datetime import date, timedelta
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from models import Traffic
from fastapi import Depends


async def create_report(traffic: Traffic, session: AsyncSession = Depends(get_session)):
    template_word = DocxTemplate(join(get_settings().template_dir, 'report.docx'))
    template_word.render(
        {
            'date': f'{date.today().day}.{date.today().month}.{date.today().year}',
            'counter': (await session.execute(
                select(traffic).
                    where(traffic.create_at == date.today()-timedelta(days=1)))
                        ).scalar().counter
        }
    )
    await template_word.save(join(get_settings().static_dir, f'{date.today()}.docx'))
