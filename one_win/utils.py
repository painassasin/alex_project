import logging

from faker import Faker
from requests_tor import RequestsTor

from one_win.models import Credentials, RegisterPayload, Request
from settings import settings

rt = RequestsTor(tor_ports=(9050,), tor_cport=9051)
faker = Faker('ru-ru')

logger = logging.getLogger('alex_project.one_win')


def main():
    creds = Credentials.get_faker_credentials(faker)
    response_data = Request(payload=RegisterPayload.create(creds, user_agent=faker.user_agent()))

    r = rt.post(settings.ONE_WIN.URL, json=response_data.dict(by_alias=True))
    rt.new_id()
    assert r.ok
    logger.debug('Response: %s', r.json())
