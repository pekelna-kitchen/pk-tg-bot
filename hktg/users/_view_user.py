
from typing import Optional

from telegram import Update
from telegram.ext import ContextTypes
from dataclasses import dataclass

from enum import Enum
from datetime import datetime

from hktg.constants import (
    Action,
    State
)
from hktg import db, util, users, common

_USER_MESSAGE = '''👤 Ось така у нас людина є!'''
_NEW_USER_MESSAGE = '''🧐 А хто це новенький в нас тут?'''


@dataclass
class ViewUser:

    class FieldType(Enum):
        Name = 1,
        Phone = 2,
        TelegramID = 3,
        ViberID = 4,

    field_type : Optional[FieldType] = None
    user_info : Optional[int | db.User] = None

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
            util.create_button(user.vb_id, ViewUser(ViewUser.FieldType.ViberID, user)),
        ])
        # else:

        action_buttons = []
        if user.id:
            origin = next(db.get_table(db.User, {'id': user.id}), None)
            if origin and origin != user:
                action_buttons.append(util.action_button(Action.SAVE))
            promotions = db.get_table(db.Promotion, {'users_id': user.id})
            for p in promotions:
                buttons.append([util.create_button(
                    "%s: + %s %s" % (
                        p.promoter().name,
                        p.role().symbol,
                        p.role().name,
                    ), p
                )])
        elif user.is_valid():
            action_buttons.append(util.action_button(Action.SAVE))

        action_buttons.append(util.action_button(Action.CREATE))
        action_buttons.append(util.action_button(Action.BACK))
        buttons.append(action_buttons)
        keyboard = InlineKeyboardMarkup(buttons)

        message = _USER_MESSAGE

        if update.callback_query:
            await update.callback_query.edit_message_text(text=message, reply_markup=keyboard)
        else:
            await update.message.reply_text(text=message, reply_markup=keyboard)

        return State.VIEWING_USER

    @staticmethod
    async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

        await update.callback_query.answer()

        query_data = update.callback_query.data

        if isinstance(query_data, Action):
            user : db.User = context.user_data['data']
            if query_data == Action.BACK:
                return await users.ViewUsers.ask(update, context)

            datadict = user.to_sql()

            if query_data == Action.SAVE:
                if user.id:
                    db.update_value(
                        db.Tables.USERS,
                        datadict,
                        {'id': user.id}
                    )
                else:
                    db.insert_value(db.Tables.USERS, datadict)

                del context.user_data['data']
                return await users.ViewUsers.ask(update, context)

            if query_data == Action.CREATE:
                context.user_data['data'] = db.Promotion()
                return users.ViewPromotion.ask(update, context)

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

        if isinstance(query_data, db.Promotion):
            context.user_data['data'] = query_data
            return await users.ViewPromotion.ask(update, context)

