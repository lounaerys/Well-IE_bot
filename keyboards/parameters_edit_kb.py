from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def parameters_edit_keyboard():
    keyboard = [
        [
            InlineKeyboardButton('Вес', callback_data='edit_weight'),
            InlineKeyboardButton('Объем ягодиц', callback_data='edit_hips'),
        ],
        [
            InlineKeyboardButton('Объем бедра', callback_data='edit_thigh'),
            InlineKeyboardButton('Объем талии', callback_data='edit_waist'),
        ],
        [
            InlineKeyboardButton('Объем груди', callback_data='edit_chest'),
            InlineKeyboardButton('Объем бицепса', callback_data='edit_biceps'),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)
