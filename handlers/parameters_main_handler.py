from datetime import datetime
from telegram.ext import ConversationHandler, MessageHandler, Filters, CallbackQueryHandler
from user_data.user_data_storage import get_last_user_entry
from keyboards.main_kb import main_keyboard
from handlers.parameters_states import *
from handlers.parameters_add_handler import (
    add_params_start, add_weight, add_hips, add_thigh,
    add_waist, add_chest, add_biceps, MAIN_MENU_BUTTONS
)
from handlers.parameters_edit_handler import (
    edit_parameters_menu, edit_parameter,
    handle_weight_edit, handle_hips_edit,
    handle_thigh_edit, handle_waist_edit,
    handle_chest_edit, handle_biceps_edit
)
from handlers.progress_handler import (
    show_progress_menu, progress_for_param,
    overall_progress, progress_menu_callback
)
from handlers.inline_utils import clear_all_inlines

def text_message_handler(update, context):
    clear_all_inlines(context)
    text = update.message.text
    if text == '📋 Текущие параметры':
        return show_current_params(update, context)
    if text == '➕ Добавить параметры':
        return add_params_start(update, context)
    if text == '✏️ Редактировать параметры':
        return edit_parameters_menu(update, context)
    if text == '📈 Мой прогресс':
        return show_progress_menu(update, context)
    update.message.reply_text("Выберите действие из меню.", reply_markup=main_keyboard())
    return ConversationHandler.END

def show_current_params(update, context):
    clear_all_inlines(context)
    user_id = update.message.from_user.id
    data = get_last_user_entry(user_id)
    if not data:
        update.message.reply_text("Параметры пока не заданы.", reply_markup=main_keyboard())
        return ConversationHandler.END

    def fmt_ts(ts):
        for fmt in ("%Y-%m-%dT%H:%M:%S","%Y-%m-%d %H:%M:%S"):
            try:
                return datetime.strptime(ts, fmt).strftime("%d.%m.%Y в %H:%M")
            except:
                pass
        return ts

    text = (
        f"Текущие параметры:\n"
        f"Вес: {data.get('weight', '-') } кг\n"
        f"Объем ягодиц: {data.get('hips', '-') } см\n"
        f"Объем бедра: {data.get('thigh', '-') } см\n"
        f"Объем талии: {data.get('waist', '-') } см\n"
        f"Объем груди: {data.get('chest', '-') } см\n"
        f"Объем бицепса: {data.get('biceps', '-') } см\n"
        f"Последнее обновление: {fmt_ts(data.get('timestamp',''))}"
    )
    update.message.reply_text(text, reply_markup=main_keyboard())
    return ConversationHandler.END

def register_parameters_handler(dp):
    conv = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.text, text_message_handler),
            CallbackQueryHandler(progress_for_param, pattern='^progress_(weight|hips|thigh|waist|chest|biceps)$'),
            CallbackQueryHandler(overall_progress, pattern='^progress_overall$'),
            CallbackQueryHandler(progress_menu_callback, pattern='^progress_menu$'),
            CallbackQueryHandler(edit_parameter, pattern='^edit_'),
        ],
        states={
            WEIGHT_ADD: [MessageHandler(Filters.text & ~Filters.command, add_weight)],
            HIPS_ADD:   [MessageHandler(Filters.text & ~Filters.command, add_hips)],
            THIGH_ADD:  [MessageHandler(Filters.text & ~Filters.command, add_thigh)],
            WAIST_ADD:  [MessageHandler(Filters.text & ~Filters.command, add_waist)],
            CHEST_ADD:  [MessageHandler(Filters.text & ~Filters.command, add_chest)],
            BICEPS_ADD: [MessageHandler(Filters.text & ~Filters.command, add_biceps)],

            EDIT_MENU: [
                CallbackQueryHandler(edit_parameter, pattern='^edit_'),
                MessageHandler(Filters.text, text_message_handler),
            ],
            WEIGHT_EDIT: [MessageHandler(Filters.text & ~Filters.command, handle_weight_edit)],
            HIPS_EDIT:   [MessageHandler(Filters.text & ~Filters.command, handle_hips_edit)],
            THIGH_EDIT:  [MessageHandler(Filters.text & ~Filters.command, handle_thigh_edit)],
            WAIST_EDIT:  [MessageHandler(Filters.text & ~Filters.command, handle_waist_edit)],
            CHEST_EDIT:  [MessageHandler(Filters.text & ~Filters.command, handle_chest_edit)],
            BICEPS_EDIT: [MessageHandler(Filters.text & ~Filters.command, handle_biceps_edit)],

            PROGRESS_MENU: [
                CallbackQueryHandler(progress_for_param,
                                     pattern='^progress_(weight|hips|thigh|waist|chest|biceps)$'),
                CallbackQueryHandler(overall_progress, pattern='^progress_overall$'),
                CallbackQueryHandler(progress_menu_callback, pattern='^progress_menu$'),
                MessageHandler(Filters.text, text_message_handler),
            ],
            PROGRESS_PARAM: [
                CallbackQueryHandler(progress_for_param,
                                     pattern='^progress_(weight|hips|thigh|waist|chest|biceps)$'),
                CallbackQueryHandler(progress_menu_callback, pattern='^progress_menu$'),
                CallbackQueryHandler(overall_progress, pattern='^progress_overall$'),
                MessageHandler(Filters.text, text_message_handler),
            ],
            PROGRESS_OVERALL: [
                CallbackQueryHandler(overall_progress, pattern='^progress_overall$'),
                CallbackQueryHandler(progress_menu_callback, pattern='^progress_menu$'),
                CallbackQueryHandler(progress_for_param,
                                     pattern='^progress_(weight|hips|thigh|waist|chest|biceps)$'),
                MessageHandler(Filters.text, text_message_handler),
            ],
        },
        fallbacks=[MessageHandler(Filters.command, lambda u, c: ConversationHandler.END)]
    )
    dp.add_handler(conv)
