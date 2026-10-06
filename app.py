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
    Constructs a native Apple iOS WindowGlass theme with high-contrast text and frosted surfaces.
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
        # Canvas Background (semi-translucent for window glass backdrop)
        body_background_fill="rgba(240, 244, 252, 0.5)",
        body_background_fill_dark="rgba(14, 18, 28, 0.7)",
        
        # WindowGlass Card Fill
        block_background_fill="rgba(255, 255, 255, 0.72)",
        block_background_fill_dark="rgba(22, 26, 40, 0.76)",
        block_border_width="1px",
        block_border_color="rgba(255, 255, 255, 0.75)",
        block_border_color_dark="rgba(255, 255, 255, 0.16)",
        block_radius="22px",
        block_shadow="0 16px 40px -8px rgba(0, 32, 64, 0.09)",
        
        # Primary Action Button (Apple System Blue)
        button_primary_background_fill="#007AFF",
        button_primary_background_fill_hover="#0062CC",
        button_primary_text_color="#FFFFFF",
        
        # Secondary Action Buttons (Frosted Glass Fill)
        button_secondary_background_fill="rgba(255, 255, 255, 0.75)",
        button_secondary_background_fill_dark="rgba(36, 42, 60, 0.75)",
        button_secondary_text_color="#007AFF",
        button_secondary_text_color_dark="#5AC8FA",
        
        # Form Inputs (Frosted Glass Fill)
        input_background_fill="rgba(255, 255, 255, 0.82)",
        input_background_fill_dark="rgba(30, 35, 50, 0.82)",
        input_border_color="rgba(0, 122, 255, 0.20)",
        input_border_color_dark="rgba(255, 255, 255, 0.18)",
        input_radius="14px"
    )
    return theme


