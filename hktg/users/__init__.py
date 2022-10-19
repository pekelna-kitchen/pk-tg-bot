
from ._view_users import ViewUsers
from ._view_user import ViewUser


from telegram.ext import (
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)


def get_handler():

    from hktg.constants import State
    from hktg import home, common

    return ConversationHandler(
        entry_points=[ CallbackQueryHandler(ViewUsers.ask) ],

        states={
            State.VIEWING_USERS: [CallbackQueryHandler(ViewUsers.answer)],
            State.VIEWING_USER: [CallbackQueryHandler(ViewUser.answer)],
            State.ENTERING_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, common.AskText.answer)],
        },
        fallbacks=[
            CallbackQueryHandler(home.Home.ask),
        ],

        map_to_parent={
            # State.VIEWING_USERS: State.VIEWING_USERS,
            State.CHOOSING_ACTION: State.CHOOSING_ACTION,
        },
    )
