
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
        entry_points=[CallbackQueryHandler(callbacks.ViewWarehouse.answer)],

        states={
            State.VIEWING_WAREHOUSE: [CallbackQueryHandler(callbacks.ViewWarehouse.answer)],
            State.VIEWING_ENTRY: [CallbackQueryHandler(callbacks.ViewEntry.answer)],

            State.CHOOSING_LOCATION: [CallbackQueryHandler(callbacks.SelectLocation.answer)],
            State.CHOOSING_PRODUCT: [CallbackQueryHandler(callbacks.SelectProduct.answer)],
            State.CHOOSING_CONTAINER: [CallbackQueryHandler(callbacks.SelectContainer.answer)],
            State.ENTERING_AMOUNT: [MessageHandler(filters.TEXT, callbacks.AskAmount.answer)],
            State.ENTERING_SYMBOL: [MessageHandler(filters.TEXT & ~filters.COMMAND, callbacks.AskSymbol.answer)],
            State.ENTERING_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, callbacks.AskText.answer)],
        },
        fallbacks=[
            CallbackQueryHandler(callbacks.Home.ask),
            # CommandHandler("stop", stop_nested),
        ],

        map_to_parent={
            # After showing data return to top level menu
            # State.SHOWING: SHOWING,

            # Return to top level menu
            State.CHOOSING_ACTION: State.CHOOSING_ACTION,
            # End conversation altogether
            # STOPPING: END,
        },
    )


    # warehouse_handler = ConversationHandler(
    #     entry_points=[CallbackQueryHandler(callbacks.ViewWarehouse.ask)],

    #     states={
    #         State.VIEWING_ENTRY: [CallbackQueryHandler(callbacks.ViewEntry.ask)],
    #         State.CHOOSING_LOCATION: [CallbackQueryHandler(callbacks.SelectLocation.ask)],
    #         State.CHOOSING_PRODUCT: [CallbackQueryHandler(callbacks.SelectProduct.ask)],
    #         State.CHOOSING_CONTAINER: [CallbackQueryHandler(callbacks.SelectContainer.answer)],
    #     },
    #     fallbacks=[
    #         # CallbackQueryHandler(callbacks.Home.stop),
    #         # CommandHandler("stop", stop_nested),
    #     ],

    #     map_to_parent={
    #         State.CHOOSING_ACTION: State.CHOOSING_ACTION,
    #     },
    # )

    products_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(callbacks.ViewProducts.answer),
            CommandHandler('products', callbacks.ViewProducts.answer)
        ],

        states={
            State.VIEWING_PRODUCTS: [CallbackQueryHandler(callbacks.ViewProducts.answer)],
            State.VIEWING_PRODUCT: [CallbackQueryHandler(callbacks.ViewProduct.answer)],
            State.CHOOSING_CONTAINER: [CallbackQueryHandler(callbacks.SelectContainer.answer)],
            State.ENTERING_AMOUNT: [MessageHandler(filters.TEXT, callbacks.AskAmount.answer)],
            State.ENTERING_SYMBOL: [MessageHandler(filters.TEXT & ~filters.COMMAND, callbacks.AskSymbol.answer)],
            State.ENTERING_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, callbacks.AskText.answer)],
        },
        fallbacks=[
            CallbackQueryHandler(callbacks.Home.ask),
        ],

        map_to_parent={
            State.CHOOSING_ACTION: State.CHOOSING_ACTION,
        },
    )

    return ConversationHandler(
        name="Hell Kitchen Bot",
        entry_points=[CommandHandler("start", callbacks.Home.ask)],

        states={
            State.CHOOSING_ACTION: [ CallbackQueryHandler(callbacks.Home.answer) ],
            State.VIEWING_WAREHOUSE: [ entry_handler ],
            State.VIEWING_PRODUCTS: [ products_handler ],
            # State.VIEWING_ENTRY: [ entry_handler ] # CallbackQueryHandler(callbacks.ViewEntry.answer)],
        },
        fallbacks=[
            CommandHandler("stop", callbacks.Home.stop),
            CallbackQueryHandler(callbacks.Home.stop)
        ],
        allow_reentry=True
    )
