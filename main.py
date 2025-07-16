import os
import threading
import time
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram.ext import Updater, MessageHandler, CommandHandler, filters

from config import TELEGRAM_TOKEN, logger
from handlers import voice_handler, start_command, file_handler

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

def keep_alive():
    """Ping the server every 14 minutes to prevent Render from spinning down due to inactivity"""
    app_url = os.environ.get('APP_URL', 'https://your-app-url.onrender.com')
    
    while True:
        try:
            logger.info("Sending keep-alive ping")
            requests.get(app_url)
        except Exception as e:
            logger.error(f"Keep-alive ping failed: {e}")
        
        # Sleep for 1 hour (3600 seconds)
        time.sleep(3600)

def main() -> None:
    """
    Main function to start the bot
    """
    # Start HTTP server in a separate thread
    server_thread = threading.Thread(target=start_http_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Start the keep-alive pinger in a separate thread
    keep_alive_thread = threading.Thread(target=keep_alive)
    keep_alive_thread.daemon = True
    keep_alive_thread.start()

    # Create the updater using token from config
    updater = Updater(TELEGRAM_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start_command))

    # Register voice message handler
    dispatcher.add_handler(MessageHandler(filters.VOICE, voice_handler))
    
    # Register document/file handler for audio files
    dispatcher.add_handler(MessageHandler(filters.DOCUMENT, file_handler))

    # Start the bot
    logger.info("Starting the bot")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
