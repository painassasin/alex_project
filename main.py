import logging

import one_win.utils
from settings import settings

logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format='%(asctime)s %(name)s %(levelname)s %(message)s'
)
logging.getLogger('stem').setLevel(logging.WARNING)
logging.getLogger('socks').setLevel(logging.INFO)

if __name__ == '__main__':
    one_win.utils.main()
