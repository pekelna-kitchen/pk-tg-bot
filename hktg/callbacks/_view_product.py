
from telegram import Update
from telegram.ext import ContextTypes

import humanize
from datetime import datetime

from hktg.constants import (
    Action,
    UserData,
    UserDataKey,
    State
)
from hktg import dbwrapper, util, callbacks
from hktg.strings import PRODUCT_MESSAGE

class ViewProduct:

    @staticmethod
    async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:

        from telegram import InlineKeyboardButton, InlineKeyboardMarkup

        query_data = UserData(update.callback_query.data.action)
        user_data = UserData(context.user_data['data'])

        buttons = []

        product_id, product_name, product_sym, limit_container, limit_amount = dbwrapper.find_in_table(
            dbwrapper.Tables.PRODUCT, 0, user_data.action.product_id)

        instances = dbwrapper.get_table(dbwrapper.Tables.INSTANCE, {
            'product_id': user_data.action.product_id
        })
        for (id, product, location, amount, container,  change_date, editor) in instances:
            cont_id, cont_sym, cont_desc = dbwrapper.find_in_table(dbwrapper.Tables.CONTAINER, 0, container)
            _, location_name, location_symbol = dbwrapper.find_in_table(dbwrapper.Tables.LOCATION, 0, location)

            product_info = "%s %s" % (amount, cont_desc)
            product_title = " ".join(
                [location_symbol, location_name, product_info]
            )

            buttons.append([ InlineKeyboardButton(
                text=product_title, 
                # "%s\n%s\n%s" % (product_title, editor, humanize.naturaltime(change_date.replace(tzinfo=None))),
                callback_data=UserData(action=Action.VIEW_ENTRY, entry_id=id)
            )])

        buttons.append([
            InlineKeyboardButton(
                text="🔔 : %s%s" % (limit_amount, limit_container) if limit_container else "🔕",
                # TODO: edit limit
                callback_data=UserData(action=Action.VIEW_PRODUCT, entry_id=product_id)
            ),
            util.action_button(Action.BACK),
        ])
        keyboard = InlineKeyboardMarkup(buttons)

        product_description = "%s %s" % (product_sym, product_name)
        if update.callback_query:
            await update.callback_query.edit_message_text(text=PRODUCT_MESSAGE % product_description, reply_markup=keyboard)
        else:
            await update.message.reply_text(text=PRODUCT_MESSAGE % product_description, reply_markup=keyboard)

        return State.VIEWING_ENTRY

    @staticmethod
    async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

        await update.callback_query.answer()

        query_data = UserData(update.callback_query.data)

        user_data = context.user_data

        if user_data[UserDataKey.ACTION] == Action.BACK:
            return ConversationHandler.END

        async def create(u, c):
            dbwrapper.update_instance(None, update.effective_user.name, {
                "product_id": user_data[UserDataKey.PRODUCT],
                "location_id": user_data[UserDataKey.LOCATION],
                "container_id": user_data[UserDataKey.CONTAINER],
                "amount": update.message.text,
            })
            util.reset_data(context)
            return await callbacks.ViewWarehouse.ask(update, context)

        # query_data = update.callback_query.data
        # for key in query_data:
        #     context.user_data[key] = query_data[key]

        mappings = {
            Action.CREATE: create,
            # Action.VIEW_WAREHOUSE: callbacks.ViewWarehouse.ask,
            Action.MODIFY: callbacks.ViewAmount.ask
        }

        return await mappings[ query_data[ UserDataKey.ACTION ] ](update, context)
