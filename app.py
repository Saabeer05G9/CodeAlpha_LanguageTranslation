"""
AI Language Translation Tool
Application: app.py

Author: Saabeer
Project: LanguageTranslation
Description:
A native Apple iOS-inspired Language Translation application built with
Python, Gradio, deep-translator, and Google Text-to-Speech (gTTS).
Features a streamlined iOS 18 layout: Language selectors & Input Card at top,
Primary Translate button, animated Spring Transition Result Card, and Inset Grouped History.
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
# Native Apple iOS Human Interface Guidelines Styling (CSS)
# -------------------------------------------------------------------------
APPLE_IOS_CSS = """
/* =========================================================================
   Apple iOS 18 Design System (Human Interface Guidelines)
   ========================================================================= */

@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

:root {
    --ios-bg: #F2F2F7;
    --ios-card: #FFFFFF;
    --ios-blue: #007AFF;
    --ios-blue-pressed: #0062CC;
    --ios-blue-light: rgba(0, 122, 255, 0.09);
    --ios-gray-fill: #E5E5EA;
    --ios-gray-fill-hover: #D1D1D6;
    --ios-secondary-text: #8E8E93;
    --ios-primary-text: #1C1C1E;
    --ios-separator: rgba(60, 60, 67, 0.08);
    --ios-pill: 9999px;
    --ios-card-radius: 22px;
}

/* Global Reset & Page Canvas */
body, html {
    background-color: var(--ios-bg) !important;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display", "Plus Jakarta Sans", "Helvetica Neue", sans-serif !important;
    -webkit-font-smoothing: antialiased;
    margin: 0;
    padding: 0;
}

.gradio-container {
    max-width: 860px !important;
    margin: 24px auto 48px auto !important;
    padding: 0 16px !important;
    background: transparent !important;
}

/* Remove default Gradio block frames */
.block {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
}

/* -------------------------------------------------------------------------
   1. Apple Navigation Header / Dynamic Island Pill
   ------------------------------------------------------------------------- */
.apple-nav-header {
    text-align: center;
    padding: 24px 20px 20px 20px;
    margin-bottom: 20px;
    background: var(--ios-card);
    border-radius: var(--ios-card-radius);
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.03), 0 1px 2px rgba(0, 0, 0, 0.02);
    border: 1px solid var(--ios-separator);
}

.apple-status-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--ios-blue-light);
    color: var(--ios-blue);
    padding: 5px 14px;
    border-radius: var(--ios-pill);
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.4px;
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
    font-size: 0.96rem !important;
    color: var(--ios-secondary-text) !important;
    margin: 4px 0 0 0 !important;
    font-weight: 400;
}

/* -------------------------------------------------------------------------
   2. Input Card & Language Selector Bar
   ------------------------------------------------------------------------- */
.apple-input-card {
    background: var(--ios-card) !important;
    border-radius: var(--ios-card-radius) !important;
    padding: 22px 24px !important;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.04), 0 1px 2px rgba(0, 0, 0, 0.02) !important;
    border: 1px solid var(--ios-separator) !important;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    margin-bottom: 16px !important;
}

.apple-input-card:focus-within {
    border-color: var(--ios-blue) !important;
    box-shadow: 0 6px 28px rgba(0, 122, 255, 0.12), 0 1px 4px rgba(0, 122, 255, 0.06) !important;
}

/* Apple Language Picker Segment */
.apple-lang-row {
    margin-bottom: 14px !important;
    gap: 12px !important;
}

.apple-picker-label {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    color: var(--ios-secondary-text);
    text-transform: uppercase;
    margin-bottom: 4px;
}

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

/* Frameless Textarea */
.apple-input-card textarea {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display", sans-serif !important;
    font-size: 1.15rem !important;
    line-height: 1.6 !important;
    color: var(--ios-primary-text) !important;
    resize: vertical !important;
    padding: 6px 0 !important;
}

.apple-input-card textarea:focus {
    outline: none !important;
    box-shadow: none !important;
}

.apple-input-card textarea::placeholder {
    color: var(--ios-secondary-text) !important;
    font-weight: 400 !important;
}

/* Live Stats Apple Pill */
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
    margin-top: 6px;
    width: fit-content;
}

/* -------------------------------------------------------------------------
   3. Primary Translate Button (Full Width iOS Pill)
   ------------------------------------------------------------------------- */
