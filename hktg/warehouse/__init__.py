
from ._view_entry import ViewEntry
from ._select_container import SelectContainer
from ._select_product import SelectProduct
from ._select_location import SelectLocation
from ._ask_symbol import AskSymbol
from ._ask_amount import AskAmount
from ._view_product import ViewProduct
from ._view_products import ViewProducts

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

    entry_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(ViewEntry.ask)],

        states={
            State.VIEWING_ENTRY: [CallbackQueryHandler(ViewEntry.answer)],

            State.CHOOSING_LOCATION: [CallbackQueryHandler(SelectLocation.answer)],
            State.CHOOSING_PRODUCT: [CallbackQueryHandler(SelectProduct.answer)],
            State.CHOOSING_CONTAINER: [CallbackQueryHandler(SelectContainer.answer)],
            State.ENTERING_AMOUNT: [MessageHandler(filters.TEXT, AskAmount.answer)],
            State.ENTERING_SYMBOL: [MessageHandler(filters.TEXT & ~filters.COMMAND, AskSymbol.answer)],
            State.ENTERING_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, common.AskText.answer)],
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
            State.ENTERING_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, common.AskText.answer)],
        },
        fallbacks=[
            CallbackQueryHandler(home.Home.ask),
        ],

        map_to_parent={
            # State.VIEWING_ENTRY: State.VIEWING_ENTRY,
            State.CHOOSING_ACTION: State.CHOOSING_ACTION,
        },
    )
