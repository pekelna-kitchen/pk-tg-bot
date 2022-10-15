
from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler
)

from hktg.constants import (
    Action,
    UserData,
    UserDataKey,
    State
)
from hktg import dbwrapper, util, callbacks

from hktg.strings import SHOWING_TEXT, COMEBACK_TEXT

class Home:
    @staticmethod
    async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        
        # await update.effective_message.reply_html(
        #     f"Your chat id is <code>{update.effective_chat.id}</code>."
        # )
        from telegram import InlineKeyboardMarkup, ReplyKeyboardMarkup

        user_data = util.user_data(context)
        util.reset_data(context)

        # users = dbwrapper.get_table(dbwrapper.Tables.TG_USERS)
        # admins = dbwrapper.get_table(dbwrapper.Tables.TG_ADMINS)
        # locations = dbwrapper.get_table(dbwrapper.Tables.LOCATION)

        # is_user = dbwrapper.find_in_table(dbwrapper.Tables.TG_USERS, 1, str(update.effective_user.id))
        # is_admin = is_user and dbwrapper.find_in_table(dbwrapper.Tables.TG_ADMINS, 1, is_user[0])

        import git
        repo = git.Repo(search_parent_directories=True)

        import humanize
        text = SHOWING_TEXT + "\n\nVersion: %s:%s\n%s" % (
            repo.active_branch.name,
            repo.head.commit.summary,
            humanize.naturaltime(repo.commit().committed_datetime.replace(tzinfo=None)),
        )

        buttons = [
            [ util.action_button(Action.VIEW_WAREHOUSE, {}), ],
            [ util.action_button(Action.VIEW_PRODUCTS, {}), ],
            [ util.action_button(ConversationHandler.END, {}), ],
        ]

        keyboard = InlineKeyboardMarkup(buttons)
        if update.callback_query:
            await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
        else:
            await update.message.reply_text(text=text, reply_markup=keyboard)

        return State.CHOOSING_ACTION

    @staticmethod
    async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:

        query_data = UserData().with_obj(update.callback_query.data)
        # for key in query_data:
        #     context.user_data[key] = query_data[key]

        action_mapping = {
            Action.VIEW_WAREHOUSE: callbacks.ViewWarehouse.ask,
            Action.VIEW_PRODUCTS: callbacks.ViewProducts.ask,
            ConversationHandler.END: callbacks.Home.stop,
        }

        return await action_mapping[query_data.action](update, context)

    @staticmethod
    async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

        # from telegram import ReplyKeyboardRemove

        util.reset_data(context)

        if update.callback_query:
            await update.callback_query.edit_message_text(text=COMEBACK_TEXT)
        else:
            await update.effective_chat.send_message(text=COMEBACK_TEXT)

        return ConversationHandler.END
