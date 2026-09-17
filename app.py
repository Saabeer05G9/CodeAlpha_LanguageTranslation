"""
CodeAlpha AI Internship — Task 1: Language Translation Tool
Application: app.py

Author: Saabeer
Project: CodeAlpha_LanguageTranslation
Description:
A clean, modern, and professional web-based Language Translation Tool built with
Python, Gradio, deep-translator, and Google Text-to-Speech (gTTS).
Satisfies all official CodeAlpha Task 1 core requirements and professional features.
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
# Custom Styling (CSS)
# -------------------------------------------------------------------------
CUSTOM_CSS = """
/* Container & Background */
.gradio-container {
    max-width: 1050px !important;
    margin: auto !important;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
}

/* Header Banner */
.header-box {
    text-align: center;
    padding: 24px 16px;
    background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #60a5fa 100%);
    border-radius: 14px;
    color: white;
    margin-bottom: 24px;
    box-shadow: 0 4px 14px rgba(30, 58, 138, 0.25);
}

.header-title {
    font-size: 2.2rem !important;
    font-weight: 800 !important;
    margin-bottom: 6px !important;
    letter-spacing: -0.5px;
}

.header-subtitle {
    font-size: 1.05rem !important;
    opacity: 0.92;
    margin: 0 !important;
}

.header-badge {
    display: inline-block;
    background: rgba(255, 255, 255, 0.22);
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.82rem;
    font-weight: 600;
    margin-top: 10px;
    letter-spacing: 0.5px;
}

/* Stat Display Card */
.stat-box {
    font-size: 0.95rem;
    color: #4b5563;
    padding: 8px 14px;
    border-radius: 8px;
    background: #f3f4f6;
    display: inline-block;
    margin: 4px 0;
    font-weight: 500;
}

