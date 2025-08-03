from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def progress_keyboard():
    keyboard = [
        [
            InlineKeyboardButton('Вес', callback_data='progress_weight'),
            InlineKeyboardButton('Объем ягодиц', callback_data='progress_hips')
        ],
        [
            InlineKeyboardButton('Объем бедра', callback_data='progress_thigh'),
            InlineKeyboardButton('Объем талии', callback_data='progress_waist')
        ],
        [
            InlineKeyboardButton('Объем груди', callback_data='progress_chest'),
            InlineKeyboardButton('Объем бицепса', callback_data='progress_biceps')
        ],
        [
            InlineKeyboardButton('📊 Общий прогресс', callback_data='progress_overall')
        ],
    ]
    return InlineKeyboardMarkup(keyboard)
