

from telegram import Update
from telegram.ext import ContextTypes

from hktg import db, warehouse, strings
from hktg.constants import (
    Action,
    State
)

class AskSymbol:
    @staticmethod
    async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=strings.SYMBOL_TEXT)

        return State.ENTERING_SYMBOL

    @staticmethod
    async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

        user_data = context.user_data['data']

        if isinstance(user_data, db.Product):
            user_data.symbol = update.message.text
            return await warehouse.ViewProduct.ask(update, context)
