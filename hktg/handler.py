
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
            State.END: [CallbackQueryHandler(callbacks.Home.stop),]
        },
        fallbacks=[
            CommandHandler("stop", callbacks.Home.stop),
            CallbackQueryHandler(callbacks.Home.stop),
            # CommandHandler("stop", stop_nested),
        ],

        map_to_parent={
            # After showing data return to top level menu
            # State.SHOWING: SHOWING,
            
            # Return to top level menu
            ConversationHandler.END: State.FILTERED_VIEW,
            # End conversation altogether
            # STOPPING: END,
        },
    )

    return ConversationHandler(
        entry_points=[CommandHandler("start", callbacks.Home.ask)],

        states={
            State.CHOOSING_ACTION: [CallbackQueryHandler(callbacks.Home.answer)],
            # State.CHOOSING_LOCATION: [CallbackQueryHandler(select_location.SelectLocation.answer)],
            State.CHOOSING_PRODUCT: [CallbackQueryHandler(callbacks.SelectProduct.answer)],
            State.CHOOSING_CONTAINER: [CallbackQueryHandler(callbacks.SelectContainer.answer)],
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
            State.FILTERED_VIEW: [CallbackQueryHandler(callbacks.FilteredView.answer)],
            State.VIEWING_ENTRY: [[entry_handler]] # CallbackQueryHandler(callbacks.ViewEntry.answer)],
        },
        fallbacks=[
            CommandHandler("stop", callbacks.Home.stop),
            CallbackQueryHandler(callbacks.Home.stop)
        ],
        allow_reentry=True
    )
