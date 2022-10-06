
from telegram import Update
from telegram.ext import ContextTypes

import logging

from hktg.constants import (
    Action,
    UserData,
    UserDataKey,
    State
)
from hktg import dbwrapper, util, callbacks
from hktg.strings import FILTERED_VIEW_TEXT, UNFILTERED_TEXT

class ViewWarehouse:
    @staticmethod
    async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

        from telegram import InlineKeyboardButton, InlineKeyboardMarkup

        await update.callback_query.answer()

        user_data = context.user_data
        logging.info( user_data['data'].dict() )

        # def constraint(product, location, amount, container, date, editor):
        #     if user_data[UserDataKey.FIELD_TYPE] == UserDataKey.PRODUCT:
        #         return product == user_data[UserDataKey.CURRENT_ID]
        #     if user_data[UserDataKey.FIELD_TYPE] == UserDataKey.LOCATION:
        #         return location == user_data[UserDataKey.CURRENT_ID]
        #     logging.error("unexpected filter type to filter by")
        #     return True

        buttons = []

        products = dbwrapper.get_table(dbwrapper.Tables.PRODUCT)
        locations = dbwrapper.get_table(dbwrapper.Tables.LOCATION)
        containers = dbwrapper.get_table(dbwrapper.Tables.CONTAINER)

        for product_id, product_name in products:
        #product_sym, limit_container, limit_amount
            product_info = ""
            for location_id, location_name, location_symbol in locations:
                instances = dbwrapper.get_table(dbwrapper.Tables.INSTANCE, {
                    'product_id': product_id,
                    'location_id': location_id
                })
                location_product_info = ""
                for (id, product, location, amount, container,  date, editor) in instances:
                    cont_id, cont_sym, cont_desc = util.find_in_table(dbwrapper.Tables.CONTAINER, 0, container)
                    location_product_info += "[%s%s]" % (amount, cont_sym)
                if location_product_info:
                    product_info += '%s %s [%s]' % (location_symbol, location_name, location_product_info)

            data = UserData(action=Action.VIEW_PRODUCT, product_id=product_id)
            buttons.append([InlineKeyboardButton(text=" ".join([product_name, product_info]), callback_data=data)])

        buttons.append([
            util.action_button(Action.CREATE),
            util.action_button(Action.HOME)])

        keyboard = InlineKeyboardMarkup(buttons)

        message = None
        # if UserDataKey.FIELD_TYPE in user_data:
        #     if user_data[UserDataKey.FIELD_TYPE] == UserDataKey.PRODUCT:
        #         product_str = util.find_in_table(
        #             dbwrapper.Tables.PRODUCT, 0, user_data[UserDataKey.CURRENT_ID])[1]
        #         message = FILTERED_VIEW_TEXT % product_str

        #     elif user_data[UserDataKey.FIELD_TYPE] == UserDataKey.LOCATION:
        #         location_str = util.find_in_table(dbwrapper.Tables.LOCATION, 0, user_data[UserDataKey.CURRENT_ID])[1]
        #         message = FILTERED_VIEW_TEXT % location_str

        await update.callback_query.edit_message_text(text=message or UNFILTERED_TEXT, reply_markup=keyboard)

        return State.VIEWING_WAREHOUSE

    @staticmethod
    async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

        await update.callback_query.answer()
    
        user_data = UserData(context.user_data['data'])
        query_data = UserData().with_obj(update.callback_query.data)
        context.user_data['data'] = user_data.with_obj(query_data)

        mappings = {
            Action.VIEW_WAREHOUSE: callbacks.ViewWarehouse.ask,
            Action.CREATE: callbacks.ViewEntry.ask,
            Action.VIEW_PRODUCT: callbacks.ViewProduct.ask,
            Action.HOME: callbacks.Home.ask
        }

        return await mappings[user_data.action](update, context)
