
from telegram import Update, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler

from enum import Enum

import humanize
from datetime import datetime
from dataclasses import dataclass

from hktg.constants import (
    Action,
    State
)
from hktg import db, util, warehouse


NEW_PRODUCT_MESSAGE='''🖊️ Введіть всі дані про новий продукт, щоб мати можливість зберегти його:

🔔 Ліміт можна встановити, щоб отримати сповіщення, якщо щось буде закінчуватись

| Символ | Назва | 🔔 Ліміт (кількість та контейнер) | '''

_PRODUCT_MESSAGE='''ℹ️ Ось дані про продукт:

%s

🔔 Ліміт можна встановити, щоб отримати сповіщення, якщо щось буде закінчуватись

| Символ | Назва | Ліміт (кількість та контейнер) | '''


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

        from telegram import InlineKeyboardMarkup, InlineKeyboardButton

        product_info : db.Product = context.user_data['data']

        # db entry or None
        origin = None
        if product_info.id:
            products = db.get_table(db.Tables.PRODUCT, {'id': product_info.id})
            if products:
                origin = db.Product(*products[0])

            if not product_info.is_valid() and origin:
                product_info = origin

        buttons = []
        # if not product_info.id:
        buttons.append([
            InlineKeyboardButton(text="Символ", callback_data=product_info),
            InlineKeyboardButton(text="Назва", callback_data=product_info),
            InlineKeyboardButton(text="🔔 скільки", callback_data=product_info),
            InlineKeyboardButton(text="🔔 в чому", callback_data=product_info),
        ])
        buttons.append([
            util.create_button(product_info.symbol, ViewProduct(ViewProduct.FieldType.Symbol)),
            util.create_button(product_info.name, ViewProduct(ViewProduct.FieldType.Text)),
            util.create_button(product_info.limit_amount, ViewProduct(ViewProduct.FieldType.LimitAmount)),
            util.create_button(product_info.container(), ViewProduct(ViewProduct.FieldType.LimitContainerID)),
        ])
        
        containers = db.get_table(db.Tables.CONTAINER)
        locations = db.get_table(db.Tables.LOCATION)

        action_buttons = []
        if product_info.id:
            entries = db.get_table(db.Tables.ENTRIES, {
                'product_id': product_info.id
            })
            for entry in entries:
                e = db.Entry(*entry)
                text = "%s %s (%s)" % (
                    e.amount,
                    e.container(containers).desc(),
                    e.location(locations).desc()
                )
                buttons.append([InlineKeyboardButton(text, callback_data=e)])

            if origin and origin != product_info:
                action_buttons.append( util.action_button(Action.SAVE) )
            else:
                action_buttons.append(util.action_button(Action.CREATE))

        elif product_info.is_valid():
            action_buttons.append(util.action_button(Action.SAVE))

        action_buttons.append(util.action_button(Action.BACK))
        buttons.append(action_buttons)

        keyboard = InlineKeyboardMarkup(buttons)

        text = _NEW_PRODUCT_MESSAGE
        if product_info.id:
            text = _PRODUCT_MESSAGE % (product_info.name or "новий продукт якийсь")

        if update.callback_query:
            await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
        else:
            await update.message.reply_text(text=text, reply_markup=keyboard)

        return State.VIEWING_PRODUCT

    @staticmethod
    async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

        await update.callback_query.answer()

        query_data = update.callback_query.data

        if isinstance(query_data, Action):
            if query_data == Action.BACK:
                return await warehouse.ViewProducts.ask(update, context)

            product_info : db.Product = context.user_data['data']
            datadict = product_info.to_sql()

            if query_data == Action.SAVE:
                if product_info.id:
                    db.update_value(db.Tables.PRODUCT, datadict, {'id': product_info.id})
                    context.user_data['data'] = db.Product(id=product_info.id)
                    return await warehouse.ViewProduct.ask(update, context)
                else:
                    db.insert_value(db.Tables.PRODUCT, datadict)
                    del context.user_data['data']
                    return await warehouse.ViewProducts.ask(update, context)


            if query_data == Action.CREATE:
                context.user_data['data'] = db.Entry(product_id=product_info.id)
                return await warehouse.ViewEntry.ask(update, context)


        if isinstance(query_data, db.Entry):
            context.user_data['data'] = query_data
            return await warehouse.ViewEntry.ask(update, context)

        if isinstance(query_data, ViewProduct):
            if query_data.field_type == ViewProduct.FieldType.Symbol:
                return await warehouse.AskSymbol.ask(update, context)
            if query_data.field_type == ViewProduct.FieldType.Text:
                return await common.AskText.ask(update, context)
            if query_data.field_type == ViewProduct.FieldType.LimitAmount:
                return await warehouse.AskAmount.ask(update, context)
            if query_data.field_type == ViewProduct.FieldType.LimitContainerID:
                return await warehouse.SelectContainer.ask(update, context)
