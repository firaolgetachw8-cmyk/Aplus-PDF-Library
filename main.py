`python
import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)
from telegram.constants import ParseMode

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(name)

# NOTE: BOT_TOKEN fi database (db) koodii kee isa durii keessaa kan fudhataman ta'u qabu.
# Bot token kee asitti ykn environment variable irraa akka dhiyaate mirkaneessi.
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# ==========================================
# APPLICATION ENTRYPOINT
# ==========================================

def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    # Commands
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("library", library_command))
    application.add_handler(CommandHandler("admin", admin_command))

    # Callback Queries (Inline buttons)
    application.add_handler(CallbackQueryHandler(handle_callback_query))

    # Admin PDF Upload
    application.add_handler(
        MessageHandler(filters.Document.PDF, handle_document_upload)
    )

    # Text Messages (Registration password input)
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message)
    )

    logger.info("A PLUS PDF LIBRARY Bot started successfully.")
    application.run_polling(drop_pending_updates=True)


if name == "main":
    main()
