
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

from hktg import dbwrapper, warehouse, home
from hktg.constants import *

def get():

    entry_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(warehouse.ViewEntry.answer)],

        states={
            State.VIEWING_ENTRY: [CallbackQueryHandler(warehouse.ViewEntry.answer)],

            State.CHOOSING_LOCATION: [CallbackQueryHandler(warehouse.SelectLocation.answer)],
            State.CHOOSING_PRODUCT: [CallbackQueryHandler(warehouse.SelectProduct.answer)],
            State.CHOOSING_CONTAINER: [CallbackQueryHandler(warehouse.SelectContainer.answer)],
            State.ENTERING_AMOUNT: [MessageHandler(filters.TEXT, warehouse.AskAmount.answer)],
            State.ENTERING_SYMBOL: [MessageHandler(filters.TEXT & ~filters.COMMAND, warehouse.AskSymbol.answer)],
            State.ENTERING_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, warehouse.AskText.answer)],
        },
        fallbacks=[
            CallbackQueryHandler(home.Home.ask),
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

    products_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(warehouse.ViewProducts.answer),
            CommandHandler('products', warehouse.ViewProducts.answer)
        ],

        states={
            State.VIEWING_PRODUCTS: [CallbackQueryHandler(warehouse.ViewProducts.answer)],
            State.VIEWING_PRODUCT: [CallbackQueryHandler(warehouse.ViewProduct.answer)],
            State.CHOOSING_CONTAINER: [CallbackQueryHandler(warehouse.SelectContainer.answer)],
            State.ENTERING_AMOUNT: [MessageHandler(filters.TEXT, warehouse.AskAmount.answer)],
            State.ENTERING_SYMBOL: [MessageHandler(filters.TEXT & ~filters.COMMAND, warehouse.AskSymbol.answer)],
            State.ENTERING_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, warehouse.AskText.answer)],
        },
        fallbacks=[
            CallbackQueryHandler(home.Home.ask),
        ],

        map_to_parent={
            State.CHOOSING_ACTION: State.CHOOSING_ACTION,
        },
    )

    return ConversationHandler(
        name="Hell Kitchen Bot",
        entry_points=[CommandHandler("start", home.Home.ask)],

        states={
            State.CHOOSING_ACTION: [ CallbackQueryHandler(home.Home.answer) ],
            State.VIEWING_WAREHOUSE: [ entry_handler ],
            State.VIEWING_PRODUCTS: [ products_handler ],
            # State.VIEWING_ENTRY: [ entry_handler ] # CallbackQueryHandler(warehouse.ViewEntry.answer)],
        },
        fallbacks=[
            CommandHandler("stop", home.Home.stop),
            CallbackQueryHandler(home.Home.stop)
        ],
        allow_reentry=True
    )
