from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from user_data.user_data_storage import (
    get_user_progress_for_periods,
    get_last_user_entry
)
from keyboards.progress_kb import progress_keyboard
from handlers.parameters_states import PROGRESS_MENU, PROGRESS_PARAM, PROGRESS_OVERALL

UNITS = {
    'weight': 'кг','hips':'см','thigh':'см',
    'waist':'см','chest':'см','biceps':'см'
}
PERIODS = ['С последнего измерения','За неделю','За месяц']

def pretty_param_name(p):
    names = {
       'weight':'Вес','hips':'Объем ягодиц','thigh':'Объем бедра',
       'waist':'Объем талии','chest':'Объем груди','biceps':'Объем бицепса'
    }
    return f'«{names[p]}»'

def show_progress_menu(update, context):
    if update.callback_query:
        q = update.callback_query; q.answer()
        q.edit_message_text('Выберите параметр:', reply_markup=progress_keyboard())
    else:
        msg = update.message.reply_text('Выберите параметр:', reply_markup=progress_keyboard())
    return PROGRESS_MENU

def progress_for_param(update, context):
    q = update.callback_query; q.answer()
    param   = q.data.replace('progress_','')
    user_id = q.from_user.id

    prog      = get_user_progress_for_periods(user_id, param)
    last_ent  = get_last_user_entry(user_id) or {}
    current   = last_ent.get(param, 'нет данных')

    text = (
        f"{pretty_param_name(param)}\n"
        f"Текущее значение: <b>{current}</b> {UNITS[param]}\n"
    )
    for per in PERIODS:
        v = prog.get(per)
        if isinstance(v, dict):
            suf = f" (от {v['date']})" if v['date'] else ''
            text += f"• {per}{suf}: {v['value']}\n"
        else:
            text += f"• {per}: {v}\n"

    kb = [[InlineKeyboardButton('🔙 Назад', callback_data='progress_menu')]]
    q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode='HTML')
    return PROGRESS_PARAM

def overall_progress(update, context):
    q = update.callback_query; q.answer()

    user_id = q.from_user.id
    text = '<b>📊 Общий прогресс</b>\n\n'
    for p in UNITS:
        prog  = get_user_progress_for_periods(user_id, p)
        start = prog.get('С начала измерений', 'нет данных')
        text += f"{pretty_param_name(p)}: {start}\n"

    kb = [[InlineKeyboardButton('🔙 Назад', callback_data='progress_menu')]]
    q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode='HTML')
    return PROGRESS_OVERALL

def progress_menu_callback(update, context):
    return show_progress_menu(update, context)
