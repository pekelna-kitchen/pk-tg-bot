
from telegram import Update
from telegram.ext import ContextTypes
from dataclasses import dataclass

import humanize
from enum import Enum
from datetime import datetime

from hktg.constants import (
    Action,
    State
)
from hktg import db, util, warehouse, home


@dataclass
class ViewEntry:

    class FieldType(Enum):
        Product = 1,
        Location = 2,
        Amount = 3,
        Container = 4,

    field_type : FieldType | None = None

    @staticmethod
    async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:

        from telegram import InlineKeyboardButton, InlineKeyboardMarkup

        # query_data = update.callback_query.data

        buttons = []
        buttons.append([ util.action_button(Action.CREATE) ])


        buttons.append([
            util.action_button(Action.BACK),
        ])
        keyboard = InlineKeyboardMarkup(buttons)

        text = "Vodii"
        if update.callback_query:
            await update.callback_query.edit_message_text(text, reply_markup=keyboard)
        else:
            await update.message.reply_text(text=text, reply_markup=keyboard)

        return State.VIEWING_ENTRY

    @staticmethod
    async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

        await update.callback_query.answer()

        query_data = update.callback_query.data
        user_data = context.user_data['data']
