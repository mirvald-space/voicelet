import os
from pydub import AudioSegment
from telegram import Update, ParseMode
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

        # Use speech_recognition for speech to text conversion
        recognizer = prepare_recognizer()
        with sr.AudioFile('voice.wav') as source:
            # Improve recognition by adjusting for ambient noise
            recognizer.adjust_for_ambient_noise(source)
            audio_data = recognizer.record(source)
            
            # Try to detect language automatically
            lang, text = detect_language(recognizer, audio_data)
            
            if text:
                language_name = LANGUAGE_NAMES.get(lang, lang)
                
                # Format the response message
                response = (
                    f"🎙 *Speech Recognition Results*\n\n"
                    f"🌍 *Language detected:* {language_name}\n\n"
                    f"📝 *Transcript:*\n"
                    f"\"{text}\"\n\n"
                    f"_Processing time: {update.message.voice.duration}s_"
                )
                
                update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)
                logger.info(f"Successfully recognized speech in {language_name}")
            else:
                error_message = (
                    f"⚠️ *Speech Recognition Failed*\n\n"
                    f"I couldn't recognize any speech in your audio message. "
                    f"Please try again with a clearer voice recording, or check the following:\n\n"
                    f"• Speak clearly and not too quickly\n"
                    f"• Avoid background noise\n"
                    f"• Make sure your message contains speech\n"
                    f"• Try recording a slightly longer message"
                )
                update.message.reply_text(error_message, parse_mode=ParseMode.MARKDOWN)
                logger.warning("Failed to recognize speech - no text detected")
                
    except Exception as e:
        error_message = (
            f"❌ *Error Processing Audio*\n\n"
            f"Sorry, I encountered a problem while processing your voice message. "
            f"Please try again later.\n\n"
            f"_Technical details: {str(e)}_"
        )
        update.message.reply_text(error_message, parse_mode=ParseMode.MARKDOWN)
        logger.error(f"Error in voice recognition: {e}")
        
    finally:
        # Clean up temporary files
        try:
            os.remove('voice.ogg')
            os.remove('voice.wav')
        except:
            pass 