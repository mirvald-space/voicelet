import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

from config import TELEGRAM_TOKEN, logger
from handlers import voice_handler, start_command

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Telegram Bot is running!')

def start_http_server():
    port = int(os.environ.get('PORT', 8080))
    httpd = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    logger.info(f"Starting HTTP server on port {port}")
    httpd.serve_forever()

def main() -> None:
    """
    Main function to start the bot
    """
    # Start HTTP server in a separate thread
    server_thread = threading.Thread(target=start_http_server)
    server_thread.daemon = True
    server_thread.start()

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
