
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
from hktg import dbwrapper, util, warehouse
from hktg.strings import ENTRY_MESSAGE

def create_button(text, callback_data):
    from telegram import InlineKeyboardButton
    if not text:
        text = "➕"
    return InlineKeyboardButton(text, callback_data=callback_data)


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

        entry : dbwrapper.Entry = None
        if isinstance(context.user_data['data'], dbwrapper.Entry):
            entry = context.user_data['data']

        buttons = []
        # if not product_info.id:
        buttons.append([
            create_button(entry.product_symbol(), ViewEntry(ViewEntry.FieldType.Product)),
            create_button(entry.location_symbol(), ViewEntry(ViewEntry.FieldType.Location)),
            create_button(entry.amount, ViewEntry(ViewEntry.FieldType.Amount)),
            create_button(entry.container_symbol(), ViewEntry(ViewEntry.FieldType.Container)),
        ])
        # else:
        if entry.id:
            entries = dbwrapper.get_table(dbwrapper.Tables.ENTRIES, {'id': entry.id})
            result_entry = util.find_tuple_element(entries, {0: entry.id})
            entry_id, product_id, location_id, amount, container_id, date, editor = result_entry
            origin = dbwrapper.Entry(entry_id, product_id, location_id, amount, container_id, date, editor)
            if not origin == entry:
                buttons.append([ util.action_button(Action.SAVE) ])
        elif entry.is_valid():
            buttons.append([ util.action_button(Action.CREATE) ])


        buttons.append([
            util.action_button(Action.BACK),
        ])
        keyboard = InlineKeyboardMarkup(buttons)

        editor_tuple = (entry.editor, humanize.naturaltime(entry.date.replace(tzinfo=None))) if entry.editor else ('ніхто', 'ніколи')

        if update.callback_query:
            await update.callback_query.edit_message_text(text=ENTRY_MESSAGE % editor_tuple, reply_markup=keyboard)
        else:
            await update.message.reply_text(text=ENTRY_MESSAGE % editor_tuple, reply_markup=keyboard)

        return State.VIEWING_ENTRY

    @staticmethod
    async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

        await update.callback_query.answer()

        query_data = update.callback_query.data

        if isinstance(query_data, Action):
            entry : dbwrapper.Entry = context.user_data['data']
            if query_data == Action.BACK:
                products = dbwrapper.get_table(dbwrapper.Tables.PRODUCT, {'id': product_info.id})
                context.user_data['data'] = dbwrapper.Product(*products[0])
                return await warehouse.ViewProduct.ask(update, context)

            entry.editor = update.effective_user.name
            entry.date = datetime.now()

            entry_id = entry.id
            entry.id = None

            datadict = entry.to_sql()

            if query_data == Action.SAVE:
                dbwrapper.update_value(
                    dbwrapper.Tables.ENTRIES,
                    datadict,
                    {'id': entry_id}
                )

            if query_data == Action.CREATE:
                dbwrapper.insert_value(dbwrapper.Tables.ENTRIES, datadict)

            # context.user_data['data'] = dbwrapper.Product(entry_data.product_id)
            # return await warehouse.ViewProduct.ask(update, context)

        if isinstance(query_data, ViewEntry):
            if query_data.field_type == ViewEntry.FieldType.Product:
                return await warehouse.SelectProduct.ask(update, context)
            if query_data.field_type == ViewEntry.FieldType.Location:
                return await warehouse.SelectLocation.ask(update, context)
            if query_data.field_type == ViewEntry.FieldType.Amount:
                return await warehouse.AskAmount.ask(update, context)
            if query_data.field_type == ViewEntry.FieldType.Container:
                return await warehouse.SelectContainer.ask(update, context)
