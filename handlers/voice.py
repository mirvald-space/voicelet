import os
from pydub import AudioSegment
from telegram import Update
from telegram.ext import CallbackContext

from config import logger, LANGUAGE_NAMES
from utils.speech import detect_language, prepare_recognizer
import speech_recognition as sr

def voice_handler(update: Update, context: CallbackContext) -> None:
    """
    Handles voice messages by converting them to text using speech recognition.
    
    Args:
        update: Telegram update object
        context: Callback context
    """
    # Get the voice message file
    file = update.message.voice.get_file()
    file.download('voice.ogg')

    try:
        # Convert OGG to WAV
        audio = AudioSegment.from_ogg('voice.ogg')
        # Normalize audio for better quality
        audio = audio.normalize()
        audio.export('voice.wav', format='wav')

        # Use speech_recognition for speech recognition
        recognizer = prepare_recognizer()
        
        with sr.AudioFile('voice.wav') as source:
            # Apply noise reduction
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio_data = recognizer.record(source)
            
            # Automatic language detection
            detected_lang, text = detect_language(recognizer, audio_data)
            
            if detected_lang:
                lang_name = LANGUAGE_NAMES.get(detected_lang, detected_lang)
                update.message.reply_text(f'Detected {lang_name} language: {text}')
            else:
                update.message.reply_text('Could not recognize speech in any supported language')
    except Exception as e:
        logger.error(f"Error in voice recognition: {e}")
        update.message.reply_text('Error in speech recognition')
    finally:
        # Delete temporary files
        if os.path.exists('voice.ogg'):
            os.remove('voice.ogg')
        if os.path.exists('voice.wav'):
            os.remove('voice.wav') 