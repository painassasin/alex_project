import logging

from faker import Faker
from requests_tor import RequestsTor

from core import settings
from core.exceptions import BadRequest, ParseError
from one_win.models import Credentials, RegisterPayload, Request, ResponseData


logger = logging.getLogger('alex_project.one_win')


class OneWinController:

    def __init__(self, rt: RequestsTor, faker: Faker = Faker()):
        self.faker = faker
        self.rt = rt
        self._credentials: Credentials | None = None

    @property
    def credentials(self) -> Credentials:
        if not self._credentials:
            raise ValueError('Credentials does not set')
        return self._credentials

    @credentials.setter
    def credentials(self, value: Credentials):
        self._credentials = value

    @property
    def request_data(self) -> dict:
        self.credentials = Credentials.get_faker_credentials(self.faker)
        request_data = Request(payload=RegisterPayload.create(self.credentials, user_agent=self.faker.user_agent()))
        return request_data.dict(by_alias=True)

    def register(self) -> tuple[Credentials, ResponseData]:
        response = self.rt.post(settings.ONE_WIN.URL, json=self.request_data)
        if response.ok:
            response_data: dict = response.json()
            logger.debug('Response: %s', response_data)
            if 'data' in response_data:
                if 'id' in response_data['data']:
                    return self.credentials, ResponseData.parse_obj(response_data['data'])
                if 'status' in response_data['data']:
                    if response_data['data']['status'] == 400:
                        logger.info('Failed to register user due error: %s', response_data)
                        raise BadRequest(response_data['data'].get('message'))
        logger.error('Failed to register user due error: %s', response.text)
        raise ParseError
