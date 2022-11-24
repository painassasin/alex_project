import logging

from faker import Faker
from requests_tor import RequestsTor

from core import settings
from core.exceptions import BaseAppException
from one_win.controller import OneWinController

logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format='%(asctime)s %(name)s %(levelname)s %(message)s'
)
logging.getLogger('stem').setLevel(logging.WARNING)
logging.getLogger('socks').setLevel(logging.INFO)
logging.getLogger('faker.factory').setLevel(logging.INFO)

rt = RequestsTor(tor_ports=(9050,), tor_cport=9051, autochange_id=1)
faker = Faker()

if __name__ == '__main__':
    try:
        result_1 = OneWinController(rt=rt, faker=faker).register()
        print()
    except BaseAppException as err:
        logging.error(err)