.apple-primary-btn-row {
    margin: 10px 0 20px 0 !important;
}

.apple-btn-primary button, button.apple-primary-action {
    background: var(--ios-blue) !important;
    background-image: linear-gradient(180deg, #0A84FF 0%, #007AFF 100%) !important;
    color: #FFFFFF !important;
    border-radius: var(--ios-pill) !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.2px !important;
    padding: 15px 32px !important;
    border: none !important;
    box-shadow: 0 6px 20px rgba(0, 122, 255, 0.38) !important;
    transition: all 0.16s cubic-bezier(0.16, 1, 0.3, 1) !important;
    cursor: pointer !important;
    width: 100% !important;
}

.apple-btn-primary button:hover {
    background-image: linear-gradient(180deg, #007AFF 0%, #0062CC 100%) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(0, 122, 255, 0.46) !important;
}

.apple-btn-primary button:active {
    transform: scale(0.97) !important;
    box-shadow: 0 2px 8px rgba(0, 122, 255, 0.2) !important;
}

/* -------------------------------------------------------------------------
   4. Translation Result Card (iOS Spring Reveal Animation)
   ------------------------------------------------------------------------- */
@keyframes iosSpringReveal {
    0% {
        opacity: 0;
        transform: translateY(22px) scale(0.97);
    }
    65% {
        opacity: 1;
        transform: translateY(-2px) scale(1.004);
    }
    100% {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

.ios-result-card {
    background: var(--ios-card) !important;
    border-radius: var(--ios-card-radius) !important;
    padding: 22px 24px !important;
    box-shadow: 0 8px 30px rgba(0, 122, 255, 0.08), 0 2px 8px rgba(0, 0, 0, 0.03) !important;
    border: 1.5px solid rgba(0, 122, 255, 0.22) !important;
    animation: iosSpringReveal 0.45s cubic-bezier(0.16, 1, 0.3, 1) forwards !important;
    margin-bottom: 22px !important;
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.ios-result-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--ios-blue-light);
    color: var(--ios-blue);
    padding: 4px 14px;
    border-radius: var(--ios-pill);
    font-size: 0.82rem;
    font-weight: 700;
    width: fit-content;
    letter-spacing: 0.3px;
    margin-bottom: 6px;
}

.ios-result-card textarea {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display", sans-serif !important;
    font-size: 1.25rem !important;
    font-weight: 600 !important;
    line-height: 1.6 !important;
    color: var(--ios-primary-text) !important;
    padding: 4px 0 !important;
}

.apple-audio-player {
    border-radius: 14px !important;
    background: var(--ios-bg) !important;
    padding: 4px !important;
    border: 1px solid var(--ios-separator) !important;
}

/* Secondary Action Buttons (Inside Result Card) */
.apple-result-actions {
    margin-top: 10px !important;
    gap: 10px !important;
}

.apple-btn-secondary button {
    background: var(--ios-gray-fill) !important;
    color: var(--ios-blue) !important;
    border-radius: var(--ios-pill) !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    padding: 11px 20px !important;
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
   5. Inset Grouped History Section
   ------------------------------------------------------------------------- */
.apple-history-accordion {
    margin-top: 14px !important;
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

/* Destructive Clear History Action */
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
   6. Apple Minimalist Footer
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
) -> Tuple[gr.update, str, str, Optional[str], str, List[List[str]], List[List[str]]]:
    """
    Handles translation requests.
    Reveals the result card with smooth animation and populates translation, audio, and history.
    """
    if not text or not text.strip():
        stats = "📊 0 characters • 0 words"
        return gr.update(visible=False), "", stats, None, "", history, history

    # Perform real translation
    translated = translate_text(text, source_lang, target_lang)

    # Calculate input text metrics
    chars, words = count_text_stats(text)
    stats = f"📊 {chars} characters • {words} words"

    # Auto-generate TTS audio if translation was successful
    audio_path = None
    if translated and not translated.startswith("Error:") and not translated.startswith("Language Error:"):
        audio_path = generate_tts_audio(translated, target_lang)

    # Result badge label
    badge_label = f"✦ Translated to {target_lang}"

    # Log to history
    timestamp = datetime.now().strftime("%H:%M:%S")
    new_entry = [timestamp, source_lang, target_lang, text.strip(), translated]
    updated_history = [new_entry] + (history or [])

    # Reveal the result container smoothly
    return gr.update(visible=True), translated, stats, audio_path, badge_label, updated_history, updated_history


def on_swap_languages(
    source_lang: str,
    target_lang: str,
    input_text: str,
    output_text: str
) -> Tuple[str, str, str, str, str, Optional[str], gr.update]:
    """
    Swaps source and target languages, reversing input/output for instant back-translation.
    """
    new_source = target_lang
    new_target = "English" if source_lang == "Auto Detect" else source_lang

    new_input = (
        output_text
        if output_text and not output_text.startswith("Error:") and not output_text.startswith("Language Error:")
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
    if not output_text or not output_text.strip():
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
# Apple iOS-Styled Gradio Application Builder
# -------------------------------------------------------------------------
def create_app() -> gr.Blocks:
    """
    Constructs the streamlined Apple iOS translation interface.
    Follows exact requested sequence:
    1. Language selectors & Text input card
    2. Primary Translate button
    3. Animated Transition Result card (revealed on translate)
    4. Inset Grouped History section below
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
            <p class="apple-app-subtitle">Select languages, enter text, and translate instantly</p>
        </div>
        """)

        # 2. Main Input Card: Language Selectors & Text Input Box
        with gr.Column(elem_classes=["apple-input-card"]):
            # Language Selection Row (From & To)
            with gr.Row(elem_classes=["apple-lang-row"]):
                with gr.Column(scale=1):
                    gr.HTML('<div class="apple-picker-label">Selected Language (From)</div>')
                    source_dropdown = gr.Dropdown(
                        choices=source_choices,
                        value="English",
                        show_label=False,
                        elem_classes=["apple-picker"]
                    )
                with gr.Column(scale=1):
                    gr.HTML('<div class="apple-picker-label">Translation Language (To)</div>')
                    target_dropdown = gr.Dropdown(
                        choices=target_choices,
                        value="Telugu",
                        show_label=False,
                        elem_classes=["apple-picker"]
                    )

            # Text Input Box
            gr.HTML('<div class="apple-picker-label" style="margin-top: 8px;">Text to Translate</div>')
            input_text = gr.Textbox(
                placeholder="Type or paste text to translate here...",
                lines=5,
                max_lines=10,
                show_label=False,
                **copy_kwarg
            )
            stats_display = gr.Markdown(
                "📊 0 characters • 0 words",
                elem_classes=["apple-stats-chip"]
            )

        # 3. Under that: Primary Translate Button
        with gr.Row(elem_classes=["apple-primary-btn-row"]):
            translate_btn = gr.Button(
                "🚀 Translate",
                variant="primary",
                elem_classes=["apple-btn-primary"]
            )

        # 4. Under that: Animated Transition Result Card (Revealed after clicking Translate)
        with gr.Column(visible=False, elem_classes=["ios-result-card"]) as result_card:
            result_badge = gr.Markdown(
                "✦ Translated Result",
                elem_classes=["ios-result-badge"]
            )
            output_text = gr.Textbox(
                placeholder="Translation appears here...",
                lines=5,
                max_lines=10,
                interactive=False,
                show_label=False,
                **copy_kwarg
            )
            audio_output = gr.Audio(
                show_label=False,
                type="filepath",
                interactive=False,
                elem_classes=["apple-audio-player"]
            )
            # Result Card Action Buttons
            with gr.Row(elem_classes=["apple-result-actions"]):
                swap_btn = gr.Button(
                    "⇄ Swap & Reverse",
                    variant="secondary",
                    scale=1,
                    elem_classes=["apple-btn-secondary"]
                )
                listen_btn = gr.Button(
                    "🔊 Re-Play Speech",
                    variant="secondary",
                    scale=1,
                    elem_classes=["apple-btn-secondary"]
                )
                clear_btn = gr.Button(
                    "✕ Clear All",
                    variant="secondary",
                    scale=1,
                    elem_classes=["apple-btn-secondary"]
                )

        # 5. Under that: Inset Grouped History Section
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

        # 6. Apple Minimalist Footer
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
            outputs=[result_card, output_text, stats_display, audio_output, result_badge, history_table, history_state]
        )

        # Enter key in text box also triggers translation
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
    print("Launching Apple iOS-Style AI Language Translation Tool...")
    # Apple clean soft theme
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
