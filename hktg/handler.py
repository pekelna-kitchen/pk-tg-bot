
from telegram.ext import (
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler,
)

from hktg import driver, warehouse, home
from hktg.constants import *

def get():

    return ConversationHandler(
        entry_points=[CommandHandler("start", home.Home.ask)],

        states={
            State.CHOOSING_ACTION: [ CallbackQueryHandler(home.Home.answer) ],
            State.VIEWING_PRODUCTS: [ driver.get_handler() ],
            State.VIEWING_PRODUCTS: [ warehouse.get_handler() ],
        },
        fallbacks=[
            CommandHandler("stop", home.Home.stop),
            CallbackQueryHandler(home.Home.stop)
        ],
        allow_reentry=True
    )
