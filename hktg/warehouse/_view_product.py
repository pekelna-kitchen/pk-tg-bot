
from telegram import Update, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler

from enum import Enum

import humanize
from datetime import datetime
from dataclasses import dataclass

from hktg.constants import (
    Action,
    UserData,
    UserDataKey,
    State
)
from hktg import dbwrapper, util, warehouse
from hktg.strings import PRODUCT_MESSAGE


def create_button(text, callback_data):
    if not text:
        text = "➕"
    return InlineKeyboardButton(text, callback_data=callback_data)

def entry_button(entry):
    e = dbwrapper.Entry(*entry)
    text = "%s %s (%s)" % (e.amount, e.container_symbol(), e.location_symbol())
    return InlineKeyboardButton(text, callback_data=e)

@dataclass
class ViewProduct:
    class FieldType(Enum):
        Symbol = 1,
        Text = 2,
        LimitAmount = 3,
        LimitContainerID = 4,

    field_type : FieldType = None,

    @staticmethod
    async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:

        from telegram import InlineKeyboardMarkup

        # query_data = UserData(update.callback_query.data)
        product_info : dbwrapper.Product = None
        if isinstance(context.user_data['data'], dbwrapper.Product):
            product_info = context.user_data['data']

        buttons = []
        # if not product_info.id:
        buttons.append([
            create_button(product_info.symbol, ViewProduct(ViewProduct.FieldType.Symbol)),
            create_button(product_info.name, ViewProduct(ViewProduct.FieldType.Text)),
            create_button(product_info.limit_amount, ViewProduct(ViewProduct.FieldType.LimitAmount)),
            create_button(product_info.container_symbol(), ViewProduct(ViewProduct.FieldType.LimitContainerID)),
        ])
        # else:
        if product_info.id:
            entries = dbwrapper.get_table(dbwrapper.Tables.ENTRIES, {
                'product_id': product_info.id
            })
            for e in entries:
                buttons.append([entry_button(e)])

            products = dbwrapper.get_table(dbwrapper.Tables.PRODUCT)
            product = util.find_tuple_element(products, {0: product_info.id})
            product_id, product_sym, product_name, limit_container, limit_amount = product
            origin = dbwrapper.Product(product_id, product_sym, product_name, limit_container, limit_amount)
            if not origin == product_info:
                buttons.append([ util.action_button(Action.MODIFY) ])
        elif product_info.is_valid():
            buttons.append([ util.action_button(Action.CREATE) ])

        buttons.append([ util.action_button(Action.BACK) ])

        keyboard = InlineKeyboardMarkup(buttons)

        text = PRODUCT_MESSAGE % (product_info.name or "??")
        if update.callback_query:
            await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
        else:
            await update.message.reply_text(text=text, reply_markup=keyboard)

        return State.VIEWING_PRODUCT

    @staticmethod
    async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

        await update.callback_query.answer()

        query_data = update.callback_query.data

        if isinstance(query_data, UserData):
            if query_data.action == Action.BACK:
                return await warehouse.ViewProducts.ask(update, context)

            product_info : dbwrapper.Product = context.user_data['data']
            datadict = product_info.to_sql()

            if query_data.action == Action.MODIFY:
                dbwrapper.update_value(dbwrapper.Tables.PRODUCT, datadict, {'id': product_info.id})
            if query_data.action == Action.CREATE:
                dbwrapper.insert_value(dbwrapper.Tables.PRODUCT, datadict)

            del context.user_data['data']
            return await warehouse.ViewProducts.ask(update, context)

        if isinstance(query_data, dbwrapper.Entry):
            context.user_data['data'] = query_data
            return await warehouse.ViewEntry.ask(update, context)

        if isinstance(query_data, ViewProduct):
            if query_data.field_type == ViewProduct.FieldType.Symbol:
                return await warehouse.AskSymbol.ask(update, context)
            if query_data.field_type == ViewProduct.FieldType.Text:
                return await warehouse.AskText.ask(update, context)
            if query_data.field_type == ViewProduct.FieldType.LimitAmount:
                return await warehouse.AskAmount.ask(update, context)
            if query_data.field_type == ViewProduct.FieldType.LimitContainerID:
                return await warehouse.SelectContainer.ask(update, context)