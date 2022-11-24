from datetime import datetime
from typing import TypeVar, Type

from faker import Faker
from pydantic import BaseModel, Field, validator

from core import settings

T1 = TypeVar('T1', bound='Credentials')
T2 = TypeVar('T2', bound='RegisterPayload')


class Credentials(BaseModel):
    phone_number: str
    email: str
    password: str

    @classmethod
    def get_faker_credentials(cls: Type[T1], faker: Faker) -> T1:
        return cls(
            phone_number='+7' + ''.join([i for i in faker.phone_number() if i.isdigit()])[-10:],
            email=faker.email(),
            password=faker.password(special_chars=False, length=12),
        )


class RegisterPayload(BaseModel):
    is_short: bool = Field(default=False, alias='isShort')
    name: str = '1win'
    birthday: int = 1099923325723
    country: str = 'ru'
    currency: str = 'RUB'
    phone: str
    email: str
    password: str
    repeat_password: str
    partner_key: str = 'fg12'
    timezone: str = 'Europe/Moscow'
    lang: str = 'ru'
    user_agent: str = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36')
    ad_group: str = Field(default='A1', alias='adGroup')

    @classmethod
    def create(cls: Type[T2], creds: Credentials, **kwargs) -> T2:
        return cls(
            phone=creds.phone_number,
            email=creds.email,
            password=creds.password,
            repeat_password=creds.password,
            partner_key=settings.ONE_WIN.PARTNER_KEY,
            **kwargs
        )

    class Config:
        allow_population_by_field_name = True


class Request(BaseModel):
    name: str = 'USER:auth-register'
    payload: RegisterPayload


class ResponseData(BaseModel):
    id: int
    email: str
    phone: str
    time_registration: datetime
    token: str
    user_id: int
    partner_key: str

    @validator('time_registration', pre=True)
    def convert_str_to_datetime(cls, value: str) -> datetime:
        if value.endswith('Z'):
            return datetime.fromisoformat(value[:-1])
        return datetime.fromisoformat(value)
