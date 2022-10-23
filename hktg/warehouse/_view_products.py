
from telegram import Update
from telegram.ext import ContextTypes

import logging

from hktg.constants import (
    Action,
    State
)
from hktg import db, util, warehouse, home

_WAREHOUSE_TEXT = "✔️ Ось що в нас є:"

class ViewProducts:
    @staticmethod
    async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

        from telegram import InlineKeyboardButton, InlineKeyboardMarkup

        await update.callback_query.answer()

        buttons = []

        products = db.get_table(db.Product)
        locations = db.get_table(db.Location)
        containers = db.get_table(db.Container)

        for p in products:
            entries = db.get_table(db.Entry, {'product_id': p.id})
            e_desc = ''
            for e in entries:
                e_desc += ' '.join([e_desc, '[%s%s]' % (e.amount, e.container(containers).symbol)])
                # entries_desc = ' '.join([p.symbol, p.name, e_desc])

            buttons.append(
                InlineKeyboardButton(
                    # TODO: message wityh desc
                    text=" ".join([p.symbol, p.name, e_desc]),
                    callback_data=p
                ),
            )

        buttons = util.split_list(buttons, 2)
        buttons.append([
            util.action_button(Action.CREATE),
            util.action_button(Action.HOME)])

        keyboard = InlineKeyboardMarkup(buttons)

        await update.callback_query.edit_message_text(text=_WAREHOUSE_TEXT, reply_markup=keyboard)

        return State.VIEWING_PRODUCTS

    @staticmethod
    async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

        await update.callback_query.answer()

        qdata = update.callback_query.data
    
        if isinstance(qdata, db.Product):
            context.user_data['data'] = qdata
            return await warehouse.ViewProduct.ask(update, context)

        if isinstance(qdata, Action):
            if qdata == Action.CREATE:
                context.user_data['data'] = db.Product()
                return await warehouse.ViewProduct.ask(update, context)
            if qdata == Action.HOME:
                return await home.Home.ask(update, context)
