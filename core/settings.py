from pathlib import Path

from pydantic import BaseSettings, HttpUrl

BASE_DIR = Path(__file__).resolve().parent.parent


class AppSettings(BaseSettings):
    BASE_DIR: Path = BASE_DIR

    class Config:
        env_file = BASE_DIR.joinpath('.env')
        env_file_encoding = 'utf-8'


class OneWinSettings(AppSettings):
    URL: HttpUrl = 'https://1wyxza.top/microservice/ask'
    PARTNER_KEY: str

    class Config:
        env_prefix = 'ONE_WIN_'


class Settings(AppSettings):
    BOT_TOKEN: str
    DEBUG: bool = False
    ONE_WIN: OneWinSettings = OneWinSettings()


settings = Settings()
