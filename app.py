"""
AI Language Translation Tool
Application: app.py

Author: Saabeer
Project: LanguageTranslation
Description:
A refined, high-contrast Apple iOS-inspired Language Translation application
built with Python, Gradio, deep-translator, and Google Text-to-Speech (gTTS).
Features high-contrast text visibility, native Apple SF Pro typography,
and the requested sequential layout with animated spring transition.
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
# Apple iOS Theme Tokens (Gradio Theme Engine)
# Ensures 100% high-contrast readability in both Light and Dark mode.
# -------------------------------------------------------------------------
def get_ios_theme() -> gr.themes.Soft:
    """
    Constructs a native Apple iOS theme with high-contrast text and surfaces.
    """
    theme = gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="slate",
        neutral_hue="slate",
        radius_size="lg",
        text_size="md",
        font=[
            "-apple-system",
            "BlinkMacSystemFont",
            "SF Pro Text",
            "SF Pro Display",
            "Helvetica Neue",
            "sans-serif"
        ]
    ).set(
        # Canvas Background
        body_background_fill="#F2F2F7",
        body_background_fill_dark="#000000",
        
        # Inset Grouped Card Fill
        block_background_fill="#FFFFFF",
        block_background_fill_dark="#1C1C1E",
        block_border_width="1px",
        block_border_color="rgba(60, 60, 67, 0.15)",
        block_border_color_dark="rgba(255, 255, 255, 0.15)",
        block_radius="18px",
        block_shadow="0 4px 20px rgba(0, 0, 0, 0.04)",
        
        # Primary Action Button (Apple System Blue)
        button_primary_background_fill="#007AFF",
        button_primary_background_fill_hover="#0062CC",
        button_primary_text_color="#FFFFFF",
        
        # Secondary Action Buttons (Apple System Gray Fill)
        button_secondary_background_fill="#E5E5EA",
        button_secondary_background_fill_dark="#2C2C2E",
        button_secondary_text_color="#007AFF",
        button_secondary_text_color_dark="#0A84FF",
        
        # Form Inputs (High-Contrast White / Dark Fill)
        input_background_fill="#FFFFFF",
        input_background_fill_dark="#2C2C2E",
        input_border_color="rgba(60, 60, 67, 0.20)",
        input_border_color_dark="rgba(255, 255, 255, 0.20)",
        input_radius="14px"
    )
    return theme


# -------------------------------------------------------------------------
# Apple iOS Custom CSS (Enhancements & Transitions)
# -------------------------------------------------------------------------
APPLE_IOS_CSS = """
/* Container Layout */
.gradio-container {
    max-width: 820px !important;
    margin: 20px auto 40px auto !important;
    padding: 0 16px !important;
}

/* Apple Header Banner */
.apple-header {
    text-align: center;
    padding: 22px 16px;
    background: #FFFFFF;
    border-radius: 20px;
    border: 1px solid rgba(60, 60, 67, 0.12);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
    margin-bottom: 20px;
}

:is(.dark) .apple-header {
    background: #1C1C1E !important;
    border-color: rgba(255, 255, 255, 0.12) !important;
}

