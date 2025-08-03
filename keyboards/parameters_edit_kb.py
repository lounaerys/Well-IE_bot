from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def parameters_edit_keyboard():
    keyboard = [
        [
            InlineKeyboardButton('Вес', callback_data='edit_weight'),
            InlineKeyboardButton('Обхват ягодиц', callback_data='edit_hips'),
        ],
        [
            InlineKeyboardButton('Обхват бедра', callback_data='edit_thigh'),
            InlineKeyboardButton('Обхват талии', callback_data='edit_waist'),
        ],
        [
            InlineKeyboardButton('Обхват груди', callback_data='edit_chest'),
            InlineKeyboardButton('Обхват бицепса', callback_data='edit_biceps'),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)
