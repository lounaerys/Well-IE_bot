from telegram.ext import ConversationHandler
from user_data.user_data_storage import create_or_update_user, add_new_log_entry
from keyboards.main_kb import main_keyboard
from handlers.parameters_states import WEIGHT_ADD, HIPS_ADD, THIGH_ADD, WAIST_ADD, CHEST_ADD, BICEPS_ADD


MAIN_MENU_BUTTONS = [
    '📋 Текущие параметры',
    '➕ Добавить параметры',
    '✏️ Редактировать параметры',
    '📈 Мой прогресс',
    '🗑️ Удалить все данные'
]


def handle_cancel_during_add(update, context):
    update.message.reply_text(
        'Операция добавления отменена, данные не сохранены.',
        reply_markup=main_keyboard()
    )
    from handlers.parameters_main_handler import text_message_handler
    return text_message_handler(update, context)


def parse_float(value):
    try:
        return float(value.replace(',', '.'))
    except Exception:
        raise ValueError('Неверный формат числа')


def add_params_start(update, context):
    update.message.reply_text('Введите ваш вес (кг):')
    return WEIGHT_ADD


def add_weight(update, context):
    if update.message.text in MAIN_MENU_BUTTONS:
        return handle_cancel_during_add(update, context)
    try:
        context.user_data['weight'] = parse_float(update.message.text)
    except ValueError:
        update.message.reply_text('Пожалуйста, введите число.')
        return WEIGHT_ADD
    update.message.reply_text('Введите обхват ягодиц (см):')
    return HIPS_ADD


def add_hips(update, context):
    if update.message.text in MAIN_MENU_BUTTONS:
        return handle_cancel_during_add(update, context)
    try:
        context.user_data['hips'] = parse_float(update.message.text)
    except ValueError:
        update.message.reply_text('Пожалуйста, введите число.')
        return HIPS_ADD
    update.message.reply_text('Введите обхват бедра (см):')
    return THIGH_ADD


def add_thigh(update, context):
    if update.message.text in MAIN_MENU_BUTTONS:
        return handle_cancel_during_add(update, context)
    try:
        context.user_data['thigh'] = parse_float(update.message.text)
    except ValueError:
        update.message.reply_text('Пожалуйста, введите число.')
        return THIGH_ADD
    update.message.reply_text('Введите обхват талии (см):')
    return WAIST_ADD


def add_waist(update, context):
    if update.message.text in MAIN_MENU_BUTTONS:
        return handle_cancel_during_add(update, context)
    try:
        context.user_data['waist'] = parse_float(update.message.text)
    except ValueError:
        update.message.reply_text('Пожалуйста, введите число.')
        return WAIST_ADD
    update.message.reply_text('Введите обхват груди (см):')
    return CHEST_ADD


def add_chest(update, context):
    if update.message.text in MAIN_MENU_BUTTONS:
        return handle_cancel_during_add(update, context)
    try:
        context.user_data['chest'] = parse_float(update.message.text)
    except ValueError:
        update.message.reply_text('Пожалуйста, введите число.')
        return CHEST_ADD
    update.message.reply_text('Введите обхват бицепса (см):')
    return BICEPS_ADD


def add_biceps(update, context):
    if update.message.text in MAIN_MENU_BUTTONS:
        return handle_cancel_during_add(update, context)
    try:
        context.user_data['biceps'] = parse_float(update.message.text)
    except ValueError:
        update.message.reply_text('Пожалуйста, введите число.')
        return BICEPS_ADD

    user_id = update.message.from_user.id
    params = {k: context.user_data[k] for k in [
        'weight', 'hips', 'thigh', 'waist', 'chest', 'biceps'
    ]}
    create_or_update_user(user_id, **params)
    add_new_log_entry(user_id, **params)
    update.message.reply_text(
        'Параметры успешно добавлены!',
        reply_markup=main_keyboard()
    )
    return ConversationHandler.END
