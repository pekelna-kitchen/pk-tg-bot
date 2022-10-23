
import os

from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler
)

from hktg.constants import (
    Action,
    State
)
from hktg import (
    db,
    util,
    driver,
    warehouse,
    users,
    common
)


DEVELOPER_CHAT_ID=os.environ.get('DEVELOPER_CHAT_ID')


_COMEBACK_TEXT = '''😔 Ну ти, цей... повертайся ще. 

PS Для цього використай /start'''


class Home:
    @staticmethod
    async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        
        # await update.effective_message.reply_html(
        #     f"Your chat id is <code>{update.effective_chat.id}</code>."
        # )
        from telegram import InlineKeyboardMarkup, ReplyKeyboardMarkup

        if 'data' in context.user_data:
            del context.user_data['data']

        users = db.get_table(db.User)
        roles = db.get_table(db.Role)

        # import humanize
        text = f"""🏠 Ласкаво прошу до 🌶️Пекельної 🧑‍🍳Кухні! 

        ID: <code>{update.effective_chat.id}</code>.

        😏 Що бажаємо?"""

        buttons = []

        is_admin = common.tg_has_role(update.effective_user.id, 'admin', users, roles)

        if is_admin or common.tg_has_role(update.effective_user.id, 'driver', users, roles):
            buttons.append([ util.action_button(Action.VIEW_MAP), ])

        if is_admin or common.tg_has_role(update.effective_user.id, 'warehouse', users, roles):
            buttons.append([ util.action_button(Action.VIEW_PRODUCTS), ])

        if is_admin:
            buttons.append([ util.action_button(Action.VIEW_USERS), ])

        buttons.append([ util.action_button(ConversationHandler.END) ])

        keyboard = InlineKeyboardMarkup(buttons)
        if update.callback_query:
            await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
        else:
            await update.message.reply_html(text=text, reply_markup=keyboard)

        return State.CHOOSING_ACTION

    @staticmethod
    async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:

        query_data = update.callback_query.data

        action_mapping = {
            Action.VIEW_PRODUCTS: warehouse.ViewProducts.ask,
            Action.VIEW_MAP: driver.ViewMap.ask,
            Action.VIEW_USERS: users.ViewUsers.ask,
            ConversationHandler.END: Home.stop,
        }

        return await action_mapping[query_data](update, context)

    @staticmethod
    async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

        # from telegram import ReplyKeyboardRemove

        if 'data' in context.user_data:
            del context.user_data['data']

        message = _COMEBACK_TEXT

        if update.callback_query:
            await update.callback_query.edit_message_text(text=message)
        else:
            await update.effective_chat.send_message(text=message)

        return ConversationHandler.END

    @staticmethod
    async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:

        import html
        import json
        import logging
        import traceback

        from telegram.constants import ParseMode

        logging.error(msg="Exception while handling an update:", exc_info=context.error)

        return

        tb_list = traceback.format_exception(None, context.error, context.error.__traceback__, limit=5, chain=False)
        tb_string = "\n".join(tb_list)

        # Build the message with some markup and additional information about what happened.
        # You might need to add some logic to deal with messages longer than the 4096 character limit.
        update_str = json.dumps(update.to_dict(), cls=util.EnhancedJSONEncoder, indent=2, ensure_ascii=False) if isinstance(update, Update) else update.__class__.__name__

        message = (
            f"An exception was raised while handling an update\n"
            f"<pre>update = {html.escape(str(update_str))}"
            "</pre>\n\n"
            f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
            f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
            f"<pre>{html.escape(tb_string)}</pre>"
        )

        # Finally, send the message
        await context.bot.send_message(
            chat_id=DEVELOPER_CHAT_ID, text=message, parse_mode=ParseMode.HTML
        )