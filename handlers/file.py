import os
import uuid
import mimetypes
from pydub import AudioSegment
from aiogram import types

from config import logger, LANGUAGE_NAMES
from utils.speech import detect_language, prepare_recognizer
from utils.database import Database
import speech_recognition as sr

# Define supported audio formats
SUPPORTED_FORMATS = ['.ogg', '.flac', '.wav', '.mp3']

# Initialize database
db = Database()

async def file_handler(message: types.Message) -> None:
    """
    Handles audio file messages by converting them to text using speech recognition.
    Supports .ogg, .flac, .wav, and .mp3 formats.
    
    Args:
        message: Message object from aiogram
    """
    # Check if the message contains a document
    if not message.document:
        return
    
    # Get file information
    file = message.document
    file_name = file.file_name if file.file_name else "audio"
    file_ext = os.path.splitext(file_name)[1].lower()
    
    # Check if the file is a supported audio format
    if file_ext not in SUPPORTED_FORMATS:
        await message.reply(
            f"❌ *Unsupported File Format*\n\n"
            f"This file format is not supported. Please send an audio file in one of the following formats:\n"
            f"• .ogg (Voice Message)\n"
            f"• .flac\n"
            f"• .wav\n"
            f"• .mp3",
            parse_mode="Markdown"
        )
        return
    
    # Generate unique file identifiers for concurrent processing
    file_id = str(uuid.uuid4())
    temp_audio_path = f'temp_audio_{file_id}{file_ext}'
    temp_wav_path = f'temp_audio_{file_id}.wav'
    
    # Send a message to inform the user that processing is underway
    processing_message = await message.reply(
        "🔄 *Processing audio file...*\n\n"
        "Please wait. Transcription may take some time.",
        parse_mode="Markdown"
    )
    
    try:
        # Download the file
        await message.bot.download(
            message.document,
            destination=temp_audio_path
        )
        
        # Convert to WAV for processing
        if file_ext == '.mp3':
            audio = AudioSegment.from_mp3(temp_audio_path)
        elif file_ext == '.ogg':
            audio = AudioSegment.from_ogg(temp_audio_path)
        elif file_ext == '.flac':
            audio = AudioSegment.from_file(temp_audio_path, format='flac')
        elif file_ext == '.wav':
            audio = AudioSegment.from_wav(temp_audio_path)
        
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
                user_id = message.from_user.id
                new_count = db.increment_transcription_count(user_id)
                
                language_name = LANGUAGE_NAMES.get(lang, lang)
                
                # Format the response message
                response = (
                    f"🎙 *Speech Recognition Results*\n\n"
                    f"🌍 *Language detected:* {language_name}\n\n"
                    f"📝 *Transcript:*\n"
                    f"\"{text}\"\n\n"
                    f"_File format: {file_ext}_\n"
                    f"_Your transcription count: {new_count}_"
                )
                
                # Delete the processing message and send the result
                await message.bot.delete_message(chat_id=message.chat.id, message_id=processing_message.message_id)
                await message.reply(response, parse_mode="Markdown")
                logger.info(f"Successfully recognized speech in {language_name} from {file_ext} file for user {message.from_user.id}")
            else:
                error_message = (
                    f"⚠️ *Speech Recognition Failed*\n\n"
                    f"I couldn't recognize any speech in your audio file. "
                    f"Please try again with a clearer audio recording, or check the following:\n\n"
                    f"• Ensure the audio contains clear speech\n"
                    f"• Check that the file isn't corrupted\n"
                    f"• Try a different audio format\n"
                    f"• Make sure the audio is not too short"
                )
                # Delete the processing message and send the error
                await message.bot.delete_message(chat_id=message.chat.id, message_id=processing_message.message_id)
                await message.reply(error_message, parse_mode="Markdown")
                logger.warning(f"Failed to recognize speech in {file_ext} file - no text detected for user {message.from_user.id}")
                
    except Exception as e:
        error_message = (
            f"❌ *Error Processing Audio*\n\n"
            f"Sorry, I encountered a problem while processing your audio file. "
            f"Please try again with a different file or format.\n\n"
            f"_Technical details: {str(e)}_"
        )
        # Try to delete the processing message if it exists and send the error
        try:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=processing_message.message_id)
        except:
            pass
        await message.reply(error_message, parse_mode="Markdown")
        logger.error(f"Error in audio file recognition for user {message.from_user.id}: {e}")
        
    finally:
        # Clean up temporary files
        try:
            os.remove(temp_audio_path)
            os.remove(temp_wav_path)
        except Exception as e:
            logger.error(f"Error cleaning up temporary files for user {message.from_user.id}: {e}") 