from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def delete_confirm_keyboard():
    keyboard = [
        [
            InlineKeyboardButton('Да, удалить всё', callback_data='delete_confirm_yes'),
            InlineKeyboardButton('Отмена', callback_data='delete_confirm_no')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
