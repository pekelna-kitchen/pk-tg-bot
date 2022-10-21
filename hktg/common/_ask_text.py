
from telegram import Update
from telegram.ext import ContextTypes

from hktg.constants import State
from hktg import db, warehouse, users

_NAME_TEXT = "Введіть текст:"

class AskText:
    @staticmethod
    async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

        user_data = context.user_data['data']

        message = _NAME_TEXT

        if update.callback_query:
            await update.callback_query.edit_message_text(text=message)
        else:
            await update.message.reply_text(text=message)

        return State.ENTERING_TEXT

    @staticmethod
    async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

        user_data = context.user_data['data']
        if isinstance(user_data, db.Product):
            user_data.name = update.message.text
            return await warehouse.ViewProduct.ask(update, context)

        if isinstance(user_data, users.ViewUser):
            query_data = user_data.user_info
            if user_data.field_type == users.ViewUser.FieldType.Name:
                query_data.name = update.message.text
            if user_data.field_type == users.ViewUser.FieldType.Phone:
                query_data.phone = update.message.text
            if user_data.field_type == users.ViewUser.FieldType.TelegramID:
                query_data.tg_id = update.message.text
            if user_data.field_type == users.ViewUser.FieldType.ViberID:
                query_data.vb_id = update.message.text
            
            context.user_data['data'] = query_data
            return await users.ViewUser.ask(update, context)
