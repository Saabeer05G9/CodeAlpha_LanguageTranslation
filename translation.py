"""
CodeAlpha AI Internship — Task 1: Language Translation Tool
Module: translation.py

This module contains the core translation engine and language configuration.
It keeps the translation business logic separate from any user interface (Gradio/Web).
"""

import os
import tempfile
from typing import Tuple, Dict, Optional
from deep_translator import GoogleTranslator, MyMemoryTranslator
from deep_translator.exceptions import (
    TooManyRequests,
    LanguageNotSupportedException,
    TranslationNotFound,
    RequestError
)
from gtts import gTTS

# -------------------------------------------------------------------------
# Language Configuration
# -------------------------------------------------------------------------
# Supported language names mapped to standard ISO language codes for GoogleTranslator.
# Includes all 15 required languages specified by the internship task.
SUPPORTED_LANGUAGES: Dict[str, str] = {
    "English": "en",
    "Telugu": "te",
    "Hindi": "hi",
    "Tamil": "ta",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Bengali": "bn",
    "Gujarati": "gu",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Japanese": "ja",
    "Chinese": "zh-CN",
    "Arabic": "ar"
}

# Source languages: includes "Auto Detect" to automatically detect the input language.
SOURCE_LANGUAGES: Dict[str, str] = {
    "Auto Detect": "auto",
    **SUPPORTED_LANGUAGES
}

# Target languages: cannot be "auto", must be a specific target language.
TARGET_LANGUAGES: Dict[str, str] = SUPPORTED_LANGUAGES

# Secondary mapping for MyMemoryTranslator as a reliable fallback
# when Google Translate scraping is rate-limited (HTTP 429) on certain IPs.
_MYMEMORY_CODE_MAP: Dict[str, str] = {
    "auto": "autodetect",
    "en": "en-GB",
    "te": "te-IN",
    "hi": "hi-IN",
    "ta": "ta-IN",
    "kn": "kn-IN",
    "ml": "ml-IN",
    "mr": "mr-IN",
    "bn": "bn-IN",
    "gu": "gu-IN",
    "es": "es-ES",
    "fr": "fr-FR",
    "de": "de-DE",
    "ja": "ja-JP",
    "zh-CN": "zh-CN",
    "ar": "ar-SA"
}

# Maximum character limit allowed for a single translation request
MAX_CHAR_LIMIT = 5000


# -------------------------------------------------------------------------
# Helper Functions
# -------------------------------------------------------------------------
def get_language_code(language_name_or_code: str, is_source: bool = False) -> str:
    """
    Converts a friendly language name (e.g. 'Telugu') or code (e.g. 'te')
    into a valid language code accepted by the translation library.
    
    Parameters:
        language_name_or_code (str): The language name or code.
        is_source (bool): True if looking up a source language (supports 'auto').
        
    Returns:
        str: ISO language code (e.g., 'te', 'en', 'auto').
        
    Raises:
        ValueError: If the language is not recognized or supported.
    """
    if not language_name_or_code:
        raise ValueError("Language selection cannot be empty.")

    clean_name = language_name_or_code.strip()

    # If it's already a code in our dictionary values
    valid_codes = set(SOURCE_LANGUAGES.values()) if is_source else set(TARGET_LANGUAGES.values())
    if clean_name.lower() in [code.lower() for code in valid_codes]:
        return clean_name

    # Check against friendly names in our dictionary
    lang_dict = SOURCE_LANGUAGES if is_source else TARGET_LANGUAGES
    for name, code in lang_dict.items():
        if name.lower() == clean_name.lower():
            return code

    raise ValueError(f"Unsupported language: '{language_name_or_code}'.")


def count_text_stats(text: str) -> Tuple[int, int]:
    """
    Computes character count and word count for a given string.
    
    Parameters:
        text (str): Input text.
        
    Returns:
        Tuple[int, int]: (character_count, word_count)
    """
    if not text:
        return 0, 0
    char_count = len(text)
    word_count = len(text.split())
    return char_count, word_count


