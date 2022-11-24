import logging

from faker import Faker
from requests_tor import RequestsTor

from core import settings
from core.exceptions import BadRequest, ParseError
from one_win.models import Credentials, Request, RegisterPayload, ResponseData

logger = logging.getLogger('alex_project.one_win')


class OneWinController:

    def __init__(self, rt: RequestsTor, faker: Faker = Faker()):
        self.faker = faker
        self.rt = rt

    @property
    def request_data(self) -> dict:
        creds = Credentials.get_faker_credentials(self.faker)
        request_data = Request(payload=RegisterPayload.create(creds, user_agent=self.faker.user_agent()))
        return request_data.dict(by_alias=True)

    def register(self):
        response = self.rt.post(settings.ONE_WIN.URL, json=self.request_data)
        if response.ok:
            response_data: dict = response.json()
            logger.debug('Response: %s', response_data)
            if 'data' in response_data:
                if 'id' in response_data['data']:
                    return ResponseData.parse_obj(response_data['data'])
                if 'status' in response_data['data']:
                    if response_data['data']['status'] == 400:
                        logger.info('Failed to register user due error: %s', response_data)
                        raise BadRequest(response_data['data'].get('message'))
        logger.error('Failed to register user due error: %s', response.text)
        raise ParseError
