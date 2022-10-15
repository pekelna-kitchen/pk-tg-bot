
from telegram import Update
from telegram.ext import ContextTypes

from hktg.constants import (
    Action,
    State,
    UserDataKey
)
from hktg import dbwrapper, warehouse

class AskAmount:
    @staticmethod
    async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:

        from telegram import ReplyKeyboardRemove

        user_data = context.user_data
        message = "ask amount"

        if update.callback_query:
            await update.callback_query.edit_message_text(text=message)
        else:
            await update.message.reply_text(text=message)

        return State.ENTERING_AMOUNT

    @staticmethod
    async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

        user_data = context.user_data['data']

        if not update.message.text.isdigit():
            return await warehouse.AskAmount.ask(update, context)

        if isinstance(user_data, dbwrapper.Product):
            user_data.limit_amount = int(update.message.text)
            return await warehouse.ViewProduct.ask(update, context)

        if isinstance(user_data, dbwrapper.Entry):
            user_data.amount = int(update.message.text)
            return await warehouse.ViewEntry.ask(update, context)

        # logging.error("Unexpected action: %s" % user_data)
