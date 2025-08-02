from telegram.ext import CommandHandler
from keyboards.main_kb import main_keyboard


def start(update, context):
    update.message.reply_text(
        'Привет! Выберите действие:',
        reply_markup=main_keyboard()
    )


def register_start_handler(dp):
    dp.add_handler(CommandHandler('start', start))
