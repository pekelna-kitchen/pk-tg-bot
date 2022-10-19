
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
from hktg import db, util, warehouse, strings


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

        entry : db.Entry = None
        if isinstance(context.user_data['data'], db.Entry):
            entry = context.user_data['data']

        buttons = []
        buttons.append([
            util.create_button("Що", callback_data=entry),
            util.create_button("Де", callback_data=entry),
            util.create_button("Скільки", callback_data=entry),
            util.create_button("Чого", callback_data=entry),
        ])
        buttons.append([
            util.create_button(entry.product(), ViewEntry(ViewEntry.FieldType.Product)),
            util.create_button(entry.location(), ViewEntry(ViewEntry.FieldType.Location)),
            util.create_button(entry.amount, ViewEntry(ViewEntry.FieldType.Amount)),
            util.create_button(entry.container(), ViewEntry(ViewEntry.FieldType.Container)),
        ])
        # else:

        action_buttons = []
        if entry.id:
            entries = db.get_table(db.Tables.ENTRIES, {'id': entry.id})
            origin = db.Entry(*entries[0])
            if origin and origin != entry:
                action_buttons.append(util.action_button(Action.SAVE))
        elif entry.is_valid():
            action_buttons.append(util.action_button(Action.CREATE))


        action_buttons.append(util.action_button(Action.BACK))
        buttons.append(action_buttons)
        keyboard = InlineKeyboardMarkup(buttons)

        editor_tuple = ('ніхто', 'ніколи')
        if entry.editor and entry.date:
            editor_tuple = (entry.editor, humanize.naturaltime(entry.date.replace(tzinfo=None)))

        message = strings.ENTRY_MESSAGE % editor_tuple

        if update.callback_query:
            await update.callback_query.edit_message_text(text=message, reply_markup=keyboard)
        else:
            await update.message.reply_text(text=message, reply_markup=keyboard)

        return State.VIEWING_ENTRY

    @staticmethod
    async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

        # await update.callback_query.answer()

        query_data = update.callback_query.data

        if isinstance(query_data, Action):
            entry : db.Entry = context.user_data['data']
            if query_data == Action.BACK:
                products = db.get_table(db.Tables.PRODUCT, {'id': entry.product_id})
                p = db.Product(*products[0])
                context.user_data['data'] = p
                return await warehouse.ViewProduct.ask(update, context)

            entry.editor = update.effective_user.name
            entry.date = datetime.now()

            entry_id = entry.id
            entry.id = None

            datadict = entry.to_sql()

            if query_data == Action.SAVE:
                db.update_value(
                    db.Tables.ENTRIES,
                    datadict,
                    {'id': entry_id}
                )
                products = db.get_table(db.Tables.PRODUCT, {'id': entry.product_id})
                p = db.Product(*products[0])
                context.user_data['data'] = p
                return await warehouse.ViewProduct.ask(update, context)

            if query_data == Action.CREATE:
                db.insert_value(db.Tables.ENTRIES, datadict)
                products = db.get_table(db.Tables.PRODUCT, {'id': entry.product_id})
                p = db.Product(*products[0])
                context.user_data['data'] = p
                return await warehouse.ViewProduct.ask(update, context)

            # context.user_data['data'] = db.Product(entry_data.product_id)
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
