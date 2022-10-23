
from typing import Optional, Union

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
from hktg import db, util, users, common

_PROMOTION_MESSAGE = '''Дані про запис:

%s
Коли: %s'''

@dataclass
class ViewPromotion:

    class FieldType(Enum):
        Name = 1,
        Role = 2,

    field_type : Optional[FieldType] = None
    promotion_info : Optional[Union[int, db.Promotion]] = None

    @staticmethod
    async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:

        from telegram import InlineKeyboardButton, InlineKeyboardMarkup

        promotion : db.Promotion = None
        if isinstance(context.user_data['data'], db.Promotion):
            promotion = context.user_data['data']

        buttons = []
        message = _PROMOTION_MESSAGE % ("новий запис", "-")

        action_buttons = []
        if promotion.id:
            message = "%s: %s => %s %s" % (
                promotion.promoter().name,
                promotion.user().name,
                promotion.role().symbol,
                promotion.role().name,
            )
            message = _PROMOTION_MESSAGE % (message, humanize.naturaltime(promotion.datetime))

            if common.tg_has_role(update.effective_user.id, 'admin'):
                action_buttons.append(util.action_button(Action.DELETE))
        else:
            buttons.append([
                util.create_button("Волонтер", callback_data=promotion),
                util.create_button("Роль", callback_data=promotion),
            ])
            buttons.append([
                util.create_button(promotion.name, ViewPromotion(ViewPromotion.FieldType.Name, promotion)),
                util.create_button(promotion.role(), ViewPromotion(ViewPromotion.FieldType.Role, promotion)),
            ])
            if promotion.is_valid():
                action_buttons.append(util.action_button(Action.SAVE))

        action_buttons.append(util.action_button(Action.BACK))
        buttons.append(action_buttons)
        keyboard = InlineKeyboardMarkup(buttons)

        if update.callback_query:
            await update.callback_query.edit_message_text(text=message, reply_markup=keyboard)
        else:
            await update.message.reply_text(text=message, reply_markup=keyboard)

        return State.VIEWING_PROMOTION

    @staticmethod
    async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

        await update.callback_query.answer()

        query_data = update.callback_query.data

        if isinstance(query_data, Action):
            promotion : db.Promotion = context.user_data['data']
            if query_data == Action.BACK:
                context.user_data['data'] = promotion.user()
                return await users.ViewUser.ask(update, context)

            datadict = promotion.to_sql()

            if query_data == Action.DELETE:
                db.delete_value(
                    db.Tables.PROMOTIONS,
                    {'id': promotion.id}
                )

                del context.user_data['data']
                return await users.ViewUser.ask(update, context)
