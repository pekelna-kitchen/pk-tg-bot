#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position

import logging
import os
import traceback
import html
import json
from hktg import handler, util

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, ContextTypes, DictPersistence

# from telegram.ext import Application

# shut up, warning!

from warnings import filterwarnings
from telegram.warnings import PTBUserWarning
filterwarnings(action="ignore", message=r".*CallbackQueryHandler",
               category=PTBUserWarning)

TG_TOKEN = os.environ["TG_TOKEN"]
PORT = int(os.environ.get('PORT', '8443'))
DEVELOPER_CHAT_ID=os.environ.get('DEVELOPER_CHAT_ID')

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__, limit=5, chain=False)
    tb_string = "\n".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    update_str = json.dumps(update.to_dict(), cls=util.EnhancedJSONEncoder, indent=2, ensure_ascii=False) if isinstance(update, Update) else update.__class__.__name__
    # str(update)
    message = (
        f"An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(str(update_str))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )

    # Finally, send the message
    await context.bot.send_message(
        chat_id=DEVELOPER_CHAT_ID, text=message, parse_mode=ParseMode.HTML
    )

def main() -> None:
    application = Application.builder().token(TG_TOKEN).arbitrary_callback_data(True).build()

    application.add_handler(handler.get())

    application.add_error_handler(error_handler)
    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
