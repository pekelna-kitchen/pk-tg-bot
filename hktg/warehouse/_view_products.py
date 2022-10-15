
from telegram import Update
from telegram.ext import ContextTypes

import logging

from hktg.constants import (
    Action,
    UserDataKey,
    State
)
from hktg import dbwrapper, util, warehouse, home
from hktg.strings import FILTERED_VIEW_TEXT, UNFILTERED_TEXT

class ViewProducts:
    @staticmethod
    async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

        from telegram import InlineKeyboardButton, InlineKeyboardMarkup

        await update.callback_query.answer()

        user_data = context.user_data
        # logging.info( user_data['data'].dict() )

        # def constraint(product, location, amount, container, date, editor):
        #     if user_data[UserDataKey.FIELD_TYPE] == UserDataKey.PRODUCT:
        #         return product == user_data[UserDataKey.CURRENT_ID]
        #     if user_data[UserDataKey.FIELD_TYPE] == UserDataKey.LOCATION:
        #         return location == user_data[UserDataKey.CURRENT_ID]
        #     logging.error("unexpected filter type to filter by")
        #     return True

        buttons = []

        products = dbwrapper.get_table(dbwrapper.Tables.PRODUCT)
        # locations = dbwrapper.get_table(dbwrapper.Tables.LOCATION)
        containers = dbwrapper.get_table(dbwrapper.Tables.CONTAINER)
        # entries = dbwrapper.get_table(dbwrapper.Tables.ENTRIES)

        for product_id, product_sym, product_name, limit_container, limit_amount in products:
            prod = dbwrapper.Product(product_id, product_sym, product_name, limit_container, limit_amount)
            buttons.append([
                InlineKeyboardButton(
                    # TODO: message wityh desc
                    text=" ".join([prod.symbol, prod.name, str(prod.limit_amount), prod.container_symbol(containers)]),
                    callback_data=prod
                ),
            ])

        buttons.append([
            util.action_button(Action.CREATE),
            util.action_button(Action.HOME)])

        keyboard = InlineKeyboardMarkup(buttons)

        await update.callback_query.edit_message_text(text=UNFILTERED_TEXT, reply_markup=keyboard)

        return State.VIEWING_PRODUCTS

    @staticmethod
    async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

        await update.callback_query.answer()

        qdata = update.callback_query.data
    
        if isinstance(qdata, dbwrapper.Product):
            context.user_data['data'] = qdata
            return await warehouse.ViewProduct.ask(update, context)

        if isinstance(qdata, Action):
            if qdata == Action.CREATE:
                context.user_data['data'] = dbwrapper.Product()
                return await warehouse.ViewProduct.ask(update, context)
            if qdata == Action.HOME:
                return await home.Home.ask(update, context)
