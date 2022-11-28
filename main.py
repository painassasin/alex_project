import logging

import telebot
from faker import Faker
from requests_tor import RequestsTor
from telebot import custom_filters
from telebot.types import Message

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
logging.getLogger('urllib3.connectionpool').setLevel(logging.INFO)

logger = logging.getLogger('alex_project.main')
faker = Faker('ru_RU')
one_win_controller = OneWinController(faker)
rt = RequestsTor(tor_ports=(9050,), tor_cport=9051, autochange_id=1)
bot = telebot.TeleBot(settings.TG.BOT_TOKEN)


@bot.message_handler(commands=['chat_id'])
def get_chat_id(message: Message):
    bot.send_message(chat_id=message.chat.id, text=str(message.from_user.id))


@bot.message_handler(chat_id=settings.TG.ADMIN_IDS, commands=['one_win'])
def create_one_win_user(message: Message):
    creds = one_win_controller.get_new_credentials()
    try:
        response = one_win_controller.register(rt=rt, credentials=creds)
    except BaseAppException as err:
        logger.error(err)
        bot.send_message(chat_id=message.chat.id, text='Failed to create user. Please try again.')
    else:
        logger.info('User created for one_win: %s', response.dict())
        bot.send_message(chat_id=message.chat.id, text=creds.as_text())


bot.add_custom_filter(custom_filters.ChatFilter())

if __name__ == '__main__':
    logger.info('Start pooling')
    bot.infinity_polling()
