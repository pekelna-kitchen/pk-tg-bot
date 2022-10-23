
from telegram.ext import (
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler,
)

from hktg import driver, warehouse, home, users
from hktg.constants import *

def get():

    return ConversationHandler(
        entry_points=[CommandHandler("start", home.Home.ask)],

        states={
            State.CHOOSING_ACTION: [ CallbackQueryHandler(home.Home.answer) ],
            State.VIEWING_MAP: [ driver.get_handler() ],
            State.VIEWING_PRODUCTS: [ warehouse.get_handler() ],
            State.VIEWING_USERS: [ users.get_handler() ],
        },
        fallbacks=[
            CommandHandler("stop", home.Home.stop),
            CallbackQueryHandler(home.Home.stop)
        ],
        # map_to_parent={
        #     State.VIEWING_USERS: State.VIEWING_USERS,
        #     State.VIEWING_MAP: State.VIEWING_MAP,
        #     State.VIEWING_PRODUCTS: State.VIEWING_PRODUCTS,
        #     State.CHOOSING_ACTION: State.CHOOSING_ACTION,
        # },
        allow_reentry=True
    )