.apple-pill-tag {
    display: inline-block;
    background: rgba(0, 122, 255, 0.10);
    color: #007AFF;
    padding: 4px 14px;
    border-radius: 9999px;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.4px;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.apple-title {
    font-size: 2.2rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.6px !important;
    margin: 2px 0 6px 0 !important;
    line-height: 1.15;
}

.apple-subtitle {
    font-size: 0.96rem !important;
    color: #8E8E93 !important;
    margin: 0 !important;
}

/* Apple Primary Button (Full-Width Pill) */
.apple-translate-btn button {
    background: #007AFF !important;
    background-image: linear-gradient(180deg, #0A84FF 0%, #007AFF 100%) !important;
    color: #FFFFFF !important;
    border-radius: 9999px !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.2px !important;
    padding: 14px 30px !important;
    border: none !important;
    box-shadow: 0 6px 20px rgba(0, 122, 255, 0.35) !important;
    transition: all 0.15s ease !important;
    cursor: pointer !important;
    width: 100% !important;
}

.apple-translate-btn button:hover {
    background-image: linear-gradient(180deg, #007AFF 0%, #0062CC 100%) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(0, 122, 255, 0.42) !important;
}

.apple-translate-btn button:active {
    transform: scale(0.97) !important;
    box-shadow: 0 2px 8px rgba(0, 122, 255, 0.2) !important;
}

/* Result Card with Smooth Spring Transition */
@keyframes iosReveal {
    0% {
        opacity: 0;
        transform: translateY(18px);
    }
    100% {
        opacity: 1;
        transform: translateY(0);
    }
}

.ios-result-section {
    animation: iosReveal 0.35s cubic-bezier(0.16, 1, 0.3, 1) forwards !important;
    margin-top: 14px !important;
    margin-bottom: 20px !important;
    padding: 18px 20px !important;
    background: #FFFFFF !important;
    border-radius: 20px !important;
    border: 1.5px solid rgba(0, 122, 255, 0.25) !important;
    box-shadow: 0 6px 28px rgba(0, 122, 255, 0.08) !important;
}

:is(.dark) .ios-result-section {
    background: #1C1C1E !important;
    border-color: rgba(10, 132, 255, 0.35) !important;
}

.ios-result-tag {
    display: inline-block;
    background: rgba(0, 122, 255, 0.10);
    color: #007AFF;
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 0.8rem;
    font-weight: 700;
    margin-bottom: 8px;
}

/* Apple Secondary Pill Buttons */
button[variant="secondary"] {
    border-radius: 9999px !important;
    font-weight: 600 !important;
    transition: all 0.15s ease !important;
}

button[variant="secondary"]:active {
    transform: scale(0.97) !important;
}

/* Destructive Button */
button[variant="stop"] {
    border-radius: 9999px !important;
    font-weight: 600 !important;
}

/* Input Stats Pill */
.stats-chip {
    font-size: 0.82rem;
    font-weight: 600;
    color: #8E8E93;
    margin-top: 4px;
}

/* Footer */
.apple-footer {
    text-align: center;
    padding: 20px 0 8px 0;
    color: #8E8E93;
    font-size: 0.82rem;
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
        return gr.update(visible=False), "", stats, None, "", history, history

    # Perform real translation
    translated = translate_text(text, source_lang, target_lang)

    # Compute text metrics
    chars, words = count_text_stats(text)
    stats = f"📊 {chars} characters • {words} words"

    # Auto-generate speech audio if translation was successful
    audio_path = None
    if translated and not translated.startswith("Error:") and not translated.startswith("Language Error:"):
        audio_path = generate_tts_audio(translated, target_lang)

    # Result tag
    badge_label = f"✦ Translation Result ({target_lang})"

    # Update history log
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
    Swaps source and target languages, reversing input/output for instant reverse-translation.
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
# Application Builder
# -------------------------------------------------------------------------
def create_app() -> gr.Blocks:
    """
    Constructs the streamlined Apple iOS translation interface.
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

    with gr.Blocks(title="Translate — Apple iOS Experience") as demo:
        # History state management
        history_state = gr.State([])

        # 1. Navigation Header
        gr.HTML("""
        <div class="apple-header">
            <span class="apple-pill-tag">✦ Neural Engine</span>
            <h1 class="apple-title">Translate</h1>
            <p class="apple-subtitle">Instant speech and text translation across 15+ languages</p>
        </div>
        """)

        # 2. Main Input Card: Language Selectors & Text Input Box
        with gr.Group():
            with gr.Row():
                source_dropdown = gr.Dropdown(
                    choices=source_choices,
                    value="English",
                    label="Selected Language (From)",
                    info="Choose input language or Auto Detect"
                )
                target_dropdown = gr.Dropdown(
                    choices=target_choices,
                    value="Telugu",
                    label="Translation Language (To)",
                    info="Choose destination language"
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
        with gr.Row(elem_classes=["apple-translate-btn"]):
            translate_btn = gr.Button(
                "🚀 Translate",
                variant="primary"
            )

        # 4. Under that: Animated Transition Result Card (Revealed on Translate)
        with gr.Column(visible=False, elem_classes=["ios-result-section"]) as result_card:
            result_badge = gr.Markdown(
                "✦ Translation Result",
                elem_classes=["ios-result-tag"]
            )
            output_text = gr.Textbox(
                label="Translated Text",
                placeholder="Translation appears here...",
                lines=4,
                max_lines=8,
                interactive=False,
                **copy_kwarg
            )
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

        # 5. Under that: Inset Grouped History Section
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

        # 6. Apple Footer
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
    print("Launching Apple iOS-Style AI Language Translation Tool...")
    theme = get_ios_theme()
    app.launch(theme=theme, css=APPLE_IOS_CSS, share=False)
