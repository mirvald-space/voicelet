import os
import threading
import time
import requests
import logging
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType
from aiogram.filters import Command, CommandStart

from config import TELEGRAM_TOKEN, logger
from handlers.voice import voice_handler
from handlers.commands import start_command
from handlers.file import file_handler

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

async def handle_start(message: types.Message):
    """Handler for /start command"""
    await start_command(message)

async def handle_voice(message: types.Message):
    """Handler for voice messages"""
    await voice_handler(message)

async def handle_file(message: types.Message):
    """Handler for document/file messages"""
    await file_handler(message)

async def main() -> None:
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

    # Initialize bot and dispatcher
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher()

    # Register command handlers
    dp.message.register(handle_start, Command(commands=["start"]))

    # Register voice message handler
    dp.message.register(handle_voice, lambda message: message.content_type == ContentType.VOICE)
    
    # Register document/file handler for audio files
    dp.message.register(handle_file, lambda message: message.content_type == ContentType.DOCUMENT)

    # Start the bot
    logger.info("Starting the bot")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
