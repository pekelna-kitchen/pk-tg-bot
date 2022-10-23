
from telegram import Update
from telegram.ext import ContextTypes

from hktg.constants import (
    Action,
    State,
)
from hktg import db, util, warehouse

_SELECT_LOCATION_TEXT = "📍 Виберіть локацію:"

class SelectLocation:
    @staticmethod
    async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

        from telegram import InlineKeyboardButton, InlineKeyboardMarkup

        locations = db.get_table(db.Location)

        buttons = []
        for id, symbol, name in locations:
            buttons.append(InlineKeyboardButton(text="%s %s" % (symbol, name), callback_data=id))

        buttons = util.split_list(buttons, 2)

        keyboard = InlineKeyboardMarkup(buttons)

        # await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=_SELECT_LOCATION_TEXT, reply_markup=keyboard)

        return State.CHOOSING_LOCATION

    @staticmethod
    async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:

        await update.callback_query.answer()

        selected_location = update.callback_query.data
        user_data = context.user_data['data']

        if isinstance(user_data, db.Entry):
            user_data.location_id = selected_location
            return await warehouse.ViewEntry.ask(update, context)

