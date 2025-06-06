import os
import uuid
from pydub import AudioSegment
from telegram import Update, ParseMode
from telegram.ext import CallbackContext

from config import logger, LANGUAGE_NAMES
from utils.speech import detect_language, prepare_recognizer
from utils.database import Database
import speech_recognition as sr

# Initialize database
db = Database()

def voice_handler(update: Update, context: CallbackContext) -> None:
    """
    Handles voice messages by converting them to text using speech recognition.
    
    Args:
        update: Telegram update object
        context: Callback context
    """
    # Generate unique file identifiers for concurrent processing
    file_id = str(uuid.uuid4())
    temp_ogg_path = f'temp_voice_{file_id}.ogg'
    temp_wav_path = f'temp_voice_{file_id}.wav'
    
    # Send a message to inform the user that processing is underway
    processing_message = update.message.reply_text(
        "🔄 *Processing voice message...*\n\n"
        "Please wait. Transcription may take some time.",
        parse_mode=ParseMode.MARKDOWN
    )
    
    # Get the voice message file
    file = update.message.voice.get_file()
    file.download(temp_ogg_path)

    try:
        # Convert OGG to WAV
        audio = AudioSegment.from_ogg(temp_ogg_path)
        # Normalize audio for better quality
        audio = audio.normalize()
        audio.export(temp_wav_path, format='wav')

        # Use speech_recognition for speech to text conversion
        recognizer = prepare_recognizer()
        with sr.AudioFile(temp_wav_path) as source:
            # Improve recognition by adjusting for ambient noise
            recognizer.adjust_for_ambient_noise(source)
            audio_data = recognizer.record(source)
            
            # Try to detect language automatically
            lang, text = detect_language(recognizer, audio_data)
            
            if text:
                # Increment transcription count for this user
                user_id = update.effective_user.id
                new_count = db.increment_transcription_count(user_id)
                
                language_name = LANGUAGE_NAMES.get(lang, lang)
                
                # Format the response message
                response = (
                    f"🎙 *Speech Recognition Results*\n\n"
                    f"🌍 *Language detected:* {language_name}\n\n"
                    f"📝 *Transcript:*\n"
                    f"\"{text}\"\n\n"
                    f"_Audio duration: {update.message.voice.duration}s_\n"
                    f"_Your transcription count: {new_count}_"
                )
                
                # Delete the processing message and send the result
                processing_message.delete()
                update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)
                logger.info(f"Successfully recognized speech in {language_name} for user {update.effective_user.id}")
            else:
                error_message = (
                    f"⚠️ *Speech Recognition Failed*\n\n"
                    f"I couldn't recognize any speech in your audio message. "
                    f"Please try again with a clearer voice recording, or check the following:\n\n"
                    f"• Speak clearly and not too quickly\n"
                    f"• Avoid background noise\n"
                    f"• Make sure your message contains speech\n"
                    f"• Try recording a slightly longer message\n"
                    f"• You can also try sending an audio file instead"
                )
                # Delete the processing message and send the error
                processing_message.delete()
                update.message.reply_text(error_message, parse_mode=ParseMode.MARKDOWN)
                logger.warning(f"Failed to recognize speech - no text detected for user {update.effective_user.id}")
                
    except Exception as e:
        error_message = (
            f"❌ *Error Processing Audio*\n\n"
            f"Sorry, I encountered a problem while processing your voice message. "
            f"Please try again later or try sending an audio file instead.\n\n"
            f"_Technical details: {str(e)}_"
        )
        # Try to delete the processing message if it exists and send the error
        try:
            processing_message.delete()
        except:
            pass
        update.message.reply_text(error_message, parse_mode=ParseMode.MARKDOWN)
        logger.error(f"Error in voice recognition for user {update.effective_user.id}: {e}")
        
    finally:
        # Clean up temporary files
        try:
            os.remove(temp_ogg_path)
            os.remove(temp_wav_path)
        except Exception as e:
            logger.error(f"Error cleaning up temporary files for user {update.effective_user.id}: {e}") 