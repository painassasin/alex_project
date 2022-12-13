import logging
from typing import Any

from faker import Faker
from pydantic import ValidationError
from requests import Response
from requests_tor import RequestsTor

from core import settings
from core.exceptions import ParseError
from one_win.models import Credentials, RegisterPayload, Request, ResponseData


logger = logging.getLogger('alex_project.one_win')


class OneWinController:

    def __init__(self, faker: Faker | None = None):
        self.faker = faker or Faker()

    def get_new_credentials(self) -> Credentials:
        return Credentials.get_faker_credentials(self.faker)

    def _get_request_data(self, creds: Credentials) -> Request:
        return Request(payload=RegisterPayload.create(creds, user_agent=self.faker.user_agent()))

    @staticmethod
    def _process_response(response: Response) -> ResponseData:
        if response.ok:
            response_data: dict[str, Any] = response.json()
            logger.debug('Response: %s', response_data)

            if 'data' in response_data:
                try:
                    return ResponseData.parse_obj(response_data['data'])
                except ValidationError as e:
                    logger.error('Failed to parse response due error: %s', e)
                    raise ParseError('Failed to parse response')

        logger.error('Failed to register user due error: %s', response.text)
        raise ParseError('Failed to register user')

    def register(self, rt: RequestsTor, credentials: Credentials | None = None) -> ResponseData:
        if not credentials:
            credentials = self.get_new_credentials()
        logger.debug('Try to register user with credentials: %s', credentials)

        request_data = self._get_request_data(credentials).dict(by_alias=True)
        logger.debug('Request data: %s', request_data)
        return self._process_response(response=rt.post(settings.ONE_WIN.URL, json=request_data))
