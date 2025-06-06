from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

from config import TELEGRAM_TOKEN, logger
from handlers import voice_handler, start_command

def main() -> None:
    """
    Main function to start the bot
    """
    # Create the updater using token from config
    updater = Updater(TELEGRAM_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start_command))

    # Register voice message handler
    dispatcher.add_handler(MessageHandler(Filters.voice, voice_handler))

    # Start the bot
    logger.info("Starting the bot")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
