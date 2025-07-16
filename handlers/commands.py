from aiogram import types

from config import logger
from utils.database import Database

# Initialize database connection
db = Database()

async def start_command(message: types.Message) -> None:
    """
    Handle the /start command
    
    Args:
        message: Message object from aiogram
    """
    user = message.from_user
    
    # Store user in database
    if user:
        user_data = {
            'user_id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'language_code': user.language_code
        }
        
        db.add_user(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            language_code=user.language_code
        )
        
        logger.info(f"User started the bot: {user.first_name} (@{user.username})")
    
    # Send welcome message with formatting
    welcome_message = (
        f"👋 Hello, {user.first_name}! I'm your voice recognition assistant.\n\n"
        f"Simply send me a voice message or audio file (OGG, MP3, WAV, FLAC) and I'll convert it to text with automatic language detection.\n\n"
        f"Check out my other bot @Vidzillabot for downloading videos from social networks!"
    )
    
    await message.reply(welcome_message, parse_mode="Markdown") 