import os
from typing import Dict
from os.path import join
from pathlib import Path
from functools import lru_cache
from pydantic import BaseSettings
from dotenv import load_dotenv

BASE_DIR: Path = Path(__file__).resolve(strict=False).parent
load_dotenv(dotenv_path=join(BASE_DIR, '.env'))

CONFIG_EMAIL = {
    'MAIL_USERNAME': os.getenv('EMAIL_USERNAME'),
    'MAIL_PASSWORD': os.getenv('EMAIL_PASSWORD'),
    'MAIL_FROM': os.getenv('EMAIL_FROM'),
    'MAIL_TO': os.getenv('EMAIL_TO'),
    'MAIL_PORT': os.getenv('EMAIL_PORT'),
    'MAIL_SERVER': os.getenv('EMAIL_SERVER')
}
MAIL_TO = os.getenv('EMAIL_TO')
NOTIFICATION_SEND_TIME = os.getenv('NOTIFICATION_SEND_TIME')
SECRET_KEY = os.getenv('SECRET_KEY')


class Settings(BaseSettings):
    base_dir: Path = BASE_DIR
    template_dir: Path = join(BASE_DIR, 'templates')
    static_dir: Path = join(BASE_DIR, 'static')

    database: Dict[str, str] = {key: os.getenv(key) for key in ('DB_SERVICE',
                                                                'DB_USER',
                                                                'DB_PASS',
                                                                'DB_HOST',
                                                                'DB_PORT',
                                                                'DB_NAME')}

    @property
    def db_sync_connections(self) -> str:
        return '%s://%s:%s@%s:%s/%s' % (
            self.database['DB_SERVICE'],
            self.database['DB_USER'],
            self.database['DB_PASS'],
            self.database['DB_HOST'],
            self.database['DB_PORT'],
            self.database['DB_NAME']
        )


@lru_cache()
def get_settings():
    return Settings()
