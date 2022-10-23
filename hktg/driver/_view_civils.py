
from typing import Optional

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
class ViewCivils:

    field_type : Optional[FieldType] = None

    @staticmethod
    async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:

        from telegram import InlineKeyboardButton, InlineKeyboardMarkup

        # query_data = update.callback_query.data

        buttons = []

        civils = db.get_table(db.Civil)

        buttons.append([
            util.action_button(Action.CREATE),
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
