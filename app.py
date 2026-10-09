"""
AI Language Translation Tool
Application: app.py

Author: Saabeer
Project: LanguageTranslation
Description:
A refined, high-contrast Modern WindowGlass Language Translation application
built with Python, Gradio, deep-translator, and Google Text-to-Speech (gTTS).
Features high-contrast text visibility, Times New Roman typography,
and the requested sequential layout with animated transition.
"""

import inspect
from datetime import datetime
from typing import Tuple, List, Optional
import gradio as gr

from translation import (
    LANGUAGES,
    SUPPORTED_LANGUAGES,
    SOURCE_LANGUAGES,
    TARGET_LANGUAGES,
    translate_text,
    count_text_stats,
    generate_tts_audio
)


# -------------------------------------------------------------------------
# Modern WindowGlass Theme Tokens (Gradio Theme Engine)
# Ensures 100% high-contrast readability in both Light and Dark mode.
# -------------------------------------------------------------------------
def get_glass_theme() -> gr.themes.Soft:
    """
    Constructs a modern WindowGlass theme with Times New Roman typography,
    high-contrast text, and generous rounded surfaces.
    """
    theme = gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="slate",
        neutral_hue="slate",
        radius_size="lg",
        text_size="lg"
    ).set(
        # Canvas Background (semi-translucent for window glass backdrop)
        body_background_fill="rgba(240, 244, 252, 0.5)",
        body_background_fill_dark="rgba(14, 18, 28, 0.7)",
        
        # WindowGlass Card Fill
        block_background_fill="rgba(255, 255, 255, 0.88)",
        block_background_fill_dark="rgba(22, 26, 40, 0.88)",
        block_border_width="1.5px",
        block_border_color="rgba(255, 255, 255, 0.85)",
        block_border_color_dark="rgba(255, 255, 255, 0.18)",
        block_radius="28px",
        block_shadow="0 16px 40px -8px rgba(0, 32, 64, 0.10)",
        
        # High Contrast Text Colors
        body_text_color="#0F172A",
        body_text_color_dark="#F8FAFC",
        block_title_text_color="#0F172A",
        block_title_text_color_dark="#FFFFFF",
        block_label_text_color="#0F172A",
        block_label_text_color_dark="#FFFFFF",
        
        # Primary Action Button (Modern Blue Pill)
        button_primary_background_fill="#007AFF",
        button_primary_background_fill_hover="#0062CC",
        button_primary_text_color="#FFFFFF",
        button_large_radius="9999px",
        
        # Secondary Action Buttons (Frosted Glass Fill)
        button_secondary_background_fill="rgba(255, 255, 255, 0.85)",
        button_secondary_background_fill_dark="rgba(36, 42, 60, 0.85)",
        button_secondary_text_color="#0055B3",
        button_secondary_text_color_dark="#5AC8FA",
        
        # Form Inputs (Frosted Glass Fill)
        input_background_fill="rgba(255, 255, 255, 0.95)",
        input_background_fill_dark="rgba(30, 36, 54, 0.95)",
        input_border_color="rgba(0, 122, 255, 0.30)",
        input_border_color_dark="rgba(255, 255, 255, 0.25)",
        input_radius="18px",
        input_padding="16px 20px",
        input_text_size="lg",
        input_text_weight="600"
    )
    return theme


