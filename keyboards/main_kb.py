from telegram import ReplyKeyboardMarkup


def main_keyboard():
    keyboard = [
        ['📋 Текущие параметры', '➕ Добавить параметры'],
        ['✏️ Редактировать параметры', '📈 Мой прогресс'],
        ['🗑️ Удалить все данные']
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
