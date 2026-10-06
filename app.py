"""
AI Language Translation Tool
Application: app.py

Author: Saabeer
Project: LanguageTranslation
Description:
A high-fidelity, Apple iOS-inspired Language Translation web application built
with Python, Gradio, deep-translator, and Google Text-to-Speech (gTTS).
Crafted following Apple Human Interface Guidelines (San Francisco typography,
frosted glass top bar, squircle cards, segmented pickers, and pill controls).
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
# Authentic Apple iOS Human Interface Guidelines CSS
# -------------------------------------------------------------------------
APPLE_IOS_CSS = """
/* =========================================================================
   Apple iOS Design System (Human Interface Guidelines)
   ========================================================================= */

@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

:root {
    --ios-bg: #F2F2F7;
    --ios-card: #FFFFFF;
    --ios-blue: #007AFF;
    --ios-blue-pressed: #0062CC;
    --ios-gray-fill: #E5E5EA;
    --ios-gray-fill-hover: #D1D1D6;
    --ios-secondary-text: #8E8E93;
    --ios-primary-text: #1C1C1E;
    --ios-separator: rgba(60, 60, 67, 0.08);
    --ios-pill: 9999px;
    --ios-card-radius: 24px;
}

/* Global Reset & Canvas */
body, html {
    background-color: var(--ios-bg) !important;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display", "Plus Jakarta Sans", "Helvetica Neue", sans-serif !important;
    -webkit-font-smoothing: antialiased;
    margin: 0;
    padding: 0;
}

.gradio-container {
    max-width: 980px !important;
    margin: 20px auto 40px auto !important;
    padding: 0 16px !important;
    background: transparent !important;
}

/* Remove default Gradio block borders & shadows */
.block {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
}

/* -------------------------------------------------------------------------
   1. Apple Dynamic Navigation Bar / Top Island
   ------------------------------------------------------------------------- */
.apple-nav-header {
    text-align: center;
    padding: 24px 20px 20px 20px;
    margin-bottom: 22px;
    background: var(--ios-card);
    border-radius: var(--ios-card-radius);
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.03), 0 1px 2px rgba(0, 0, 0, 0.02);
    border: 1px solid var(--ios-separator);
    position: relative;
}

.apple-status-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(0, 122, 255, 0.09);
    color: var(--ios-blue);
    padding: 5px 14px;
    border-radius: var(--ios-pill);
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-bottom: 8px;
    border: 1px solid rgba(0, 122, 255, 0.14);
}

.apple-app-title {
    font-size: 2.3rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.7px !important;
    color: var(--ios-primary-text) !important;
    margin: 0 !important;
    line-height: 1.15;
}

.apple-app-subtitle {
    font-size: 0.98rem !important;
    color: var(--ios-secondary-text) !important;
    margin: 5px 0 0 0 !important;
    font-weight: 400;
}

/* -------------------------------------------------------------------------
   2. Apple Inset Grouped Translation Cards
   ------------------------------------------------------------------------- */
.apple-surface-card {
    background: var(--ios-card) !important;
    border-radius: var(--ios-card-radius) !important;
    padding: 20px 22px !important;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.04), 0 1px 2px rgba(0, 0, 0, 0.02) !important;
    border: 1px solid var(--ios-separator) !important;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.apple-surface-card:focus-within {
    border-color: var(--ios-blue) !important;
    box-shadow: 0 6px 28px rgba(0, 122, 255, 0.12), 0 1px 4px rgba(0, 122, 255, 0.06) !important;
}

/* Card Header Labels */
.apple-card-tag {
    font-size: 0.76rem;
    font-weight: 700;
    letter-spacing: 0.6px;
    color: var(--ios-secondary-text);
    text-transform: uppercase;
    margin-bottom: 4px;
}

/* Apple Dropdown Pickers */
.apple-picker {
    background: var(--ios-bg) !important;
    border-radius: 14px !important;
    border: 1px solid var(--ios-separator) !important;
    padding: 2px 8px !important;
    font-weight: 600 !important;
}

.apple-picker .wrap {
    border: none !important;
    box-shadow: none !important;
    background: transparent !important;
}