# -------------------------------------------------------------------------
# Core Translation Function
# -------------------------------------------------------------------------
def translate_text(
    text: str,
    source_language: str = "Auto Detect",
    target_language: str = "Telugu"
) -> str:
    """
    Translates input text from source language to target language.
    
    Workflow:
    1. Validates input text (empty check, length check).
    2. Resolves human-readable language names to ISO codes.
    3. Handles identity translation (same source and target language).
    4. Calls GoogleTranslator via deep-translator.
    5. Gracefully falls back to MyMemoryTranslator if Google rate-limits (HTTP 429).
    6. Catches all exceptions to ensure the UI never crashes.
    
    Parameters:
        text (str): The text to translate.
        source_language (str): Source language name or code (default: 'Auto Detect').
        target_language (str): Target language name or code (default: 'Telugu').
        
    Returns:
        str: The translated text, or a user-friendly error message.
    """
    # 1. Validation: Empty or whitespace input
    if text is None or not text.strip():
        return ""

    clean_text = text.strip()

    # 2. Validation: Character limit check
    if len(clean_text) > MAX_CHAR_LIMIT:
        return f"Error: Input exceeds maximum character limit of {MAX_CHAR_LIMIT} characters."

    # 3. Resolve language codes
    try:
        source_code = get_language_code(source_language, is_source=True)
        target_code = get_language_code(target_language, is_source=False)
    except ValueError as val_err:
        return f"Language Error: {str(val_err)}"

    # 4. Identity Check: If source and target are identical
    if source_code != "auto" and source_code.lower() == target_code.lower():
        return clean_text

    # 5. Perform Translation with Fallback Handling
    try:
        # Primary Engine: GoogleTranslator
        translator = GoogleTranslator(source=source_code, target=target_code)
        translated = translator.translate(clean_text)
        return translated if translated is not None else ""

    except TooManyRequests:
        # Fallback Engine: MyMemoryTranslator when Google rate-limits
        try:
            mem_src = _MYMEMORY_CODE_MAP.get(source_code, source_code)
            mem_tgt = _MYMEMORY_CODE_MAP.get(target_code, target_code)
            fallback_translator = MyMemoryTranslator(source=mem_src, target=mem_tgt)
            fallback_translated = fallback_translator.translate(clean_text)
            return fallback_translated if fallback_translated is not None else ""
        except Exception as fallback_err:
            return f"Translation Service Unavailable: {str(fallback_err)}"

    except (LanguageNotSupportedException, TranslationNotFound) as specific_err:
        return f"Translation Error: {str(specific_err)}"

    except RequestError as req_err:
        return f"Network Error: Unable to reach translation server. ({str(req_err)})"

    except Exception as general_err:
        # Catch-all to guarantee UI never crashes
        return f"Unexpected Error: {str(general_err)}"


# -------------------------------------------------------------------------
# Text-to-Speech (TTS) Function
# -------------------------------------------------------------------------
def generate_tts_audio(text: str, target_language: str = "Telugu") -> Optional[str]:
    """
    Synthesizes speech from translated text using Google Text-to-Speech (gTTS).
    
    Parameters:
        text (str): Text to convert to speech.
        target_language (str): Target language name or ISO code.
        
    Returns:
        Optional[str]: Filepath to the generated .mp3 file, or None if text is empty/unsupported.
    """
    if not text or not text.strip():
        return None

    clean_text = text.strip()

    # Do not attempt TTS on error messages
    if clean_text.startswith("Error:") or clean_text.startswith("Language Error:") or clean_text.startswith("Translation Error:"):
        return None

    try:
        lang_code = get_language_code(target_language, is_source=False)
        # gTTS supports all our 15 ISO language codes
        tts = gTTS(text=clean_text, lang=lang_code, slow=False)
        
        # Save audio file to a temporary file
        temp_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        temp_file_path = temp_file.name
        temp_file.close()
        
        tts.save(temp_file_path)
        return temp_file_path
    except Exception as e:
        print(f"[TTS Warning]: Could not generate audio for '{clean_text[:20]}...': {e}")
        return None

