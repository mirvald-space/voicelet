import speech_recognition as sr
from config import logger, LANGUAGES

def detect_language(recognizer, audio_data):
    """
    Attempts to determine the language of speech by checking recognition in multiple languages.
    
    Args:
        recognizer: Speech recognizer instance
        audio_data: Audio data to recognize
        
    Returns:
        tuple: (detected_language, recognized_text) or (None, None) if no language detected
    """
    results = {}
    
    for lang in LANGUAGES:
        try:
            text = recognizer.recognize_google(audio_data, language=lang)
            results[lang] = text
            logger.info(f"Recognized in {lang}: {text}")
        except sr.UnknownValueError:
            logger.info(f"Could not recognize audio in {lang}")
        except sr.RequestError:
            logger.error(f"Could not request results from Google Speech Recognition service for {lang}")
    
    # If recognized in multiple languages, choose based on result length
    # (usually the correct language gives a more complete recognition)
    if results:
        # Choose the language with the longest text result
        detected_lang = max(results.keys(), key=lambda k: len(results[k]))
        return detected_lang, results[detected_lang]
    
    return None, None

def prepare_recognizer():
    """
    Creates and configures a speech recognizer with optimal settings.
    
    Returns:
        sr.Recognizer: Configured speech recognizer
    """
    recognizer = sr.Recognizer()
    # Increase recognition sensitivity
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True
    return recognizer 