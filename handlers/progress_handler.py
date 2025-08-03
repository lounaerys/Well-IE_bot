from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from user_data.user_data_storage import (
    get_user_progress_for_periods,
    get_last_user_entry
)
from keyboards.progress_kb import progress_keyboard
from handlers.parameters_states import PROGRESS_MENU, PROGRESS_PARAM, PROGRESS_OVERALL
from handlers.inline_utils import clear_all_inlines, register_inline


UNITS = {
    'weight': 'кг', 'hips': 'см', 'thigh': 'см',
    'waist': 'см', 'chest': 'см', 'biceps': 'см'
}
PERIODS = ['С последнего измерения', 'За неделю', 'За месяц']

EMOJIS = {
    'weight': '⚖️',
    'hips': '🍑',
    'thigh': '🦵',
    'waist': '🔄',
    'chest': '🎽',
    'biceps': '💪'
}


def pretty_param_name(p):
    names = {
        'weight': 'Вес',
        'hips': 'Обхват ягодиц',
        'thigh': 'Обхват бедра',
        'waist': 'Обхват талии',
        'chest': 'Обхват груди',
        'biceps': 'Обхват бицепса'
    }
    return f'{EMOJIS[p]} {names[p]}'


def format_number(val, param):
    try:
        num = float(val)
        if num.is_integer():
            return str(int(num))
        if param == 'weight':
            return f'{num:.2f}'.rstrip('0').rstrip('.')
        else:
            return f'{num:.1f}'.rstrip('0').rstrip('.')
    except Exception:
        return val


def format_with_sign(val, param=None):
    try:
        num = float(val)
        formatted_val = format_number(num, param) if param else str(val)
        if num > 0:
            return f'+ {formatted_val}'
        if num < 0:
            return f'- {formatted_val.lstrip("-")}'
        return formatted_val
    except Exception:
        return val


def _format_progress_block(param, current, prog):
    def get_trend_emoji(change):
        try:
            val = float(change)
        except (TypeError, ValueError):
            return '⏸️'
        if val > 0:
            return '🔼'
        if val < 0:
            return '🔽'
        return '⏸️'

    unit = UNITS[param]
    trend_val = prog.get('С последнего измерения')
    if isinstance(trend_val, dict):
        trend_val = trend_val.get('value', '0')
    trend_emoji = get_trend_emoji(trend_val)
    current_str = f'{trend_emoji} {current} {unit}' if current != 'нет данных' else 'нет данных'
    param_name_bold = f'<b>{pretty_param_name(param)}</b>'
    text = f'{param_name_bold}\n'
    text += f'Текущее значение: <b>{current_str}</b>\n'

    for per in PERIODS:
        v = prog.get(per)
        if isinstance(v, dict):
            suf = f" ({v['date']})" if v['date'] else ''
            val_str = format_with_sign(v['value'], param)
        else:
            suf = ''
            val_str = format_with_sign(v, param)
        try:
            float_val = float(val_str.replace('+', '').replace('-', '').replace(' ', ''))
            show_unit = True
        except Exception:
            show_unit = False
        text += f'• {per}{suf}: {val_str}{" " + unit if show_unit else ""}\n'

    start_val = prog.get('С начала измерений')
    start_date = ''
    if isinstance(start_val, dict):
        val_str = format_with_sign(start_val['value'], param)
        if start_val.get('date'):
            start_date = f" ({start_val['date']})"
    else:
        val_str = format_with_sign(start_val, param)
    if start_val is not None and (not isinstance(start_val, dict) or start_val.get('value') != 'нет данных для сравнения с началом'):
        try:
            float_val = float(val_str.replace('+', '').replace('-', '').replace(' ', ''))
            show_unit = True
        except Exception:
            show_unit = False
        text += f'• С начала измерений{start_date}: {val_str}{" " + unit if show_unit else ""}\n'
    return text


def show_progress_menu(update, context):
    clear_all_inlines(context)
    if update.callback_query:
        q = update.callback_query
        q.answer()
        q.edit_message_text('Выберите параметр:', reply_markup=progress_keyboard())
        register_inline(context, q.message.chat.id, q.message.message_id)
    else:
        msg = update.message.reply_text('Выберите параметр:', reply_markup=progress_keyboard())
        register_inline(context, msg.chat.id, msg.message_id)
    return PROGRESS_MENU


def progress_for_param(update, context):
    clear_all_inlines(context)
    q = update.callback_query
    q.answer()
    param = q.data.replace('progress_', '')
    user_id = q.from_user.id

    prog = get_user_progress_for_periods(user_id, param)
    last_ent = get_last_user_entry(user_id) or {}
    current = last_ent.get(param, 'нет данных')

    text = _format_progress_block(param, current, prog)

    kb = [[InlineKeyboardButton('🔙 Назад', callback_data='progress_menu')]]
    q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode='HTML')
    register_inline(context, q.message.chat.id, q.message.message_id)
    return PROGRESS_PARAM


def overall_progress(update, context):
    clear_all_inlines(context)
    q = update.callback_query
    q.answer()

    user_id = q.from_user.id
    text = '<b>📊 Общий прогресс</b>\n\n'
    for p in UNITS:
        prog = get_user_progress_for_periods(user_id, p)
        last_ent = get_last_user_entry(user_id) or {}
        current = last_ent.get(p, 'нет данных')
        text += _format_progress_block(p, current, prog) + '\n'

    kb = [[InlineKeyboardButton('🔙 Назад', callback_data='progress_menu')]]
    q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode='HTML')
    register_inline(context, q.message.chat.id, q.message.message_id)
    return PROGRESS_OVERALL


def progress_menu_callback(update, context):
    return show_progress_menu(update, context)
