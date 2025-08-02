from telegram.ext import ConversationHandler, MessageHandler, Filters
from user_data.user_data_storage import create_or_update_user, update_last_user_entry
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


def add_params_start(update, context):
    update.message.reply_text('Введите ваш вес (кг):')
    return WEIGHT_ADD


def add_weight(update, context):
    if update.message.text in MAIN_MENU_BUTTONS:
        return handle_cancel_during_add(update, context)
    try:
        context.user_data['weight'] = int(update.message.text)
    except ValueError:
        update.message.reply_text('Пожалуйста, введите число.')
        return WEIGHT_ADD
    update.message.reply_text('Объем ягодиц (см):')
    return HIPS_ADD


def add_hips(update, context):
    if update.message.text in MAIN_MENU_BUTTONS:
        return handle_cancel_during_add(update, context)
    try:
        context.user_data['hips'] = int(update.message.text)
    except ValueError:
        update.message.reply_text('Пожалуйста, введите число.')
        return HIPS_ADD
    update.message.reply_text('Объем бедра (см):')
    return THIGH_ADD


def add_thigh(update, context):
    if update.message.text in MAIN_MENU_BUTTONS:
        return handle_cancel_during_add(update, context)
    try:
        context.user_data['thigh'] = int(update.message.text)
    except ValueError:
        update.message.reply_text('Пожалуйста, введите число.')
        return THIGH_ADD
    update.message.reply_text('Объем талии (см):')
    return WAIST_ADD


def add_waist(update, context):
    if update.message.text in MAIN_MENU_BUTTONS:
        return handle_cancel_during_add(update, context)
    try:
        context.user_data['waist'] = int(update.message.text)
    except ValueError:
        update.message.reply_text('Пожалуйста, введите число.')
        return WAIST_ADD
    update.message.reply_text('Объем груди (см):')
    return CHEST_ADD


def add_chest(update, context):
    if update.message.text in MAIN_MENU_BUTTONS:
        return handle_cancel_during_add(update, context)
    try:
        context.user_data['chest'] = int(update.message.text)
    except ValueError:
        update.message.reply_text('Пожалуйста, введите число.')
        return CHEST_ADD
    update.message.reply_text('Объем бицепса (см):')
    return BICEPS_ADD


def add_biceps(update, context):
    if update.message.text in MAIN_MENU_BUTTONS:
        return handle_cancel_during_add(update, context)
    try:
        context.user_data['biceps'] = int(update.message.text)
    except ValueError:
        update.message.reply_text('Пожалуйста, введите число.')
        return BICEPS_ADD

    user_id = update.message.from_user.id
    params = {k: context.user_data[k] for k in [
        'weight', 'hips', 'thigh', 'waist', 'chest', 'biceps'
    ]}
    create_or_update_user(user_id, **params)
    update_last_user_entry(user_id, **params)
    update.message.reply_text(
        'Параметры успешно добавлены!',
        reply_markup=main_keyboard()
    )
    return ConversationHandler.END
