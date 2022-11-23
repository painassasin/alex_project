from pydantic import BaseSettings, HttpUrl


class AppSettings(BaseSettings):
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class OneWinSettings(AppSettings):
    URL: HttpUrl = 'https://1wyxza.top/microservice/ask'


class Settings(AppSettings):
    BOT_TOKEN: str
    DEBUG: bool = False
    ONE_WIN: OneWinSettings = OneWinSettings()


settings = Settings()