/* Apple Textareas */
.apple-surface-card textarea {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display", sans-serif !important;
    font-size: 1.12rem !important;
    line-height: 1.6 !important;
    color: var(--ios-primary-text) !important;
    resize: vertical !important;
    padding: 6px 0 !important;
}

.apple-surface-card textarea:focus {
    outline: none !important;
    box-shadow: none !important;
}

.apple-surface-card textarea::placeholder {
    color: var(--ios-secondary-text) !important;
    font-weight: 400 !important;
}

/* Live Stats Apple Chip */
.apple-stats-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    background: var(--ios-gray-fill);
    color: var(--ios-primary-text);
    border-radius: var(--ios-pill);
    font-size: 0.8rem;
    font-weight: 600;
    margin-top: 4px;
    width: fit-content;
}

/* -------------------------------------------------------------------------
   3. Apple Pill Action Buttons
   ------------------------------------------------------------------------- */
.apple-actions-row {
    margin-top: 16px !important;
    gap: 12px !important;
}

/* Primary Translate Button */
.apple-btn-primary button, button.apple-primary-action {
    background: var(--ios-blue) !important;
    background-image: linear-gradient(180deg, #0A84FF 0%, #007AFF 100%) !important;
    color: #FFFFFF !important;
    border-radius: var(--ios-pill) !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.2px !important;
    padding: 13px 28px !important;
    border: none !important;
    box-shadow: 0 4px 16px rgba(0, 122, 255, 0.35) !important;
    transition: all 0.16s cubic-bezier(0.16, 1, 0.3, 1) !important;
    cursor: pointer !important;
}

.apple-btn-primary button:hover {
    background-image: linear-gradient(180deg, #007AFF 0%, #0062CC 100%) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 22px rgba(0, 122, 255, 0.45) !important;
}

.apple-btn-primary button:active {
    transform: scale(0.96) !important;
    box-shadow: 0 2px 8px rgba(0, 122, 255, 0.22) !important;
}

/* Secondary Pill Buttons (Swap, Clear, Listen) */
.apple-btn-secondary button {
    background: var(--ios-gray-fill) !important;
    color: var(--ios-blue) !important;
    border-radius: var(--ios-pill) !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    padding: 12px 20px !important;
    border: none !important;
    box-shadow: none !important;
    transition: all 0.16s cubic-bezier(0.16, 1, 0.3, 1) !important;
    cursor: pointer !important;
}

.apple-btn-secondary button:hover {
    background: var(--ios-gray-fill-hover) !important;
    color: var(--ios-blue-pressed) !important;
}

.apple-btn-secondary button:active {
    transform: scale(0.96) !important;
}

/* -------------------------------------------------------------------------
   4. Apple Audio Player & History Inset Group
   ------------------------------------------------------------------------- */
.apple-audio-box {
    border-radius: 16px !important;
    background: var(--ios-bg) !important;
    padding: 6px !important;
    border: 1px solid var(--ios-separator) !important;
}

.apple-history-accordion {
    margin-top: 24px !important;
    border-radius: var(--ios-card-radius) !important;
    background: var(--ios-card) !important;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.03) !important;
    border: 1px solid var(--ios-separator) !important;
    overflow: hidden !important;
}

.apple-history-accordion .label-wrap {
    padding: 16px 20px !important;
    font-weight: 700 !important;
    font-size: 1.05rem !important;
    color: var(--ios-primary-text) !important;
}

.apple-history-table {
    border-radius: 14px !important;
    overflow: hidden !important;
    border: 1px solid var(--ios-separator) !important;
}

/* Apple Destructive Button */
.apple-btn-destructive button {
    background: rgba(255, 59, 48, 0.08) !important;
    color: #FF3B30 !important;
    border-radius: var(--ios-pill) !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    border: 1px solid rgba(255, 59, 48, 0.18) !important;
    padding: 8px 18px !important;
    transition: all 0.16s ease !important;
    cursor: pointer !important;
}

.apple-btn-destructive button:hover {
    background: rgba(255, 59, 48, 0.15) !important;
}

.apple-btn-destructive button:active {
    transform: scale(0.96) !important;
}

/* -------------------------------------------------------------------------
   5. Apple Footer
   ------------------------------------------------------------------------- */
.apple-footer {
    text-align: center;
    padding: 24px 0 10px 0;
    color: var(--ios-secondary-text);
    font-size: 0.84rem;
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
# Apple iOS-Styled Gradio Application Builder
# -------------------------------------------------------------------------
def create_app() -> gr.Blocks:
    """
    Builds the Apple iOS translation interface.
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

    with gr.Blocks(title="Translate — Apple iOS Experience") as demo:
        # History state management
        history_state = gr.State([])

        # 1. Apple Navigation Header
        gr.HTML("""
        <div class="apple-nav-header">
            <div class="apple-status-pill">✦ Neural Engine</div>
            <h1 class="apple-app-title">Translate</h1>
            <p class="apple-app-subtitle">Instant speech and text translation across 15+ languages</p>
        </div>
        """)

        # 2. Main Translation Cards (Side-by-Side Inset Grouped)
        with gr.Row():
            # Source Card (Input)
            with gr.Column(scale=1, elem_classes=["apple-surface-card"]):
                gr.HTML('<div class="apple-card-tag">FROM LANGUAGE</div>')
                source_dropdown = gr.Dropdown(
                    choices=source_choices,
                    value="English",
                    label="",
                    show_label=False,
                    elem_classes=["apple-picker"]
                )
                input_text = gr.Textbox(
                    placeholder="Type or paste text to translate...",
                    lines=6,
                    max_lines=12,
                    show_label=False,
                    **copy_kwarg
                )
                stats_display = gr.Markdown(
                    "📊 0 characters • 0 words",
                    elem_classes=["apple-stats-chip"]
                )

            # Target Card (Output)
            with gr.Column(scale=1, elem_classes=["apple-surface-card"]):
                gr.HTML('<div class="apple-card-tag">TO LANGUAGE</div>')
                target_dropdown = gr.Dropdown(
                    choices=target_choices,
                    value="Telugu",
                    label="",
                    show_label=False,
                    elem_classes=["apple-picker"]
                )
                output_text = gr.Textbox(
                    placeholder="Translation appears here...",
                    lines=6,
                    max_lines=12,
                    interactive=False,
                    show_label=False,
                    **copy_kwarg
                )
                audio_output = gr.Audio(
                    show_label=False,
                    type="filepath",
                    interactive=False,
                    elem_classes=["apple-audio-box"]
                )

        # 3. Apple Pill Action Bar
        with gr.Row(elem_classes=["apple-actions-row"]):
            translate_btn = gr.Button(
                "Translate",
                variant="primary",
                scale=2,
                elem_classes=["apple-btn-primary"]
            )
            swap_btn = gr.Button(
                "⇄ Swap",
                variant="secondary",
                scale=1,
                elem_classes=["apple-btn-secondary"]
            )
            clear_btn = gr.Button(
                "✕ Clear",
                variant="secondary",
                scale=1,
                elem_classes=["apple-btn-secondary"]
            )
            listen_btn = gr.Button(
                "🔊 Listen",
                variant="secondary",
                scale=1,
                elem_classes=["apple-btn-secondary"]
            )

        # 4. Inset Grouped Translation History
        with gr.Accordion("Recent Translations", open=True, elem_classes=["apple-history-accordion"]):
            history_table = gr.Dataframe(
                headers=["Time", "From", "To", "Original Text", "Translated Text"],
                datatype=["str", "str", "str", "str", "str"],
                value=[],
                interactive=False,
                wrap=True,
                elem_classes=["apple-history-table"]
            )
            with gr.Row():
                clear_history_btn = gr.Button(
                    "Clear History",
                    size="sm",
                    variant="stop",
                    elem_classes=["apple-btn-destructive"]
                )

        # 5. Apple Footer
        gr.HTML(
            """
            <div class="apple-footer">
                Designed with Apple Human Interface Guidelines • Neural Speech & Translation Engine
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
    print("Launching Apple iOS-Style AI Language Translation Tool...")
    # Apple-style clean soft theme
    theme = gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="slate",
        neutral_hue="slate",
        font=[
            "-apple-system",
            "BlinkMacSystemFont",
            "SF Pro Text",
            "SF Pro Display",
            gr.themes.GoogleFont("Plus Jakarta Sans"),
            "sans-serif"
        ],
        radius_size=gr.themes.sizes.radius_lg
    )
    app.launch(theme=theme, css=APPLE_IOS_CSS, share=False)
