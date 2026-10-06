"""
AI Language Translation Tool
Module: translation.py

This module contains the core translation engine and language configuration.
It keeps the translation business logic separate from any user interface (Gradio/Web).
Supports 130+ languages dynamically via GoogleTranslator and MyMemoryTranslator fallback.
"""

import os
import tempfile
from typing import Tuple, Dict, Optional, List
from deep_translator import GoogleTranslator, MyMemoryTranslator
from deep_translator.exceptions import (
    TooManyRequests,
    LanguageNotSupportedException,
    TranslationNotFound,
    RequestError
)
from gtts import gTTS

# -------------------------------------------------------------------------
# Dynamic Language Configuration (130+ Languages)
# -------------------------------------------------------------------------

# Retrieve native list of all 133 supported languages from deep-translator
_RAW_GOOGLE_LANGS: Dict[str, str] = GoogleTranslator().get_supported_languages(as_dict=True)

def _format_display_name(raw_name: str) -> str:
    """
    Formats raw deep-translator language keys into clean, professional title case.
    E.g., 'chinese (simplified)' -> 'Chinese (Simplified)'
    """
    return " ".join(
        part.capitalize() if not part.startswith("(") else f"({part[1:].capitalize()}"
        for part in raw_name.split()
    )

# Curated priority languages placed at the top of dropdown menus for fast access
_PRIORITY_ORDER: List[str] = [
    "English",
    "Telugu",
    "Hindi",
    "Tamil",
    "Kannada",
    "Malayalam",
    "Marathi",
    "Bengali",
    "Gujarati",
    "Punjabi",
    "Urdu",
    "Spanish",
    "French",
    "German",
    "Italian",
    "Portuguese",
    "Russian",
    "Japanese",
    "Chinese (Simplified)",
    "Chinese (Traditional)",
    "Korean",
    "Arabic",
    "Turkish",
    "Dutch",
    "Vietnamese",
    "Thai",
    "Indonesian",
]

# Formatted full dictionary: Display Name -> ISO language code
_FORMATTED_ALL_LANGS: Dict[str, str] = {
    _format_display_name(k): v for k, v in _RAW_GOOGLE_LANGS.items()
}

# Construct SUPPORTED_LANGUAGES: priority languages first, then remainder alphabetically
SUPPORTED_LANGUAGES: Dict[str, str] = {}
for lang in _PRIORITY_ORDER:
    if lang in _FORMATTED_ALL_LANGS:
        SUPPORTED_LANGUAGES[lang] = _FORMATTED_ALL_LANGS[lang]

for lang in sorted(_FORMATTED_ALL_LANGS.keys()):
    if lang not in SUPPORTED_LANGUAGES:
        SUPPORTED_LANGUAGES[lang] = _FORMATTED_ALL_LANGS[lang]

# Source languages: includes "Auto Detect" as first option
SOURCE_LANGUAGES: Dict[str, str] = {
    "Auto Detect": "auto",
    **SUPPORTED_LANGUAGES
}

# Target languages: all 133 supported languages
TARGET_LANGUAGES: Dict[str, str] = SUPPORTED_LANGUAGES

# Fast normalized lookup maps for robust resolution
_NORMALIZED_NAME_TO_CODE: Dict[str, str] = {
    name.lower().strip(): code for name, code in SUPPORTED_LANGUAGES.items()
}
for raw_k, code in _RAW_GOOGLE_LANGS.items():
    _NORMALIZED_NAME_TO_CODE[raw_k.lower().strip()] = code

# Common language aliases and shortcuts
_NORMALIZED_NAME_TO_CODE.update({
    "chinese": "zh-CN",
    "kurdish": "ckb",
    "odia": "or",
    "oriya": "or",
    "manipuri": "mni-Mtei",
    "auto": "auto",
    "autodetect": "auto",
    "auto detect": "auto",
})

# Code to display name lookup map
_CODE_TO_NAME: Dict[str, str] = {
    code.lower(): name for name, code in SUPPORTED_LANGUAGES.items()
}
_CODE_TO_NAME["auto"] = "Auto Detect"

# Fallback mapping for MyMemoryTranslator when Google rate-limits
_MYMEMORY_LANGUAGE_NAME_MAP: Dict[str, str] = {
    "aymara": "central aymara",
    "chichewa": "nyanja",
    "chinese (simplified)": "chinese simplified",
    "chinese (traditional)": "chinese traditional",
    "dhivehi": "maldivian",
    "haitian creole": "haitian creole french",
    "igbo": "igbo ig",
    "irish": "irish gaelic",
    "kurdish (kurmanji)": "northern kurdish",
    "kurdish (sorani)": "kurdish sorani",
    "meiteilon (manipuri)": "manipuri",
    "myanmar": "burmese",
    "norwegian": "norwegian bokmål",
    "odia (oriya)": "odia",
    "oromo": "west central oromo",
    "sepedi": "sesotho",
    "serbian": "serbian cyrillic",
    "sindhi": "sindhi sd",
    "tamil": "tamil india",
    "uyghur": "uyghur ug",
}

