from telegram import Update
from telegram.ext import CallbackContext

from config import logger
from utils.database import Database

# Initialize database connection
db = Database()

def start_command(update: Update, context: CallbackContext) -> None:
    """
    Handle the /start command
    
    Args:
        update: Telegram update object
        context: Callback context
    """
    user = update.effective_user
    
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
    
    # Send welcome message
    welcome_message = (
        f"👋 Hello, {user.first_name}!\n\n"
        f"I'm Voicelet, a voice recognition bot that can convert your voice messages to text "
        f"with automatic language detection.\n\n"
        f"Just send me a voice message, and I'll transcribe it for you!"
    )
    
    update.message.reply_text(welcome_message) 