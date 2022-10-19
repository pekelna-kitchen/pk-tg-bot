
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
from hktg import db, util, users, strings, common


@dataclass
class ViewUser:

    class FieldType(Enum):
        Name = 1,
        Phone = 2,
        TelegramID = 3,
        ViberID = 4,

    field_type : FieldType | None = None
    user_info : int | db.User | None = None

    @staticmethod
    async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:

        from telegram import InlineKeyboardButton, InlineKeyboardMarkup

        user : db.User = None
        if isinstance(context.user_data['data'], db.User):
            user = context.user_data['data']

        buttons = []
        buttons.append([
            util.create_button("Ім'я", callback_data=user),
            util.create_button("Телефон", callback_data=user),
            util.create_button("TG", callback_data=user),
            util.create_button("Viber", callback_data=user),
        ])
        buttons.append([
            util.create_button(user.name, ViewUser(ViewUser.FieldType.Name, user)),
            util.create_button(user.phone, ViewUser(ViewUser.FieldType.Phone, user)),
            util.create_button(user.tg_id, ViewUser(ViewUser.FieldType.TelegramID, user)),
            util.create_button(user.viber_id, ViewUser(ViewUser.FieldType.ViberID, user)),
        ])
        # else:

        action_buttons = []
        if user.id:
            users = db.get_table(db.Tables.USERS, {'id': user.id})
            origin = db.User(*users[0])
            if origin and origin != user:
                action_buttons.append(util.action_button(Action.SAVE))
            promotions = db.get_table(db.Tables.PROMOTIONS, {'id': user.id})
            for promotion in promotions:
                util.create_button("%s: %s => %s" % (promotion.name), ViewUser(ViewUser.FieldType.Name, user))
        elif user.is_valid():
            action_buttons.append(util.action_button(Action.CREATE))


        action_buttons.append(util.action_button(Action.BACK))
        buttons.append(action_buttons)
        keyboard = InlineKeyboardMarkup(buttons)

        message = strings.USER_MESSAGE

        if update.callback_query:
            await update.callback_query.edit_message_text(text=message, reply_markup=keyboard)
        else:
            await update.message.reply_text(text=message, reply_markup=keyboard)

        return State.VIEWING_USER

    @staticmethod
    async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

        # await update.callback_query.answer()

        query_data = update.callback_query.data

        if isinstance(query_data, Action):
            user : db.User = context.user_data['data']
            if query_data == Action.BACK:
                return await users.ViewUsers.ask(update, context)

            datadict = user.to_sql()

            if query_data == Action.SAVE:
                db.update_value(
                    db.Tables.USERS,
                    datadict,
                    {'id': user.id}
                )
                del context.user_data['data']
                return await users.ViewUsers.ask(update, context)

            if query_data == Action.CREATE:
                db.insert_value(db.Tables.USERS, datadict)
                products = db.get_table(db.Tables.PRODUCT, {'id': user.product_id})
                p = db.Product(*products[0])
                context.user_data['data'] = p
                return await users.ViewUsers.ask(update, context)

        if isinstance(query_data, ViewUser):
            context.user_data['data'] = query_data
            if query_data.field_type == ViewUser.FieldType.Name:
                return await common.AskText.ask(update, context)
            if query_data.field_type == ViewUser.FieldType.Phone:
                return await common.AskText.ask(update, context)
            if query_data.field_type == ViewUser.FieldType.TelegramID:
                return await common.AskText.ask(update, context)
            if query_data.field_type == ViewUser.FieldType.ViberID:
                return await common.AskText.ask(update, context)
