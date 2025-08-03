from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ConversationHandler
from user_data.user_data_storage import create_or_update_user, update_last_user_entry
from keyboards.parameters_edit_kb import parameters_edit_keyboard
from keyboards.main_kb import main_keyboard
from handlers.parameters_states import (
    EDIT_MENU, WEIGHT_EDIT, HIPS_EDIT, THIGH_EDIT,
    WAIST_EDIT, CHEST_EDIT, BICEPS_EDIT
)
from handlers.parameters_add_handler import MAIN_MENU_BUTTONS
from handlers.inline_utils import clear_all_inlines, register_inline

def pretty_param_name(param):
    names = {
        'weight': 'Вес',
        'hips':   'Объем ягодиц',
        'thigh':  'Объем бедра',
        'waist':  'Объем талии',
        'chest':  'Объем груди',
        'biceps': 'Объем бицепса'
    }
    return f'«{names[param]}»'

def edit_parameters_menu(update, context):
    clear_all_inlines(context)
    if update.callback_query:
        q = update.callback_query; q.answer()
        q.edit_message_text(
            'Выберите параметр для редактирования:',
            reply_markup=parameters_edit_keyboard()
        )
        register_inline(context, q.message.chat.id, q.message.message_id)
    else:
        msg = update.message.reply_text(
            'Выберите параметр для редактирования:',
            reply_markup=parameters_edit_keyboard()
        )
        register_inline(context, msg.chat.id, msg.message_id)
    context.user_data['editing_param'] = True
    return EDIT_MENU

def edit_parameter(update, context):
    q = update.callback_query; q.answer()
    param = q.data.replace('edit_', '')
    context.user_data['edit_param'] = param
    q.edit_message_text(f'Введите новое значение для {pretty_param_name(param)}:')
    return {
        'weight': WEIGHT_EDIT, 'hips': HIPS_EDIT,
        'thigh':  THIGH_EDIT,  'waist': WAIST_EDIT,
        'chest':  CHEST_EDIT,  'biceps': BICEPS_EDIT
    }[param]

def handle_edit(update, context, param):
    from handlers.parameters_main_handler import text_message_handler  # импорт внутри функции

    text = update.message.text
    if text in MAIN_MENU_BUTTONS:
        clear_all_inlines(context)
        update.message.reply_text(
            'Изменение параметра прервано, данные не сохранены.',
            reply_markup=main_keyboard()
        )
        return text_message_handler(update, context)

    try:
        value = int(text)
    except ValueError:
        update.message.reply_text('Пожалуйста, введите число.')
        state_name = f'{param.upper()}_EDIT'
        return globals().get(state_name, ConversationHandler.END)

    user_id = update.message.from_user.id
    update_last_user_entry(user_id, **{param: value})
    create_or_update_user(user_id, **{param: value})

    clear_all_inlines(context)
    update.message.reply_text(f'{pretty_param_name(param)} обновлен.', reply_markup=main_keyboard())
    context.user_data.pop('editing_param', None)
    context.user_data.pop('edit_param', None)
    return ConversationHandler.END

def handle_weight_edit(update, context):  return handle_edit(update, context, 'weight')
def handle_hips_edit(update, context):    return handle_edit(update, context, 'hips')
def handle_thigh_edit(update, context):   return handle_edit(update, context, 'thigh')
def handle_waist_edit(update, context):   return handle_edit(update, context, 'waist')
def handle_chest_edit(update, context):   return handle_edit(update, context, 'chest')
def handle_biceps_edit(update, context):  return handle_edit(update, context, 'biceps')
