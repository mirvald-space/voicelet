import os
import threading
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType
from aiogram.filters import Command

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
    port = int(os.environ.get('PORT', 3000))
    httpd = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    logger.info(f"Starting HTTP server on port {port}")
    httpd.serve_forever()

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
