
from telegram import Update
from telegram.ext import ContextTypes

from hktg.constants import (
    Action,
    State,
)
from hktg import db, util, warehouse

class SelectProduct:
    @staticmethod
    async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

        from telegram import InlineKeyboardButton, InlineKeyboardMarkup

        products = db.get_table(db.Tables.PRODUCT)

        buttons = []
        for product_id, product_sym, product_name, _, _ in products:
            buttons.append(InlineKeyboardButton(
                text="%s %s" % (product_sym, product_name),
                callback_data=product_id)
            )

        # users = db.get_table(db.Tables.TG_USERS)
        # is_user = db.find_in_table(users, 1, str(update.effective_user.id))

        # if is_user:
        #     buttons.append(util.action_button(Action.CREATE))

        buttons = util.split_list(buttons, 2)

        keyboard = InlineKeyboardMarkup(buttons)

        await update.callback_query.edit_message_text(text="Виберіть продукцію:", reply_markup=keyboard)

        return State.CHOOSING_PRODUCT

    @staticmethod
    async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:

        selected_product = update.callback_query.data
        user_data = context.user_data['data']

        if isinstance(user_data, db.Entry):
            user_data.product_id = selected_product
            return await warehouse.ViewEntry.ask(update, context)
