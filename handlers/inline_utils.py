def clear_all_inlines(context):
    bot = context.bot
    msgs = context.user_data.pop('inline_msgs', [])
    for chat_id, msg_id in msgs:
        try:
            bot.edit_message_reply_markup(
                chat_id=chat_id,
                message_id=msg_id,
                reply_markup=None
            )
        except:
            pass


def register_inline(context, chat_id, message_id):
    lst = context.user_data.get('inline_msgs')
    if lst is None:
        lst = []
        context.user_data['inline_msgs'] = lst
    lst.append((chat_id, message_id))
