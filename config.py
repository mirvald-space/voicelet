import os
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Logging configuration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token from environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    logger.error("No TELEGRAM_TOKEN found in environment variables!")
    raise ValueError("TELEGRAM_TOKEN environment variable is required")

# Speech recognition settings
ENERGY_THRESHOLD = int(os.getenv("ENERGY_THRESHOLD", "300"))
LANGUAGES = os.getenv("LANGUAGES", "ru-RU,en-US").split(",")

# MongoDB configuration
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "voicelet_db")

# Language display names
LANGUAGE_NAMES = {
    'ru-RU': 'Russian',
    'en-US': 'English',
    'fr-FR': 'French',
    'de-DE': 'German',
    'es-ES': 'Spanish',
    'it-IT': 'Italian',
    'pt-PT': 'Portuguese',
    'nl-NL': 'Dutch',
    'pl-PL': 'Polish',
    'tr-TR': 'Turkish',
    'ar-SA': 'Arabic',
    'zh-CN': 'Chinese',
    'ja-JP': 'Japanese',
    'ko-KR': 'Korean'
} 