# -------------------------------------------------------------------------
# WindowGlass Background & Extended Layout CSS
# -------------------------------------------------------------------------
APPLE_IOS_CSS = """
/* Background Image & WindowGlass Ambience */
body {
    background-image: 
        linear-gradient(135deg, rgba(240, 244, 252, 0.82), rgba(248, 250, 255, 0.88)),
        url('https://cdn.vectorstock.com/i/1000v/07/99/icon-representing-translation-from-english-vector-53290799.jpg'),
        url('/file=assets/bg_translation.jpg') !important;
    background-position: center center !important;
    background-repeat: no-repeat !important;
    background-size: cover !important;
    background-attachment: fixed !important;
    min-height: 100vh !important;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display", "Helvetica Neue", sans-serif !important;
}

:is(.dark) body {
    background-image: 
        linear-gradient(135deg, rgba(16, 20, 32, 0.88), rgba(24, 30, 46, 0.92)),
        url('https://cdn.vectorstock.com/i/1000v/07/99/icon-representing-translation-from-english-vector-53290799.jpg'),
        url('/file=assets/bg_translation.jpg') !important;
    background-position: center center !important;
    background-repeat: no-repeat !important;
    background-size: cover !important;
    background-attachment: fixed !important;
}

/* Extended Horizontal Layout Container */
.gradio-container {
    max-width: 1100px !important;
    width: 95% !important;
    margin: 24px auto 48px auto !important;
    padding: 0 20px !important;
    background: transparent !important;
}

/* WindowGlass Card Effect (Translucent + Heavy Backdrop Blur) */
.glass-card,
.apple-header,
.ios-result-section,
.gr-group,
div[data-testid="block"] {
    background: rgba(255, 255, 255, 0.72) !important;
    -webkit-backdrop-filter: blur(28px) saturate(190%) !important;
    backdrop-filter: blur(28px) saturate(190%) !important;
    border: 1px solid rgba(255, 255, 255, 0.75) !important;
    border-radius: 24px !important;
    box-shadow: 0 16px 40px -8px rgba(0, 32, 64, 0.09), 0 0 0 1px rgba(255, 255, 255, 0.6) inset !important;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

:is(.dark) .glass-card,
:is(.dark) .apple-header,
:is(.dark) .ios-result-section,
:is(.dark) .gr-group,
:is(.dark) div[data-testid="block"] {
    background: rgba(22, 26, 40, 0.76) !important;
    border: 1px solid rgba(255, 255, 255, 0.16) !important;
    box-shadow: 0 16px 40px -8px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(255, 255, 255, 0.08) inset !important;
}

/* Glass Header Banner */
.apple-header {
    text-align: center;
    padding: 24px 20px;
    margin-bottom: 22px;
}

.apple-pill-tag {
    display: inline-block;
    background: rgba(0, 122, 255, 0.12);
    color: #007AFF;
    padding: 4px 16px;
    border-radius: 9999px;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-bottom: 8px;
    border: 1px solid rgba(0, 122, 255, 0.2);
}

:is(.dark) .apple-pill-tag {
    background: rgba(10, 132, 255, 0.2);
    color: #5AC8FA;
    border-color: rgba(90, 200, 250, 0.3);
}

.apple-title {
    font-size: 2.3rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.6px !important;
    margin: 2px 0 6px 0 !important;
    line-height: 1.15;
}

.apple-subtitle {
    font-size: 0.98rem !important;
    color: #6E6E73 !important;
    margin: 0 !important;
}

:is(.dark) .apple-subtitle {
    color: #98989D !important;
}

/* Frosted Glass Inputs & Textareas */
input, textarea, .gr-input, .gr-box {
    background: rgba(255, 255, 255, 0.82) !important;
    -webkit-backdrop-filter: blur(14px) !important;
    backdrop-filter: blur(14px) !important;
    border: 1px solid rgba(0, 122, 255, 0.18) !important;
    border-radius: 14px !important;
    color: #1C1C1E !important;
    font-size: 1rem !important;
}

:is(.dark) input, :is(.dark) textarea, :is(.dark) .gr-input, :is(.dark) .gr-box {
    background: rgba(30, 35, 50, 0.82) !important;
    border-color: rgba(255, 255, 255, 0.18) !important;
    color: #F2F2F7 !important;
}

/* Apple Primary Button (Vibrant Pill with Glass Shine) */
.apple-translate-btn button {
    background: linear-gradient(180deg, #0A84FF 0%, #007AFF 100%) !important;
    color: #FFFFFF !important;
    border-radius: 9999px !important;
    font-size: 1.15rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.2px !important;
    padding: 15px 32px !important;
    border: 1px solid rgba(255, 255, 255, 0.25) !important;
    box-shadow: 0 8px 26px rgba(0, 122, 255, 0.38), 0 1px 2px rgba(255, 255, 255, 0.4) inset !important;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    cursor: pointer !important;
    width: 100% !important;
}

.apple-translate-btn button:hover {
    background: linear-gradient(180deg, #007AFF 0%, #0062CC 100%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 30px rgba(0, 122, 255, 0.48), 0 1px 2px rgba(255, 255, 255, 0.5) inset !important;
}

.apple-translate-btn button:active {
    transform: scale(0.98) !important;
    box-shadow: 0 4px 12px rgba(0, 122, 255, 0.25) !important;
}

/* Result Card with Spring Animation */
@keyframes iosReveal {
    0% {
        opacity: 0;
        transform: translateY(20px) scale(0.99);
    }
    100% {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

.ios-result-section {
    animation: iosReveal 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards !important;
    margin-top: 16px !important;
    margin-bottom: 22px !important;
    padding: 22px 24px !important;
    border: 1.5px solid rgba(0, 122, 255, 0.35) !important;
}

:is(.dark) .ios-result-section {
    border-color: rgba(10, 132, 255, 0.45) !important;
}

.ios-result-tag {
    display: inline-block;
    background: rgba(0, 122, 255, 0.12);
    color: #007AFF;
    padding: 4px 14px;
    border-radius: 9999px;
    font-size: 0.82rem;
    font-weight: 700;
    margin-bottom: 12px;
}

/* Frosted Glass Secondary Pill Buttons */
button[variant="secondary"] {
    background: rgba(255, 255, 255, 0.75) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    backdrop-filter: blur(16px) !important;
    border: 1px solid rgba(255, 255, 255, 0.8) !important;
    color: #007AFF !important;
    border-radius: 9999px !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05) !important;
    transition: all 0.2s ease !important;
}

button[variant="secondary"]:hover {
    background: rgba(255, 255, 255, 0.95) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08) !important;
}

button[variant="secondary"]:active {
    transform: scale(0.97) !important;
}

:is(.dark) button[variant="secondary"] {
    background: rgba(36, 42, 60, 0.75) !important;
    border-color: rgba(255, 255, 255, 0.15) !important;
    color: #5AC8FA !important;
}

/* Stop / Destructive Button */
button[variant="stop"] {
    border-radius: 9999px !important;
    font-weight: 600 !important;
}

/* Character & Word Stats Pill */
.stats-chip {
    font-size: 0.84rem;
    font-weight: 600;
    color: #6E6E73;
    margin-top: 6px;
}

/* Inset Grouped History Table */
.gr-dataframe {
    border-radius: 16px !important;
    overflow: hidden !important;
}

/* Footer */
.apple-footer {
    text-align: center;
    padding: 24px 0 12px 0;
    color: #6E6E73;
    font-size: 0.84rem;
}

:is(.dark) .apple-footer {
    color: #98989D;
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
            <p class="apple-subtitle">Instant speech and text translation across 130+ languages</p>
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
    app.launch(theme=theme, css=APPLE_IOS_CSS, share=False, allowed_paths=["assets"])
