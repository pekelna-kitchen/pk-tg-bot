
from telegram import Update
from telegram.ext import ContextTypes

from hktg.constants import (
    Action,
    State,
    UserDataKey
)
from hktg import dbwrapper, util, callbacks

class SelectProduct:
    @staticmethod
    async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

        from telegram import InlineKeyboardButton, InlineKeyboardMarkup

        products = dbwrapper.get_table(dbwrapper.Tables.PRODUCT)

        buttons = []
        for product_id, product_sym, product_name, _, _ in products:
            buttons.append(InlineKeyboardButton(
                text="%s %s" % (product_sym, product_name),
                callback_data=product_id)
            )

        # users = dbwrapper.get_table(dbwrapper.Tables.TG_USERS)
        # is_user = dbwrapper.find_in_table(users, 1, str(update.effective_user.id))

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

        if isinstance(user_data, dbwrapper.Entry):
            user_data.product_id = selected_product
            return await callbacks.ViewEntry.ask(update, context)

        # if isentry(selected_product, dict):
        #     return await callbacks.AddProduct.ask(update, context)

        # if context.user_data[UserDataKey.ACTION] == Action.MODIFY:
        #     if context.user_data[UserDataKey.FIELD_TYPE] == UserDataKey.PRODUCT:
        #         dbwrapper.update_value(
        #             dbwrapper.Tables.ENTRIES, {'product_id': selected_product}, 
        #             {'id': context.user_data[UserDataKey.CURRENT_ID]})
        #     else:
        #         logging.error("Unexpected datafield %s" %
        #                       context.user_data[UserDataKey.FIELD_TYPE])
        #     return await callbacks.Home.ask(update, context)
        # elif context.user_data[UserDataKey.ACTION] == Action.CREATE:
        #     context.user_data[UserDataKey.PRODUCT] = selected_product
        #     return await callbacks.SelectContainer.ask(update, context)
