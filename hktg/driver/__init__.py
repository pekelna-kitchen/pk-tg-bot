
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

    return ConversationHandler(
        entry_points=[CallbackQueryHandler(ViewMap.answer)],

        states={
            State.VIEWING_MAP: [CallbackQueryHandler(ViewMap.answer)],

            # State.CHOOSING_LOCATION: [CallbackQueryHandler(SelectLocation.answer)],
            # State.CHOOSING_PRODUCT: [CallbackQueryHandler(SelectProduct.answer)],
            # State.CHOOSING_CONTAINER: [CallbackQueryHandler(SelectContainer.answer)],
            # State.ENTERING_AMOUNT: [MessageHandler(filters.TEXT, AskAmount.answer)],
            # State.ENTERING_SYMBOL: [MessageHandler(filters.TEXT & ~filters.COMMAND, AskSymbol.answer)],
            # State.ENTERING_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, AskText.answer)],
        },
        fallbacks=[
            CallbackQueryHandler(home.Home.ask),
        ],

        map_to_parent={
            State.CHOOSING_ACTION: State.CHOOSING_ACTION,
            State.VIEWING_MAP: State.VIEWING_MAP,
        },
    )
