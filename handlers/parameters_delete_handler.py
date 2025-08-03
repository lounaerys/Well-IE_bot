from telegram.ext import ConversationHandler
from user_data.user_data_storage import delete_all_user_data
from keyboards.parameters_delete_kb import delete_confirm_keyboard
from keyboards.main_kb import main_keyboard
from handlers.parameters_states import DELETE_CONFIRM
from handlers.inline_utils import clear_all_inlines, register_inline


def ask_delete_data(update, context):
    clear_all_inlines(context)
    user_id = update.effective_user.id if update.callback_query else update.message.from_user.id
    from user_data.user_data_storage import get_last_user_entry
    data = get_last_user_entry(user_id)
    if not data:
        if update.callback_query:
            q = update.callback_query
            q.answer()
            q.message.reply_text('Данных для удаления пока нет.', reply_markup=main_keyboard())
        else:
            update.message.reply_text('Данных для удаления пока нет.', reply_markup=main_keyboard())
        return ConversationHandler.END
    kb = delete_confirm_keyboard()
    if update.callback_query:
        q = update.callback_query
        q.answer()
        q.edit_message_text(
            'Вы уверены, что хотите удалить все свои данные? Это действие необратимо.',
            reply_markup=kb
        )
        register_inline(context, q.message.chat.id, q.message.message_id)
    else:
        msg = update.message.reply_text(
            'Вы уверены, что хотите удалить все свои данные? Это действие необратимо.',
            reply_markup=kb
        )
        register_inline(context, msg.chat.id, msg.message_id)
    return DELETE_CONFIRM


def delete_data_confirm_inline(update, context):
    clear_all_inlines(context)
    q = update.callback_query
    q.answer()
    if q.data == 'delete_confirm_yes':
        delete_all_user_data(q.from_user.id)
        q.edit_message_text('Все ваши данные удалены!')
    else:
        q.edit_message_text('Удаление отменено, данные не удалены.')
    return ConversationHandler.END


def cancel_delete_inline(update, context):
    clear_all_inlines(context)
    q = update.callback_query
    q.answer()
    q.message.reply_text(
        'Операция удаления отменена, данные не удалены.',
        reply_markup=main_keyboard()
    )
    return ConversationHandler.END


def cancel_delete_by_message(update, context):
    clear_all_inlines(context)
    from handlers.parameters_main_handler import text_message_handler
    return text_message_handler(update, context)
