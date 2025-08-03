import os
import logging

from dotenv import load_dotenv
from telegram.ext import Updater

from handlers.start_handler import register_start_handler
from handlers.parameters_main_handler import register_parameters_handler
from user_data.user_data_storage import init_db


load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def main():
    print('Запуск бота...')
    init_db()
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    register_start_handler(dp)
    register_parameters_handler(dp)

    updater.start_polling()
    print('Бот успешно запущен!')
    updater.idle()


if __name__ == '__main__':
    main()
