from datetime import datetime
from telegram.ext import ConversationHandler, MessageHandler, Filters
from user_data.user_data_storage import get_last_user_entry
from keyboards.main_kb import main_keyboard
from handlers.parameters_states import *
from handlers.parameters_add_handler import (
    add_params_start, add_weight, add_hips, add_thigh,
    add_waist, add_chest, add_biceps, MAIN_MENU_BUTTONS
)


def text_message_handler(update, context):
    text = update.message.text
    if text == '📋 Текущие параметры':
        return show_current_params(update, context)
    if text == '➕ Добавить параметры':
        return add_params_start(update, context)
    update.message.reply_text(
        'Выберите действие из меню.',
        reply_markup=main_keyboard()
    )
    return ConversationHandler.END


def show_current_params(update, context):
    user_id = update.message.from_user.id
    data = get_last_user_entry(user_id)
    if not data:
        update.message.reply_text(
            'Параметры пока не заданы.',
            reply_markup=main_keyboard()
        )
        return ConversationHandler.END

    def fmt_ts(ts):
        for fmt in ('%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S'):
            try:
                return datetime.strptime(ts, fmt).strftime('%d.%m.%Y в %H:%M')
            except Exception:
                pass
        return ts

    text = (
        f'Текущие параметры:\n'
        f'Вес: {data.get("weight", "-")} кг\n'
        f'Объем ягодиц: {data.get("hips", "-")} см\n'
        f'Объем бедра: {data.get("thigh", "-")} см\n'
        f'Объем талии: {data.get("waist", "-")} см\n'
        f'Объем груди: {data.get("chest", "-")} см\n'
        f'Объем бицепса: {data.get("biceps", "-")} см\n'
        f'Последнее обновление: {fmt_ts(data.get("timestamp", ""))}'
    )
    update.message.reply_text(text, reply_markup=main_keyboard())
    return ConversationHandler.END


def register_parameters_handler(dp):
    conv = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.text, text_message_handler),
        ],
        states={
            WEIGHT_ADD: [MessageHandler(Filters.text & ~Filters.command, add_weight)],
            HIPS_ADD: [MessageHandler(Filters.text & ~Filters.command, add_hips)],
            THIGH_ADD: [MessageHandler(Filters.text & ~Filters.command, add_thigh)],
            WAIST_ADD: [MessageHandler(Filters.text & ~Filters.command, add_waist)],
            CHEST_ADD: [MessageHandler(Filters.text & ~Filters.command, add_chest)],
            BICEPS_ADD: [MessageHandler(Filters.text & ~Filters.command, add_biceps)],
        },
        fallbacks=[MessageHandler(Filters.command, lambda u, c: ConversationHandler.END)]
    )
    dp.add_handler(conv)
