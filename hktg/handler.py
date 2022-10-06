
from telegram import (
    Update
)
from telegram.ext import (
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)

from hktg import dbwrapper, callbacks
from hktg.constants import *

def get():

    entry_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(callbacks.ViewEntry.ask)],

        states={
            State.VIEWING_ENTRY: [CallbackQueryHandler(callbacks.ViewEntry.ask)],
            State.CHOOSING_LOCATION: [CallbackQueryHandler(callbacks.SelectLocation.ask)],
            # State.CHOOSING_LOCATION: [CallbackQueryHandler(select_location.SelectLocation.answer)],
            State.CHOOSING_PRODUCT: [CallbackQueryHandler(callbacks.SelectProduct.ask)],
            State.CHOOSING_CONTAINER: [CallbackQueryHandler(callbacks.SelectContainer.answer)],
        },
        fallbacks=[
            # CallbackQueryHandler(callbacks.Home.stop),
            # CommandHandler("stop", stop_nested),
        ],

        map_to_parent={
            # After showing data return to top level menu
            # State.SHOWING: SHOWING,

            # Return to top level menu
            State.VIEWING_ENTRY: State.VIEWING_ENTRY,
            ConversationHandler.END: State.VIEWING_ENTRY,
            # End conversation altogether
            # STOPPING: END,
        },
    )


    warehouse_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(callbacks.ViewEntry.ask)],

        states={
            State.VIEWING_ENTRY: [CallbackQueryHandler(callbacks.ViewEntry.ask)],
            State.CHOOSING_LOCATION: [CallbackQueryHandler(callbacks.SelectLocation.ask)],
            State.CHOOSING_PRODUCT: [CallbackQueryHandler(callbacks.SelectProduct.ask)],
            State.CHOOSING_CONTAINER: [CallbackQueryHandler(callbacks.SelectContainer.answer)],
        },
        fallbacks=[
            # CallbackQueryHandler(callbacks.Home.stop),
            # CommandHandler("stop", stop_nested),
        ],

        map_to_parent={
            # After showing data return to top level menu
            # State.SHOWING: SHOWING,

            # Return to top level menu
            State.VIEWING_WAREHOUSE: State.VIEWING_WAREHOUSE,
            ConversationHandler.END: State.VIEWING_WAREHOUSE,
            # End conversation altogether
            # STOPPING: END,
        },
    )

    return ConversationHandler(
        entry_points=[CommandHandler("start", callbacks.Home.ask)],

        states={
            State.CHOOSING_ACTION: [CallbackQueryHandler(callbacks.Home.answer)],
            State.CHOOSING_PRODUCT: [CallbackQueryHandler(callbacks.SelectProduct.answer)],
            State.ENTERING_LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, callbacks.AddLocation.answer)],
            State.ENTERING_PRODUCT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, callbacks.AddProduct.answer)
            ],
            State.ENTERING_CONTAINER_SYMBOL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, callbacks.AddContainerSymbol.answer)
            ],
            State.ENTERING_CONTAINER_DESCRIPTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, callbacks.AddContainerDescription.answer)
            ],
            State.ENTERING_AMOUNT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, callbacks.AskAmount.answer)
            ],
            State.VIEWING_WAREHOUSE: [CallbackQueryHandler(callbacks.ViewWarehouse.answer)],
            State.VIEWING_ENTRY: [[entry_handler]] # CallbackQueryHandler(callbacks.ViewEntry.answer)],
        },
        fallbacks=[
            CommandHandler("stop", callbacks.Home.stop),
            CallbackQueryHandler(callbacks.Home.stop)
        ],
        allow_reentry=True
    )