# -------------------------------------------------------------------------
# WindowGlass Background & Extended Layout CSS
# -------------------------------------------------------------------------
WINDOW_GLASS_CSS = """
/* =========================================================================
   Modern WindowGlass Theme — Refined Typography & Curved Geometry
   Typography: "Times New Roman", Times, Georgia, serif
   ========================================================================= */

/* 1. Universal Typography & Reset */
* {
    font-family: "Times New Roman", Times, Georgia, serif !important;
}

/* 2. WindowGlass Canvas Background */
body {
    background-image: 
        linear-gradient(135deg, rgba(238, 243, 252, 0.85), rgba(246, 249, 255, 0.90)),
        url('https://cdn.vectorstock.com/i/1000v/07/99/icon-representing-translation-from-english-vector-53290799.jpg'),
        url('/file=assets/bg_translation.jpg') !important;
    background-position: center center !important;
    background-repeat: no-repeat !important;
    background-size: cover !important;
    background-attachment: fixed !important;
    min-height: 100vh !important;
    color: #0F172A !important;
    font-family: "Times New Roman", Times, Georgia, serif !important;
}

:is(.dark) body {
    background-image: 
        linear-gradient(135deg, rgba(14, 18, 30, 0.90), rgba(20, 26, 42, 0.94)),
        url('https://cdn.vectorstock.com/i/1000v/07/99/icon-representing-translation-from-english-vector-53290799.jpg'),
        url('/file=assets/bg_translation.jpg') !important;
    background-position: center center !important;
    background-repeat: no-repeat !important;
    background-size: cover !important;
    background-attachment: fixed !important;
    color: #F8FAFC !important;
}

/* 3. Container & Alignment */
.gradio-container {
    max-width: 1080px !important;
    width: 95% !important;
    margin: 28px auto 56px auto !important;
    padding: 0 16px !important;
    background: transparent !important;
    box-sizing: border-box !important;
}

/* 4. Unified Section Cards — Perfect Curved Corners (border-radius: 28px) & Alignment */
.app-header,
.main-input-card,
.result-section,
.history-card {
    border-radius: 28px !important;
    border: 2px solid rgba(255, 255, 255, 0.88) !important;
    box-shadow: 0 18px 45px -10px rgba(0, 32, 64, 0.10), 0 0 0 1px rgba(255, 255, 255, 0.8) inset !important;
    padding: 28px 32px !important;
    margin-bottom: 24px !important;
    width: 100% !important;
    box-sizing: border-box !important;
    transition: all 0.25s ease !important;
}

:is(.dark) .app-header,
:is(.dark) .main-input-card,
:is(.dark) .result-section,
:is(.dark) .history-card {
    border: 2px solid rgba(255, 255, 255, 0.18) !important;
    box-shadow: 0 18px 45px -10px rgba(0, 0, 0, 0.55), 0 0 0 1px rgba(255, 255, 255, 0.08) inset !important;
}

/* Header Banner Card */
.app-header {
    background: rgba(255, 255, 255, 0.78) !important;
    -webkit-backdrop-filter: blur(28px) saturate(190%) !important;
    backdrop-filter: blur(28px) saturate(190%) !important;
    text-align: center;
    padding: 28px 24px !important;
}

:is(.dark) .app-header {
    background: rgba(20, 25, 40, 0.82) !important;
}

.pill-tag {
    display: inline-block;
    background: rgba(0, 122, 255, 0.14) !important;
    color: #0056B3 !important;
    padding: 6px 18px !important;
    border-radius: 9999px !important;
    font-size: 0.85rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.8px !important;
    text-transform: uppercase;
    margin-bottom: 10px !important;
    border: 1.5px solid rgba(0, 122, 255, 0.28) !important;
}

:is(.dark) .pill-tag {
    background: rgba(10, 132, 255, 0.22) !important;
    color: #5AC8FA !important;
    border-color: rgba(90, 200, 250, 0.35) !important;
}

.app-title {
    font-size: 2.5rem !important;
    font-weight: 800 !important;
    color: #0F172A !important;
    letter-spacing: -0.5px !important;
    margin: 2px 0 8px 0 !important;
    line-height: 1.15;
}

:is(.dark) .app-title {
    color: #FFFFFF !important;
}

.app-subtitle {
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    color: #334155 !important;
    margin: 0 !important;
}

:is(.dark) .app-subtitle {
    color: #CBD5E1 !important;
}

/* Main Input Card */
.main-input-card {
    background: rgba(255, 255, 255, 0.94) !important;
    overflow: visible !important;
}

:is(.dark) .main-input-card {
    background: rgba(22, 27, 44, 0.96) !important;
}

/* Ensure Dropdown Menus Float Unclipped */
.main-input-card,
.language-picker-row,
.dropdown-picker,
.gr-row,
.gr-form,
.form,
.gr-group {
    overflow: visible !important;
}

/* 5. Language Selection Blocks — Prominent, Spacious & Beautiful Curved Corners */
.language-picker-row {
    display: flex !important;
    gap: 24px !important;
    margin-bottom: 22px !important;
    width: 100% !important;
}

.dropdown-picker {
    flex: 1 1 0% !important;
    background: rgba(248, 250, 254, 0.90) !important;
    border: 1.5px solid rgba(0, 122, 255, 0.26) !important;
    border-radius: 20px !important;
    padding: 16px 20px !important;
    box-shadow: 0 4px 16px rgba(0, 32, 64, 0.04) !important;
    transition: all 0.2s ease !important;
    box-sizing: border-box !important;
}

:is(.dark) .dropdown-picker {
    background: rgba(28, 35, 54, 0.90) !important;
    border-color: rgba(90, 200, 250, 0.26) !important;
}

.dropdown-picker:hover {
    border-color: #007AFF !important;
    box-shadow: 0 6px 22px rgba(0, 122, 255, 0.12) !important;
}

/* High Contrast Dropdown Labels & Info Text */
.dropdown-picker label span,
.main-input-card label span,
.result-section label span {
    font-size: 1.18rem !important;
    font-weight: 700 !important;
    color: #0F172A !important;
    opacity: 1 !important;
    display: inline-block !important;
    margin-bottom: 4px !important;
}

:is(.dark) .dropdown-picker label span,
:is(.dark) .main-input-card label span,
:is(.dark) .result-section label span {
    color: #FFFFFF !important;
}

.dropdown-picker .info,
.main-input-card .info,
span[data-testid="block-info"] {
    font-size: 0.98rem !important;
    font-weight: 500 !important;
    color: #334155 !important;
    opacity: 1 !important;
    display: block !important;
    margin-bottom: 8px !important;
}

:is(.dark) .dropdown-picker .info,
:is(.dark) .main-input-card .info,
:is(.dark) span[data-testid="block-info"] {
    color: #CBD5E1 !important;
}

/* Dropdown Selector Input Element */
.dropdown-picker .wrap,
.dropdown-picker div[data-testid="dropdown"] .wrap {
    min-height: 54px !important;
    background: rgba(255, 255, 255, 0.96) !important;
    border: 1.5px solid rgba(0, 122, 255, 0.35) !important;
    border-radius: 16px !important;
    padding: 4px 14px !important;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03) inset !important;
}

:is(.dark) .dropdown-picker .wrap {
    background: rgba(22, 28, 44, 0.96) !important;
    border-color: rgba(255, 255, 255, 0.25) !important;
}

.dropdown-picker input[role="combobox"],
.dropdown-picker input {
    font-size: 1.22rem !important;
    font-weight: 700 !important;
    color: #0F172A !important;
    height: 46px !important;
    line-height: 46px !important;
    background: transparent !important;
    border: none !important;
}

:is(.dark) .dropdown-picker input[role="combobox"],
:is(.dark) .dropdown-picker input {
    color: #FFFFFF !important;
}

/* Prominent Dropdown Arrow Icon */
.dropdown-picker svg,
.dropdown-picker .dropdown-arrow {
    width: 22px !important;
    height: 22px !important;
    color: #007AFF !important;
    stroke: #007AFF !important;
    stroke-width: 2.5px !important;
    opacity: 1 !important;
}

/* 6. Source Text Input & Translated Text Input (Generous & High Contrast) */
textarea,
.main-input-card textarea,
.result-section textarea {
    background: rgba(255, 255, 255, 0.95) !important;
    border: 1.5px solid rgba(0, 122, 255, 0.28) !important;
    border-radius: 18px !important;
    color: #0F172A !important;
    font-size: 1.2rem !important;
    font-weight: 500 !important;
    line-height: 1.5 !important;
    padding: 16px 20px !important;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03) inset !important;
    width: 100% !important;
    box-sizing: border-box !important;
}

textarea::placeholder {
    color: #475569 !important;
    opacity: 0.85 !important;
    font-style: italic !important;
}

:is(.dark) textarea,
:is(.dark) .main-input-card textarea,
:is(.dark) .result-section textarea {
    background: rgba(22, 28, 44, 0.95) !important;
    border-color: rgba(255, 255, 255, 0.22) !important;
    color: #FFFFFF !important;
}

:is(.dark) textarea::placeholder {
    color: #94A3B8 !important;
}

/* Stats Pill Chip */
.stats-chip {
    display: inline-block !important;
    background: rgba(0, 122, 255, 0.09) !important;
    border: 1px solid rgba(0, 122, 255, 0.22) !important;
    color: #0F172A !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    padding: 6px 16px !important;
    border-radius: 9999px !important;
    margin-top: 10px !important;
}

:is(.dark) .stats-chip {
    background: rgba(10, 132, 255, 0.18) !important;
    border-color: rgba(90, 200, 250, 0.25) !important;
    color: #E2E8F0 !important;
}

/* 7. Primary Action Button (Modern Blue Pill) */
.translate-btn button {
    background: linear-gradient(180deg, #0A84FF 0%, #007AFF 100%) !important;
    color: #FFFFFF !important;
    border-radius: 9999px !important;
    font-size: 1.3rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.3px !important;
    padding: 16px 36px !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    box-shadow: 0 10px 30px rgba(0, 122, 255, 0.40), 0 1px 2px rgba(255, 255, 255, 0.5) inset !important;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    cursor: pointer !important;
    width: 100% !important;
    height: 60px !important;
}

.translate-btn button:hover {
    background: linear-gradient(180deg, #007AFF 0%, #0062CC 100%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 14px 36px rgba(0, 122, 255, 0.50), 0 1px 2px rgba(255, 255, 255, 0.6) inset !important;
}

.translate-btn button:active {
    transform: scale(0.98) !important;
    box-shadow: 0 4px 12px rgba(0, 122, 255, 0.25) !important;
}

/* 8. Result Card with Spring Animation */
@keyframes resultReveal {
    0% {
        opacity: 0;
        transform: translateY(20px) scale(0.99);
    }
    100% {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

.result-section {
    animation: resultReveal 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards !important;
    background: rgba(255, 255, 255, 0.94) !important;
    border: 2px solid rgba(0, 122, 255, 0.4) !important;
    margin-top: 18px !important;
}

:is(.dark) .result-section {
    background: rgba(22, 27, 44, 0.96) !important;
    border-color: rgba(10, 132, 255, 0.5) !important;
}

.result-tag {
    display: inline-block;
    background: rgba(0, 122, 255, 0.15) !important;
    color: #0056B3 !important;
    padding: 6px 18px !important;
    border-radius: 9999px !important;
    font-size: 0.95rem !important;
    font-weight: 800 !important;
    margin-bottom: 14px !important;
    border: 1px solid rgba(0, 122, 255, 0.3) !important;
}

:is(.dark) .result-tag {
    background: rgba(10, 132, 255, 0.22) !important;
    color: #5AC8FA !important;
    border-color: rgba(90, 200, 250, 0.35) !important;
}

/* Secondary Action Buttons (Frosted Glass Pill Buttons) */
button[variant="secondary"] {
    background: rgba(255, 255, 255, 0.88) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    backdrop-filter: blur(16px) !important;
    border: 1.5px solid rgba(0, 122, 255, 0.3) !important;
    color: #0056B3 !important;
    border-radius: 9999px !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    padding: 12px 24px !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05) !important;
    transition: all 0.2s ease !important;
}

button[variant="secondary"]:hover {
    background: rgba(255, 255, 255, 1.0) !important;
    border-color: #007AFF !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(0, 122, 255, 0.18) !important;
}

button[variant="secondary"]:active {
    transform: scale(0.97) !important;
}

:is(.dark) button[variant="secondary"] {
    background: rgba(36, 44, 66, 0.88) !important;
    border-color: rgba(90, 200, 250, 0.3) !important;
    color: #5AC8FA !important;
}

button[variant="stop"] {
    border-radius: 9999px !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 10px 22px !important;
}

/* 9. History Card & Accordion Styling */
.history-card {
    background: rgba(255, 255, 255, 0.92) !important;
}

:is(.dark) .history-card {
    background: rgba(22, 27, 44, 0.94) !important;
}

.history-card .label-wrap span,
.history-card button span {
    font-size: 1.25rem !important;
    font-weight: 800 !important;
    color: #0F172A !important;
}

:is(.dark) .history-card .label-wrap span,
:is(.dark) .history-card button span {
    color: #FFFFFF !important;
}

.gr-dataframe {
    border-radius: 18px !important;
    overflow: hidden !important;
    border: 1.5px solid rgba(0, 122, 255, 0.22) !important;
}

.gr-dataframe th {
    background: rgba(240, 244, 255, 0.92) !important;
    color: #0F172A !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    padding: 12px 16px !important;
}

:is(.dark) .gr-dataframe th {
    background: rgba(30, 38, 58, 0.92) !important;
    color: #FFFFFF !important;
}

.gr-dataframe td {
    color: #1E293B !important;
    font-size: 1rem !important;
    font-weight: 500 !important;
    padding: 10px 16px !important;
}

:is(.dark) .gr-dataframe td {
    color: #E2E8F0 !important;
}

/* 10. Footer */
.app-footer {
    text-align: center;
    padding: 24px 0 12px 0;
    color: #1E293B;
    font-size: 0.95rem;
    font-weight: 600;
}

:is(.dark) .app-footer {
    color: #CBD5E1;
}
"""


