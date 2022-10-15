
from ._view_map import ViewMap

from telegram.ext import (
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)

def get_handler():

    from hktg.constants import State
    from hktg import home

    entry_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(ViewMap.answer)],

        states={
            State.VIEWING_MAP: [CallbackQueryHandler(ViewMap.answer)],

            State.CHOOSING_LOCATION: [CallbackQueryHandler(SelectLocation.answer)],
            State.CHOOSING_PRODUCT: [CallbackQueryHandler(SelectProduct.answer)],
            State.CHOOSING_CONTAINER: [CallbackQueryHandler(SelectContainer.answer)],
            State.ENTERING_AMOUNT: [MessageHandler(filters.TEXT, AskAmount.answer)],
            State.ENTERING_SYMBOL: [MessageHandler(filters.TEXT & ~filters.COMMAND, AskSymbol.answer)],
            State.ENTERING_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, AskText.answer)],
        },
        fallbacks=[
            CallbackQueryHandler(home.Home.ask),
        ],

        map_to_parent={
            State.CHOOSING_ACTION: State.CHOOSING_ACTION,
            State.VIEWING_PRODUCT: State.VIEWING_PRODUCT,
        },
    )

    return ConversationHandler(
        entry_points=[
            CallbackQueryHandler(ViewProducts.answer),
            CommandHandler('products', ViewProducts.answer)
        ],

        states={
            State.VIEWING_PRODUCTS: [CallbackQueryHandler(ViewProducts.answer)],
            State.VIEWING_PRODUCT: [CallbackQueryHandler(ViewProduct.answer)],
            State.VIEWING_ENTRY: [ entry_handler ],
            State.CHOOSING_CONTAINER: [CallbackQueryHandler(SelectContainer.answer)],
            State.ENTERING_AMOUNT: [MessageHandler(filters.TEXT, AskAmount.answer)],
            State.ENTERING_SYMBOL: [MessageHandler(filters.TEXT & ~filters.COMMAND, AskSymbol.answer)],
            State.ENTERING_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, AskText.answer)],
        },
        fallbacks=[
            CallbackQueryHandler(home.Home.ask),
        ],

        map_to_parent={
            # State.VIEWING_ENTRY: State.VIEWING_ENTRY,
            State.CHOOSING_ACTION: State.CHOOSING_ACTION,
        },
    )
