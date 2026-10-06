"""
AI Language Translation Tool
Application: app.py

Author: Saabeer
Project: LanguageTranslation
Description:
A sleek, iOS-inspired web-based Language Translation application built with
Python, Gradio, deep-translator, and Google Text-to-Speech (gTTS).
Crafted following Apple Human Interface Guidelines (SF typography, glassmorphism,
pill controls, tactile interactions, and inset grouped layouts).
"""

import inspect
from datetime import datetime
from typing import Tuple, List, Optional
import gradio as gr

from translation import (
    SUPPORTED_LANGUAGES,
    SOURCE_LANGUAGES,
    TARGET_LANGUAGES,
    translate_text,
    count_text_stats,
    generate_tts_audio
)


# -------------------------------------------------------------------------
# iOS Design System Styling (CSS)
# -------------------------------------------------------------------------
IOS_CSS = """
/* =========================================================================
   Apple iOS Design System Theme
   Human Interface Guidelines: SF Typography, Vibrancy, Squircle Radii, Pills
   ========================================================================= */

@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

:root {
    --ios-bg: #F2F2F7;
    --ios-card-bg: #FFFFFF;
    --ios-blue: #007AFF;
    --ios-blue-hover: #0062CC;
    --ios-blue-light: rgba(0, 122, 255, 0.10);
    --ios-gray-fill: #E5E5EA;
    --ios-gray-fill-hover: #D1D1D6;
    --ios-gray-text: #8E8E93;
    --ios-dark-text: #1C1C1E;
    --ios-border: rgba(60, 60, 67, 0.12);
    --ios-shadow: 0 8px 30px rgba(0, 0, 0, 0.04), 0 2px 8px rgba(0, 0, 0, 0.02);
    --ios-card-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
    --ios-radius: 20px;
    --ios-pill-radius: 9999px;
}

/* Overall Body & Container */
body {
    background-color: var(--ios-bg) !important;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display", "Plus Jakarta Sans", "Helvetica Neue", sans-serif !important;
    -webkit-font-smoothing: antialiased;
}

.gradio-container {
    max-width: 960px !important;
    margin: 20px auto !important;
    padding: 16px 20px !important;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display", "Plus Jakarta Sans", "Helvetica Neue", sans-serif !important;
}

/* iOS Top Navigation Bar / Header */
.ios-header {
    text-align: center;
    padding: 28px 20px 22px 20px;
    margin-bottom: 24px;
    background: var(--ios-card-bg);
    border-radius: 24px;
    box-shadow: var(--ios-shadow);
    border: 1px solid var(--ios-border);
    position: relative;
    overflow: hidden;
}

.ios-header::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #007AFF 0%, #5856D6 50%, #AF52DE 100%);
}

.ios-pill-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--ios-blue-light);
    color: var(--ios-blue);
    padding: 5px 14px;
    border-radius: var(--ios-pill-radius);
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.3px;
    text-transform: uppercase;
    margin-bottom: 10px;
    border: 1px solid rgba(0, 122, 255, 0.15);
}

.ios-header-title {
    font-size: 2.4rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.7px !important;
    color: var(--ios-dark-text) !important;
    margin: 4px 0 6px 0 !important;
    line-height: 1.15;
}

.ios-header-subtitle {
    font-size: 1.0rem !important;
    color: var(--ios-gray-text) !important;
    margin: 0 !important;
    font-weight: 500;
}

/* Cards & Inset Surfaces */
.block {
    border-radius: 18px !important;
    border: 1px solid var(--ios-border) !important;
    background: var(--ios-card-bg) !important;
    box-shadow: var(--ios-card-shadow) !important;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

.block:focus-within {
    border-color: var(--ios-blue) !important;
    box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.15) !important;
}

/* Dropdowns & Selectors */
.gr-dropdown {
    border-radius: 14px !important;
}

/* Text Areas */
textarea {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Plus Jakarta Sans", sans-serif !important;
    font-size: 1.05rem !important;
    line-height: 1.55 !important;
    border-radius: 14px !important;
    color: var(--ios-dark-text) !important;
    padding: 12px 14px !important;
}

textarea::placeholder {
    color: var(--ios-gray-text) !important;
    font-weight: 400;
}

/* Live Stats Chip */
.ios-stats-chip {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 14px;
    background: var(--ios-gray-fill);
    color: var(--ios-dark-text);
    border-radius: var(--ios-pill-radius);
    font-size: 0.82rem;
    font-weight: 600;
    margin-top: 4px;
}

/* iOS Primary Button (Translate) */
button.primary-btn, button[variant="primary"] {
    background: linear-gradient(180deg, #0A84FF 0%, #007AFF 100%) !important;
    color: #FFFFFF !important;
    border-radius: var(--ios-pill-radius) !important;
    font-weight: 700 !important;
    font-size: 1.02rem !important;
    padding: 12px 26px !important;
    border: none !important;
    box-shadow: 0 4px 16px rgba(0, 122, 255, 0.32) !important;
    cursor: pointer !important;
    transition: all 0.15s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

button.primary-btn:hover, button[variant="primary"]:hover {
    background: linear-gradient(180deg, #007AFF 0%, #0062CC 100%) !important;
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(0, 122, 255, 0.4) !important;
}

button.primary-btn:active, button[variant="primary"]:active {
    transform: scale(0.97) !important;
    box-shadow: 0 2px 8px rgba(0, 122, 255, 0.2) !important;
}

/* iOS Secondary Buttons (Swap, Clear, Listen) */
button[variant="secondary"] {
    background: var(--ios-gray-fill) !important;
    color: var(--ios-blue) !important;
    border-radius: var(--ios-pill-radius) !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    border: none !important;
    padding: 10px 20px !important;
    cursor: pointer !important;
    transition: all 0.15s ease !important;
}

button[variant="secondary"]:hover {
    background: var(--ios-gray-fill-hover) !important;
    color: var(--ios-blue-hover) !important;
}

button[variant="secondary"]:active {
    transform: scale(0.97) !important;
}

/* iOS Destructive Button (Clear History) */
button[variant="stop"] {
    background: rgba(255, 59, 48, 0.10) !important;
    color: #FF3B30 !important;
    border-radius: var(--ios-pill-radius) !important;
    font-weight: 600 !important;
    border: 1px solid rgba(255, 59, 48, 0.2) !important;
    transition: all 0.15s ease !important;
}

button[variant="stop"]:hover {
    background: rgba(255, 59, 48, 0.18) !important;
}

button[variant="stop"]:active {
    transform: scale(0.97) !important;
}

/* iOS Accordion (History) */
.gr-accordion {
    border-radius: 20px !important;
    border: 1px solid var(--ios-border) !important;
    background: var(--ios-card-bg) !important;
    box-shadow: var(--ios-card-shadow) !important;
    overflow: hidden !important;
    margin-top: 16px !important;
}

/* Dataframe (iOS Inset Grouped Table) */
.gr-dataframe {
    border-radius: 14px !important;
    overflow: hidden !important;
    border: 1px solid var(--ios-border) !important;
}

/* iOS Minimalist Footer */
.ios-footer {
    text-align: center;
    padding: 18px 0;
    margin-top: 24px;
    color: var(--ios-gray-text);
    font-size: 0.85rem;
    font-weight: 500;
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
) -> Tuple[str, str, Optional[str], List[List[str]], List[List[str]]]:
    """
    Handles translation requests triggered by Translate button or Enter key.
    
    Returns:
        (translated_text, stats_markdown, tts_audio_path, updated_history_table, updated_history_state)
    """
    if not text or not text.strip():
        stats = "📊 0 characters • 0 words"
        return "", stats, None, history, history

    # Perform translation
    translated = translate_text(text, source_lang, target_lang)

    # Compute text metrics
    chars, words = count_text_stats(text)
    stats = f"📊 {chars} characters • {words} words"

    # Auto-generate TTS audio if translation was successful
    audio_path = None
    if translated and not translated.startswith("Error:") and not translated.startswith("Language Error:"):
        audio_path = generate_tts_audio(translated, target_lang)

    # Log to history
    timestamp = datetime.now().strftime("%H:%M:%S")
    new_entry = [timestamp, source_lang, target_lang, text.strip(), translated]
    updated_history = [new_entry] + (history or [])

    return translated, stats, audio_path, updated_history, updated_history


def on_swap_languages(
    source_lang: str,
    target_lang: str,
    input_text: str,
    output_text: str
) -> Tuple[str, str, str, str, str, Optional[str]]:
    """
    Swaps source and target languages, reversing input/output for quick back-translation.
    """
    new_source = target_lang
    new_target = "English" if source_lang == "Auto Detect" else source_lang

    # Set previous output as new input (if valid)
    new_input = (
        output_text
        if output_text and not output_text.startswith("Error:") and not output_text.startswith("Language Error:")
        else input_text
    )
    new_output = ""

    chars, words = count_text_stats(new_input)
    stats = f"📊 {chars} characters • {words} words"

    return new_source, new_target, new_input, new_output, stats, None


def on_clear() -> Tuple[str, str, str, Optional[str]]:
    """
    Resets input, output, metrics, and audio player.
    """
    return "", "", "📊 0 characters • 0 words", None


def on_listen(output_text: str, target_lang: str) -> Optional[str]:
    """
    Generates voice playback for the current translated text.
    """
    if not output_text or not output_text.strip():
        return None
    return generate_tts_audio(output_text, target_lang)


def on_input_text_change(text: str) -> str:
    """
    Dynamically recalculates character and word metrics as user types.
    """
    chars, words = count_text_stats(text)
    return f"📊 {chars} characters • {words} words"


def on_clear_history() -> Tuple[List[List[str]], List[List[str]]]:
    """
    Clears all translation history.
    """
    return [], []


# -------------------------------------------------------------------------
# iOS-Styled Gradio Application Builder
# -------------------------------------------------------------------------
def create_app() -> gr.Blocks:
    """
    Builds the iOS Human Interface Guidelines translation interface.
    Compatible across Gradio 4.x, 5.x, and 6.x.
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

    with gr.Blocks(title="Translate — AI Language Translation") as demo:
        # History state management
        history_state = gr.State([])

        # iOS Navigation Header
        gr.HTML("""
        <div class="ios-header">
            <div class="ios-pill-badge">✦ Neural Translate</div>
            <h1 class="ios-header-title">Translate</h1>
            <p class="ios-header-subtitle">Instant speech and text translation across 15+ languages</p>
        </div>
        """)

        # Main Translation Card (Side-by-Side Inset Grouped)
        with gr.Row():
            # Source Column
            with gr.Column(scale=1):
                source_dropdown = gr.Dropdown(
                    choices=source_choices,
                    value="English",
                    label="From",
                    info="Input language"
                )
                input_text = gr.Textbox(
                    label="Text to Translate",
                    placeholder="Enter text here...",
                    lines=6,
                    max_lines=12,
                    **copy_kwarg
                )
                stats_display = gr.Markdown(
                    "📊 0 characters • 0 words"
                )

            # Target Column
            with gr.Column(scale=1):
                target_dropdown = gr.Dropdown(
                    choices=target_choices,
                    value="Telugu",
                    label="To",
                    info="Destination language"
                )
                output_text = gr.Textbox(
                    label="Translation",
                    placeholder="Translation appears here...",
                    lines=6,
                    max_lines=12,
                    interactive=False,
                    **copy_kwarg
                )
                audio_output = gr.Audio(
                    label="🔊 Speech Pronunciation",
                    type="filepath",
                    interactive=False
                )

        # iOS Pill Action Buttons
        with gr.Row():
            translate_btn = gr.Button(
                "􀊄 Translate",
                variant="primary",
                scale=2
            )
            swap_btn = gr.Button(
                "⇄ Swap",
                variant="secondary",
                scale=1
            )
            clear_btn = gr.Button(
                "✕ Clear",
                variant="secondary",
                scale=1
            )
            listen_btn = gr.Button(
                "🔊 Listen",
                variant="secondary",
                scale=1
            )

        # Translation History (iOS Inset Grouped List)
        with gr.Accordion("📜 Translation History", open=True):
            history_table = gr.Dataframe(
                headers=["Time", "From", "To", "Original Text", "Translated Text"],
                datatype=["str", "str", "str", "str", "str"],
                value=[],
                interactive=False,
                wrap=True
            )
            with gr.Row():
                clear_history_btn = gr.Button("🗑️ Clear History", size="sm", variant="stop")

        # Apple-Inspired Minimalist Footer
        gr.HTML(
            """
            <div class="ios-footer">
                Designed with Apple Human Interface Guidelines • Powered by <code>deep-translator</code> & <code>gTTS</code>
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
            outputs=[output_text, stats_display, audio_output, history_table, history_state]
        )

        # Enter key submit triggers translation
        input_text.submit(
            fn=on_translate,
            inputs=[input_text, source_dropdown, target_dropdown, history_state],
            outputs=[output_text, stats_display, audio_output, history_table, history_state]
        )

        # Swap languages click
        swap_btn.click(
            fn=on_swap_languages,
            inputs=[source_dropdown, target_dropdown, input_text, output_text],
            outputs=[source_dropdown, target_dropdown, input_text, output_text, stats_display, audio_output]
        )

        # Clear button click
        clear_btn.click(
            fn=on_clear,
            inputs=[],
            outputs=[input_text, output_text, stats_display, audio_output]
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
    print("Launching iOS-Style AI Language Translation Tool...")
    # Apple-style clean soft theme
    theme = gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="slate",
        neutral_hue="slate",
        font=[
            gr.themes.GoogleFont("Plus Jakarta Sans"),
            "-apple-system",
            "BlinkMacSystemFont",
            "sans-serif"
        ],
        radius_size=gr.themes.sizes.radius_lg
    )
    app.launch(theme=theme, css=IOS_CSS, share=False)