# -------------------------------------------------------------------------
# UI Event Handlers
# -------------------------------------------------------------------------
def on_translate(
    text: str,
    source_lang: str,
    target_lang: str,
    history: List[List[str]]
) -> Tuple[gr.update, str, str, Optional[str], str, List[List[str]], List[List[str]]]:
    """
    Translates input text and reveals the result section in a smooth transition.
    """
    if not text or not text.strip():
        stats = "📊 0 characters • 0 words"
        msg = "Please enter some text to translate."
        return gr.update(visible=True), msg, stats, None, "✦ Notice", history, history

    # Perform real translation
    translated = translate_text(text, source_lang, target_lang)

    # Compute text metrics
    chars, words = count_text_stats(text)
    stats = f"📊 {chars} characters • {words} words"

    # Auto-generate speech audio if translation was successful
    audio_path = None
    if (
        translated
        and not translated.startswith("Error:")
        and not translated.startswith("Language Error:")
        and not translated.startswith("Translation")
        and translated != "Please enter some text to translate."
    ):
        audio_path = generate_tts_audio(translated, target_lang)

    # Result tag
    badge_label = f"✦ Translation Result ({target_lang})"

    # Update history log only for genuine translations
    updated_history = history or []
    if (
        translated
        and not translated.startswith("Error:")
        and not translated.startswith("Language Error:")
        and not translated.startswith("Translation")
        and translated != "Please enter some text to translate."
    ):
        timestamp = datetime.now().strftime("%H:%M:%S")
        new_entry = [timestamp, source_lang, target_lang, text.strip(), translated]
        updated_history = [new_entry] + updated_history

    # Reveal the result container smoothly
    return gr.update(visible=True), translated, stats, audio_path, badge_label, updated_history, updated_history


