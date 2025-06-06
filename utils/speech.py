import speech_recognition as sr
from config import logger, LANGUAGES, ENERGY_THRESHOLD

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
    
    # Choose the language with the longest recognized text (often the correct one)
    if results:
        # Sort by text length, descending
        sorted_results = sorted(results.items(), key=lambda x: len(x[1]), reverse=True)
        detected_lang, text = sorted_results[0]
        return detected_lang, text
    
    return None, None

def prepare_recognizer():
    """
    Prepares a speech recognizer with optimal settings
    
    Returns:
        Speech recognizer instance
    """
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = ENERGY_THRESHOLD  # Default energy threshold
    recognizer.dynamic_energy_threshold = True
    recognizer.dynamic_energy_adjustment_damping = 0.15
    recognizer.dynamic_energy_ratio = 1.5
    recognizer.pause_threshold = 0.8  # Seconds of non-speaking audio before a phrase is considered complete
    return recognizer 