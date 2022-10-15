
from telegram import Update
from telegram.ext import ContextTypes

from hktg.constants import (
    Action,
    State,
)
from hktg import db, util, warehouse

class SelectContainer:
    @staticmethod
    async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup

        containers = db.get_table(db.Tables.CONTAINER)
        buttons = []
        for container_id, containers_symbol, containers_desc in containers:
            buttons.append(
                InlineKeyboardButton(text="%s %s" % (
                    containers_symbol, containers_desc), callback_data=container_id),
            )

        buttons = util.split_list(buttons, 2)

        keyboard = InlineKeyboardMarkup(buttons)
        # keyboard = ReplyKeyboardMarkup(buttons)

        await update.callback_query.edit_message_text(text="Виберіть тару:", reply_markup=keyboard)

        return State.CHOOSING_CONTAINER

    @staticmethod
    async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

        selected_container = update.callback_query.data
        user_data = context.user_data['data']

        if isinstance(user_data, db.Product):
            user_data.limit_container = selected_container
            return await warehouse.ViewProduct.ask(update, context)

        if isinstance(user_data, db.Entry):
            user_data.container_id = selected_container
            return await warehouse.ViewEntry.ask(update, context)