def on_swap_languages(
    source_lang: str,
    target_lang: str,
    input_text: str,
    output_text: str
) -> Tuple[str, str, str, str, str, Optional[str], gr.update]:
    """
    Swaps source and target languages, reversing input/output for instant reverse-translation.
    """
    new_source = target_lang
    new_target = "English" if source_lang == "Auto Detect" else source_lang

    new_input = (
        output_text
        if output_text
        and not output_text.startswith("Error:")
        and not output_text.startswith("Language Error:")
        and not output_text.startswith("Translation")
        and output_text != "Please enter some text to translate."
        else input_text
    )
    new_output = ""

    chars, words = count_text_stats(new_input)
    stats = f"📊 {chars} characters • {words} words"

    # Hide result card until user clicks Translate again
    return new_source, new_target, new_input, new_output, stats, None, gr.update(visible=False)


def on_clear() -> Tuple[gr.update, str, str, str, Optional[str]]:
    """
    Resets input, output, stats, audio, and smoothly collapses the result card.
    """
    return gr.update(visible=False), "", "", "📊 0 characters • 0 words", None


def on_listen(output_text: str, target_lang: str) -> Optional[str]:
    """
    Generates voice playback on demand.
    """
    if (
        not output_text
        or not output_text.strip()
        or output_text == "Please enter some text to translate."
        or output_text.startswith("Error:")
        or output_text.startswith("Language Error:")
        or output_text.startswith("Translation")
    ):
        return None
    return generate_tts_audio(output_text, target_lang)