/* History Box */
.history-section {
    margin-top: 24px;
    border-top: 2px solid #e5e7eb;
    padding-top: 20px;
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
    Handles translation request triggered by the Translate button or Enter key.
    
    Returns:
        (translated_text, stats_markdown, tts_audio_path, updated_history_table, updated_history_state)
    """
    if not text or not text.strip():
        stats = "📊 **Input Stats:** 0 characters | 0 words"
        return "", stats, None, history, history

    # Perform translation
    translated = translate_text(text, source_lang, target_lang)

    # Calculate input text statistics
    chars, words = count_text_stats(text)
    stats = f"📊 **Input Stats:** {chars} characters | {words} words"

    # Auto-generate TTS audio if translation succeeded
    audio_path = None
    if translated and not translated.startswith("Error:") and not translated.startswith("Language Error:"):
        audio_path = generate_tts_audio(translated, target_lang)

    # Update history log
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
    Swaps source and target languages, and sets previous output as new input.
    If source was 'Auto Detect', it defaults to 'English' as target.
    """
    # Determine new source
    new_source = target_lang

    # Determine new target (cannot be 'Auto Detect')
    new_target = "English" if source_lang == "Auto Detect" else source_lang

    # Swap text contents if an output exists
    new_input = output_text if output_text and not output_text.startswith("Error:") and not output_text.startswith("Language Error:") else input_text
    new_output = ""

    # Recompute text stats for new input
    chars, words = count_text_stats(new_input)
    stats = f"📊 **Input Stats:** {chars} characters | {words} words"

    return new_source, new_target, new_input, new_output, stats, None


def on_clear() -> Tuple[str, str, str, Optional[str]]:
    """
    Clears input, output, stats, and audio.
    """
    return "", "", "📊 **Input Stats:** 0 characters | 0 words", None


def on_listen(output_text: str, target_lang: str) -> Optional[str]:
    """
    Generates speech for the current translated text on-demand.
    """
    if not output_text or not output_text.strip():
        return None
    return generate_tts_audio(output_text, target_lang)


def on_input_text_change(text: str) -> str:
    """
    Dynamically updates character and word counts as the user types.
    """
    chars, words = count_text_stats(text)
    return f"📊 **Input Stats:** {chars} characters | {words} words"


def on_clear_history() -> Tuple[List[List[str]], List[List[str]]]:
    """
    Clears the translation history table.
    """
    return [], []


# -------------------------------------------------------------------------
# Gradio Application Builder
# -------------------------------------------------------------------------
def create_app() -> gr.Blocks:
    """
    Constructs and returns the Gradio Blocks application.
    Supports cross-version compatibility for Gradio 4.x, 5.x, and 6.x.
    """
    source_choices = list(SOURCE_LANGUAGES.keys())
    target_choices = list(TARGET_LANGUAGES.keys())

    # Detect supported copy button parameter dynamically across Gradio versions
    tb_sig = inspect.signature(gr.Textbox.__init__).parameters
    copy_kwarg = {}
    if "buttons" in tb_sig:
        copy_kwarg = {"buttons": ["copy"]}
    elif "show_copy_button" in tb_sig:
        copy_kwarg = {"show_copy_button": True}

    with gr.Blocks(title="AI Language Translator — CodeAlpha") as demo:
        # History state management
        history_state = gr.State([])

        # Header Section
        gr.HTML("""
        <div class="header-box">
            <h1 class="header-title">🌐 AI Language Translator</h1>
            <p class="header-subtitle">Translate text seamlessly across 15+ languages with speech & history</p>
            <span class="header-badge">CodeAlpha AI Internship — Task 1</span>
        </div>
        """)

        # Main Translation Interface Card
        with gr.Row():
            with gr.Column(scale=1):
                source_dropdown = gr.Dropdown(
                    choices=source_choices,
                    value="English",
                    label="Source Language",
                    info="Select input language or Auto Detect"
                )
                input_text = gr.Textbox(
                    label="Source Text",
                    placeholder="Type or paste text to translate here...",
                    lines=6,
                    max_lines=12,
                    **copy_kwarg
                )
                stats_display = gr.Markdown(
                    "📊 **Input Stats:** 0 characters | 0 words"
                )

            with gr.Column(scale=1):
                target_dropdown = gr.Dropdown(
                    choices=target_choices,
                    value="Telugu",
                    label="Target Language",
                    info="Select destination language"
                )
                output_text = gr.Textbox(
                    label="Translated Text",
                    placeholder="Translation will appear here...",
                    lines=6,
                    max_lines=12,
                    interactive=False,
                    **copy_kwarg
                )
                audio_output = gr.Audio(
                    label="🔊 Spoken Translation (TTS)",
                    type="filepath",
                    interactive=False
                )

        # Action Buttons
        with gr.Row():
            translate_btn = gr.Button(
                "🚀 Translate",
                variant="primary",
                scale=2
            )
            swap_btn = gr.Button(
                "🔄 Swap Languages",
                variant="secondary",
                scale=1
            )
            clear_btn = gr.Button(
                "🧹 Clear Text",
                variant="secondary",
                scale=1
            )
            listen_btn = gr.Button(
                "🔊 Re-Play Speech",
                variant="secondary",
                scale=1
            )

        # Translation History Section
        with gr.Accordion("📜 Translation History", open=True):
            history_table = gr.Dataframe(
                headers=["Time", "Source", "Target", "Original Text", "Translated Text"],
                datatype=["str", "str", "str", "str", "str"],
                value=[],
                interactive=False,
                wrap=True
            )
            with gr.Row():
                clear_history_btn = gr.Button("🗑️ Clear History", size="sm", variant="stop")

        # Footer
        gr.Markdown(
            """
            ---
            <center>
            <small style="color: #6b7280;">
            Developed for <b>CodeAlpha Artificial Intelligence Internship</b> • Powered by <code>deep-translator</code> & <code>gTTS</code>
            </small>
            </center>
            """
        )

        # -----------------------------------------------------------------
        # Wire Events
        # -----------------------------------------------------------------
        # Dynamic stats on input change
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

        # Enter key in input textbox also triggers translation
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
# Main Execution Entrypoint
# -------------------------------------------------------------------------
if __name__ == "__main__":
    app = create_app()
    print("Launching AI Language Translation Tool...")
    theme = gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="slate",
        neutral_hue="slate"
    )
    # launch parameters handle theme and CSS cleanly in Gradio 6
    app.launch(theme=theme, css=CUSTOM_CSS, share=False)