# Supported TTS language codes lookup
try:
    from gtts.lang import tts_langs
    _TTS_SUPPORTED_CODES = set(tts_langs().keys())
except Exception:
    _TTS_SUPPORTED_CODES = set()

# Maximum character limit allowed for a single translation request
MAX_CHAR_LIMIT = 5000


# -------------------------------------------------------------------------
# Helper Functions
# -------------------------------------------------------------------------
def get_language_code(language_name_or_code: str, is_source: bool = False) -> str:
    """
    Converts a friendly language name (e.g. 'Telugu', 'Russian') or code (e.g. 'te', 'ru')
    into a valid ISO code accepted by the translation engine.
    
    Parameters:
        language_name_or_code (str): The language name or code.
        is_source (bool): True if looking up a source language (supports 'auto').
        
    Returns:
        str: ISO language code (e.g., 'te', 'ru', 'auto').
        
    Raises:
        ValueError: If the language is not recognized or supported.
    """
    if not language_name_or_code:
        raise ValueError("Language selection cannot be empty.")

    clean_str = language_name_or_code.strip()
    clean_lower = clean_str.lower()

    # Handle auto detect for source
    if clean_lower in ("auto", "auto detect", "autodetect"):
        if is_source:
            return "auto"
        raise ValueError("Target language cannot be 'Auto Detect'. Please choose an explicit target language.")

    # Direct match in normalized name map
    if clean_lower in _NORMALIZED_NAME_TO_CODE:
        return _NORMALIZED_NAME_TO_CODE[clean_lower]

    # Check if already a valid ISO code
    valid_codes = {c.lower() for c in SUPPORTED_LANGUAGES.values()}
    if clean_lower in valid_codes:
        return clean_str

    # Partial / substring match fallback
    for name, code in SUPPORTED_LANGUAGES.items():
        if clean_lower == name.lower():
            return code

    raise ValueError(f"Unsupported language: '{language_name_or_code}'.")


def get_language_name(language_code_or_name: str) -> str:
    """
    Converts an ISO language code (e.g. 'te', 'ru') or name to its friendly display name.
    
    Parameters:
        language_code_or_name (str): Language code or name.
        
    Returns:
        str: Friendly display name (e.g. 'Telugu', 'Russian', 'Auto Detect').
    """
    if not language_code_or_name:
        return ""

    clean_str = language_code_or_name.strip()
    clean_lower = clean_str.lower()

    if clean_lower in ("auto", "auto detect", "autodetect"):
        return "Auto Detect"

    # Direct match in code to name map
    if clean_lower in _CODE_TO_NAME:
        return _CODE_TO_NAME[clean_lower]

    # Direct match in display names
    for name in SUPPORTED_LANGUAGES:
        if name.lower() == clean_lower:
            return name

    return clean_str


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
    2. Resolves human-readable language names to ISO codes across 130+ languages.
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
            if source_code == "auto":
                source_mem = "english"
            else:
                source_name = get_language_name(source_code).lower()
                source_mem = _MYMEMORY_LANGUAGE_NAME_MAP.get(source_name, source_name)

            target_name = get_language_name(target_code).lower()
            target_mem = _MYMEMORY_LANGUAGE_NAME_MAP.get(target_name, target_name)

            fallback_translator = MyMemoryTranslator(source=source_mem, target=target_mem)
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
        
        # Check if the code or base language is supported by gTTS
        if _TTS_SUPPORTED_CODES and lang_code.lower() not in _TTS_SUPPORTED_CODES:
            # Try 2-letter base code (e.g. 'zh' for 'zh-CN')
            base_code = lang_code.split("-")[0].lower()
            if base_code not in _TTS_SUPPORTED_CODES:
                return None
            tts_lang = base_code
        else:
            tts_lang = lang_code

        tts = gTTS(text=clean_text, lang=tts_lang, slow=False)
        
        # Save audio file to a temporary file
        temp_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        temp_file_path = temp_file.name
        temp_file.close()
        
        tts.save(temp_file_path)
        return temp_file_path
    except Exception as e:
        print(f"[TTS Warning]: Could not generate audio for '{clean_text[:20]}...': {e}")
        return None