def on_input_text_change(text: str) -> str:
    """
    Dynamically recalculates live character and word counters.
    """
    chars, words = count_text_stats(text)
    return f"📊 {chars} characters • {words} words"


def on_clear_history() -> Tuple[List[List[str]], List[List[str]]]:
    """
    Clears translation history records.
    """
    return [], []


# -------------------------------------------------------------------------
# Application Builder
# -------------------------------------------------------------------------
def create_app() -> gr.Blocks:
    """
    Constructs the streamlined modern WindowGlass translation interface.
    Layout order:
    1. Language selectors & Text input box (at top)
    2. Primary Translate button (under that)
    3. Animated Transition Result card (revealed on translate)
    4. Inset Grouped History section (under that)
    """
    source_choices = list(SOURCE_LANGUAGES.keys())
    target_choices = list(TARGET_LANGUAGES.keys())

    # Detect copy button parameter across Gradio versions
    tb_sig = inspect.signature(gr.Textbox.__init__).parameters
    copy_kwarg = {}
    if "buttons" in tb_sig:
        copy_kwarg = {"buttons": ["copy"]}
    elif "show_copy_button" in tb_sig:
        copy_kwarg = {"show_copy_button": True}

    with gr.Blocks(title="Translate AI — Language Translation Tool") as demo:
        # History state management
        history_state = gr.State([])

        # 1. Navigation Header
        gr.HTML("""
        <div class="app-header">
            <span class="pill-tag">✦ Neural Engine</span>
            <h1 class="app-title">Translate</h1>
            <p class="app-subtitle">Instant speech and text translation across 130+ languages</p>
        </div>
        """)

        # 2. Main Input Card: Language Selectors & Text Input Box
        with gr.Column(elem_classes=["main-input-card"]):
            with gr.Row(elem_classes=["language-picker-row"]):
                source_dropdown = gr.Dropdown(
                    choices=source_choices,
                    value="English",
                    label="Source Language (From)",
                    info="Choose input language or Auto Detect",
                    interactive=True,
                    scale=1,
                    min_width=320,
                    elem_classes=["dropdown-picker"]
                )
                target_dropdown = gr.Dropdown(
                    choices=target_choices,
                    value="Telugu",
                    label="Translation Language (To)",
                    info="Choose destination language",
                    interactive=True,
                    scale=1,
                    min_width=320,
                    elem_classes=["dropdown-picker"]
                )

            input_text = gr.Textbox(
                label="Source Text",
                placeholder="Type or paste text to translate here...",
                lines=4,
                max_lines=8,
                **copy_kwarg
            )
            stats_display = gr.Markdown(
                "📊 0 characters • 0 words",
                elem_classes=["stats-chip"]
            )

        # 3. Under that: Primary Translate Button
        with gr.Row(elem_classes=["translate-btn"]):
            translate_btn = gr.Button(
                "🚀 Translate",
                variant="primary"
            )

        # 4. Under that: Animated Transition Result Card (Revealed on Translate)
        with gr.Column(visible=False, elem_classes=["result-section"]) as result_card:
            result_badge = gr.Markdown(
                "✦ Translation Result",
                elem_classes=["result-tag"]
            )
            with gr.Row():
                with gr.Column(scale=3):
                    output_text = gr.Textbox(
                        label="Translated Text",
                        placeholder="Translation appears here...",
                        lines=4,
                        max_lines=8,
                        interactive=False,
                        **copy_kwarg
                    )
                with gr.Column(scale=2):
                    audio_output = gr.Audio(
                        label="🔊 Speech Pronunciation",
                        type="filepath",
                        interactive=False
                    )
            # Result Action Controls
            with gr.Row():
                swap_btn = gr.Button("⇄ Swap Languages", variant="secondary")
                listen_btn = gr.Button("🔊 Re-Play Speech", variant="secondary")
                clear_btn = gr.Button("✕ Clear Text", variant="secondary")

        # 5. Under that: Inset Grouped History Section (Card with Perfect Curved Corners)
        with gr.Column(elem_classes=["history-card"]):
            with gr.Accordion("Recent Translations", open=True):
                history_table = gr.Dataframe(
                    headers=["Time", "From", "To", "Original Text", "Translated Text"],
                    datatype=["str", "str", "str", "str", "str"],
                    value=[],
                    interactive=False,
                    wrap=True
                )
                with gr.Row():
                    clear_history_btn = gr.Button("Clear History", size="sm", variant="stop")

        # 6. App Footer
        gr.HTML(
            """
            <div class="app-footer">
                CodeAlpha Artificial Intelligence Internship • Neural Speech & Translation Engine
            </div>
            """
        )

        # -----------------------------------------------------------------
        # Event Bindings
        # -----------------------------------------------------------------
        # Dynamic stats on input text change
        input_text.change(
            fn=on_input_text_change,
            inputs=[input_text],
            outputs=[stats_display]
        )

        # Translate button click
        translate_btn.click(
            fn=on_translate,
            inputs=[input_text, source_dropdown, target_dropdown, history_state],
            outputs=[result_card, output_text, stats_display, audio_output, result_badge, history_table, history_state]
        )

        # Enter key submit also triggers translation
        input_text.submit(
            fn=on_translate,
            inputs=[input_text, source_dropdown, target_dropdown, history_state],
            outputs=[result_card, output_text, stats_display, audio_output, result_badge, history_table, history_state]
        )

        # Swap languages click
        swap_btn.click(
            fn=on_swap_languages,
            inputs=[source_dropdown, target_dropdown, input_text, output_text],
            outputs=[source_dropdown, target_dropdown, input_text, output_text, stats_display, audio_output, result_card]
        )

        # Clear button click
        clear_btn.click(
            fn=on_clear,
            inputs=[],
            outputs=[result_card, input_text, output_text, stats_display, audio_output]
        )

        # Listen button click
        listen_btn.click(
            fn=on_listen,
            inputs=[output_text, target_dropdown],
            outputs=[audio_output]
        )

        # Clear history click
        clear_history_btn.click(
            fn=on_clear_history,
            inputs=[],
            outputs=[history_table, history_state]
        )

    return demo


# -------------------------------------------------------------------------
# Application Entry Point
# -------------------------------------------------------------------------
if __name__ == "__main__":
    app = create_app()
    print("Launching AI Language Translation Tool...")
    theme = get_glass_theme()
    app.launch(theme=theme, css=WINDOW_GLASS_CSS, share=False, allowed_paths=["assets"])
