
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

import logging

from hktg.constants import (
    Action,
    State
)
from hktg import db, util, home, users

_USERS_TEXT = '''✔️ Інформація про волонтерів.

'''

class ViewUsers:
    @staticmethod
    async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

        from telegram import InlineKeyboardButton, InlineKeyboardMarkup

        await update.callback_query.answer()

        buttons = []

        users = db.get_table(db.User)
        roles = db.get_table(db.Role)
        promotions = db.get_table(db.Promotion)

        for user in users:
            
            user_str = user.name
            for svc_name, svc_id in (("TG", user.tg_id), ("Viber", user.vb_id)):
                if svc_id:
                    user_str += " [%s: %s]" % (svc_name, svc_id)
            buttons.append(InlineKeyboardButton(user_str, callback_data=user))

        buttons = util.split_list(buttons, 2)

        buttons.append([
            util.action_button(Action.CREATE),
            util.action_button(Action.HOME)])

        keyboard = InlineKeyboardMarkup(buttons)

        await update.callback_query.edit_message_text(text=_USERS_TEXT, reply_markup=keyboard)

        return State.VIEWING_USERS

    @staticmethod
    async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

        await update.callback_query.answer()

        qdata = update.callback_query.data
    
        if isinstance(qdata, db.User):
            context.user_data['data'] = qdata
            return await users.ViewUser.ask(update, context)

        if isinstance(qdata, Action):
            if qdata == Action.CREATE:
                context.user_data['data'] = db.User()
                return await users.ViewUser.ask(update, context)
            if qdata == Action.HOME:
                return await home.Home.ask(update, context)
