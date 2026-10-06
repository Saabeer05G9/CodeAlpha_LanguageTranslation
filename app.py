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
        input_background_fill="rgba(255, 255, 255, 0.88)",
        input_background_fill_dark="rgba(30, 36, 54, 0.88)",
        input_border_color="rgba(0, 122, 255, 0.25)",
        input_border_color_dark="rgba(255, 255, 255, 0.20)",
        input_radius="18px",
        input_padding="14px 18px",
        input_text_size="lg",
        input_text_weight="600"
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
.ios-result-section {
    background: rgba(255, 255, 255, 0.74) !important;
    -webkit-backdrop-filter: blur(28px) saturate(190%) !important;
    backdrop-filter: blur(28px) saturate(190%) !important;
    border: 1px solid rgba(255, 255, 255, 0.75) !important;
    border-radius: 24px !important;
    box-shadow: 0 16px 40px -8px rgba(0, 32, 64, 0.09), 0 0 0 1px rgba(255, 255, 255, 0.6) inset !important;
    padding: 22px 24px !important;
    margin-bottom: 20px !important;
    overflow: visible !important;
}

:is(.dark) .glass-card,
:is(.dark) .apple-header,
:is(.dark) .ios-result-section {
    background: rgba(22, 26, 40, 0.78) !important;
    border: 1px solid rgba(255, 255, 255, 0.16) !important;
    box-shadow: 0 16px 40px -8px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(255, 255, 255, 0.08) inset !important;
}

/* Main Input Card: Frosted surface WITHOUT backdrop-filter to keep viewport coordinates for dropdown popover */
.main-input-card {
    background: rgba(255, 255, 255, 0.94) !important;
    border: 1.5px solid rgba(255, 255, 255, 0.9) !important;
    border-radius: 24px !important;
    box-shadow: 0 16px 40px -8px rgba(0, 32, 64, 0.12), 0 0 0 1px rgba(255, 255, 255, 0.8) inset !important;
    padding: 24px 26px !important;
    margin-bottom: 20px !important;
    overflow: visible !important;
    backdrop-filter: none !important;
    -webkit-backdrop-filter: none !important;
    transform: none !important;
}

:is(.dark) .main-input-card {
    background: rgba(22, 26, 42, 0.96) !important;
    border: 1.5px solid rgba(255, 255, 255, 0.16) !important;
    box-shadow: 0 16px 40px -8px rgba(0, 0, 0, 0.6), 0 0 0 1px rgba(255, 255, 255, 0.08) inset !important;
}

/* Ensure Dropdown Floating Menus Are Never Clipped and Always on Top */
.main-input-card,
.language-picker-row,
.gr-row,
.gr-form,
.form,
.gr-group {
    overflow: visible !important;
}

/* =========================================================================
   Apple iOS Language Selector Boxes (Prominent, High-Touch, Luxurious)
   ========================================================================= */
.language-picker-row {
    display: flex !important;
    gap: 18px !important;
    margin-bottom: 18px !important;
    width: 100% !important;
    overflow: visible !important;
}

/* Dropdown Container */
.ios-dropdown-picker,
div[data-testid="dropdown"],
.gr-dropdown {
    position: relative !important;
    z-index: 60 !important;
    overflow: visible !important;
    flex: 1 1 320px !important;
}

/* Dropdown Labels & Helper Info */
.ios-dropdown-picker label > span:first-child,
div[data-testid="dropdown"] label > span:first-child,
.ios-dropdown-picker .block-label {
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    color: #1C1C1E !important;
    letter-spacing: -0.2px !important;
    margin-bottom: 4px !important;
    display: block !important;
}

:is(.dark) .ios-dropdown-picker label > span:first-child,
:is(.dark) div[data-testid="dropdown"] label > span:first-child,
:is(.dark) .ios-dropdown-picker .block-label {
    color: #FFFFFF !important;
}

.ios-dropdown-picker .block-info,
.ios-dropdown-picker label .info,
div[data-testid="dropdown"] .info {
    font-size: 0.85rem !important;
    color: #6E6E73 !important;
    margin-bottom: 8px !important;
}

:is(.dark) .ios-dropdown-picker .block-info,
:is(.dark) .ios-dropdown-picker label .info,
:is(.dark) div[data-testid="dropdown"] .info {
    color: #98989D !important;
}

/* The Selector Box Outer Wrap (Taller, Prominent, Pill-Rounded, WindowGlass) */
.ios-dropdown-picker .wrap,
div[data-testid="dropdown"] .wrap,
.ios-dropdown-picker .container .wrap {
    min-height: 58px !important;
    height: 58px !important;
    border-radius: 18px !important;
    background: rgba(255, 255, 255, 0.90) !important;
    -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
    backdrop-filter: blur(20px) saturate(180%) !important;
    border: 1.5px solid rgba(0, 122, 255, 0.28) !important;
    box-shadow: 0 4px 16px rgba(0, 32, 64, 0.07), 0 1px 2px rgba(255, 255, 255, 0.85) inset !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
    padding: 0 16px !important;
    position: relative !important;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    overflow: visible !important;
}

:is(.dark) .ios-dropdown-picker .wrap,
:is(.dark) div[data-testid="dropdown"] .wrap,
:is(.dark) .ios-dropdown-picker .container .wrap {
    background: rgba(30, 36, 54, 0.90) !important;
    border-color: rgba(255, 255, 255, 0.22) !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4), 0 1px 2px rgba(255, 255, 255, 0.08) inset !important;
}

.ios-dropdown-picker .wrap:hover,
div[data-testid="dropdown"] .wrap:hover {
    border-color: #007AFF !important;
    box-shadow: 0 6px 20px rgba(0, 122, 255, 0.18), 0 1px 2px rgba(255, 255, 255, 0.9) inset !important;
    transform: translateY(-1px) !important;
}

.ios-dropdown-picker .wrap:focus-within,
div[data-testid="dropdown"] .wrap:focus-within {
    border-color: #007AFF !important;
    box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.25), 0 8px 24px rgba(0, 122, 255, 0.15) !important;
}

:is(.dark) .ios-dropdown-picker .wrap:focus-within,
:is(.dark) div[data-testid="dropdown"] .wrap:focus-within {
    border-color: #5AC8FA !important;
    box-shadow: 0 0 0 3px rgba(90, 200, 250, 0.3), 0 8px 24px rgba(0, 0, 0, 0.5) !important;
}

/* Secondary Wrap and Inner Structure */
.ios-dropdown-picker .wrap-inner,
div[data-testid="dropdown"] .wrap-inner,
.ios-dropdown-picker .secondary-wrap,
div[data-testid="dropdown"] .secondary-wrap {
    width: 100% !important;
    height: 100% !important;
    display: flex !important;
    align-items: center !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    position: relative !important;
    cursor: pointer !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* Dropdown Input Text (Crisp, Large Typography, Clear Selection) */
.ios-dropdown-picker input,
div[data-testid="dropdown"] input,
.ios-dropdown-picker input[role="combobox"],
div[data-testid="dropdown"] input[role="combobox"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    font-size: 1.15rem !important;
    font-weight: 600 !important;
    color: #1C1C1E !important;
    letter-spacing: -0.2px !important;
    cursor: pointer !important;
    width: 100% !important;
    height: 100% !important;
    padding: 0 36px 0 4px !important;
    outline: none !important;
}

:is(.dark) .ios-dropdown-picker input,
:is(.dark) div[data-testid="dropdown"] input,
:is(.dark) .ios-dropdown-picker input[role="combobox"],
:is(.dark) div[data-testid="dropdown"] input[role="combobox"] {
    color: #FFFFFF !important;
}

/* Selecting Arrow / Chevron (Prominent, Apple Blue, Elegant) */
.ios-dropdown-picker .icon-wrap,
div[data-testid="dropdown"] .icon-wrap,
.icon-wrap.svelte-1xfsv4t {
    position: absolute !important;
    right: 16px !important;
    top: 50% !important;
    transform: translateY(-50%) !important;
    width: 32px !important;
    height: 32px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    pointer-events: none !important;
    color: #007AFF !important;
    opacity: 0.9 !important;
}

:is(.dark) .ios-dropdown-picker .icon-wrap,
:is(.dark) div[data-testid="dropdown"] .icon-wrap,
:is(.dark) .icon-wrap.svelte-1xfsv4t {
    color: #5AC8FA !important;
}

.ios-dropdown-picker svg.dropdown-arrow,
div[data-testid="dropdown"] svg.dropdown-arrow,
.ios-dropdown-picker .icon-wrap svg,
div[data-testid="dropdown"] .icon-wrap svg,
.ios-dropdown-picker svg,
div[data-testid="dropdown"] svg,
.icon-wrap.svelte-1xfsv4t svg {
    width: 24px !important;
    height: 24px !important;
    min-width: 24px !important;
    min-height: 24px !important;
    fill: currentColor !important;
    color: #007AFF !important;
    transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

:is(.dark) .ios-dropdown-picker svg.dropdown-arrow,
:is(.dark) div[data-testid="dropdown"] svg.dropdown-arrow,
:is(.dark) .ios-dropdown-picker .icon-wrap svg,
:is(.dark) div[data-testid="dropdown"] .icon-wrap svg,
:is(.dark) .ios-dropdown-picker svg,
:is(.dark) div[data-testid="dropdown"] svg,
:is(.dark) .icon-wrap.svelte-1xfsv4t svg {
    color: #5AC8FA !important;
}

/* Arrow rotation on focus */
.ios-dropdown-picker .wrap:focus-within svg.dropdown-arrow,
div[data-testid="dropdown"] .wrap:focus-within svg.dropdown-arrow,
.ios-dropdown-picker .wrap:focus-within .icon-wrap svg,
div[data-testid="dropdown"] .wrap:focus-within .icon-wrap svg {
    transform: rotate(180deg) !important;
}

/* =========================================================================
   Dropdown Popover Menu (Spacious, Scrollable, Expansive 130+ Languages)
   ========================================================================= */
.options,
div.options,
ul.options,
.options.svelte-1ou0lab,
.dropdown-menu,
div[role="listbox"],
ul[role="listbox"] {
    position: fixed !important;
    z-index: 999999 !important;
    pointer-events: auto !important;
    max-height: 480px !important;
    min-height: 260px !important;
    min-width: 320px !important;
    background: rgba(255, 255, 255, 0.98) !important;
    -webkit-backdrop-filter: blur(32px) saturate(200%) !important;
    backdrop-filter: blur(32px) saturate(200%) !important;
    border: 1.5px solid rgba(0, 122, 255, 0.32) !important;
    border-radius: 20px !important;
    box-shadow: 0 24px 60px rgba(0, 32, 64, 0.22), 0 0 0 1px rgba(255, 255, 255, 0.9) inset !important;
    padding: 8px !important;
    overflow: hidden !important;
    opacity: 1 !important;
    visibility: visible !important;
}

:is(.dark) .options,
:is(.dark) div.options,
:is(.dark) ul.options,
:is(.dark) .options.svelte-1ou0lab,
:is(.dark) .dropdown-menu,
:is(.dark) div[role="listbox"],
:is(.dark) ul[role="listbox"] {
    background: rgba(24, 30, 46, 0.98) !important;
    border-color: rgba(90, 200, 250, 0.35) !important;
    box-shadow: 0 24px 60px rgba(0, 0, 0, 0.7), 0 0 0 1px rgba(255, 255, 255, 0.12) inset !important;
}

/* Option List Container */
.option-list,
ul.option-list,
.option-list.svelte-1ou0lab {
    max-height: 460px !important;
    min-height: 240px !important;
    overflow-y: auto !important;
    scrollbar-width: thin !important;
    scrollbar-color: rgba(0, 122, 255, 0.4) transparent !important;
    padding: 0 !important;
    margin: 0 !important;
    list-style: none !important;
}

/* Individual Language Item */
li.item,
.item,
[role="option"],
li[data-testid="dropdown-option"],
.item.svelte-1ou0lab {
    padding: 12px 18px !important;
    min-height: 46px !important;
    font-size: 1.05rem !important;
    font-weight: 500 !important;
    color: #1C1C1E !important;
    cursor: pointer !important;
    border-radius: 12px !important;
    margin-bottom: 2px !important;
    display: flex !important;
    align-items: center !important;
    transition: background 0.15s ease, color 0.15s ease, transform 0.1s ease !important;
}

/* CRITICAL: Delegate all clicks on child spans / text directly to the <li> with data-index */
li.item *,
.item *,
[role="option"] *,
li[data-testid="dropdown-option"] *,
.item.svelte-1ou0lab *,
.inner-item,
.inner-item *,
.inner-item.svelte-1ou0lab,
.inner-item.svelte-1ou0lab * {
    pointer-events: none !important;
}

:is(.dark) li.item,
:is(.dark) .item,
:is(.dark) [role="option"],
:is(.dark) li[data-testid="dropdown-option"],
:is(.dark) .item.svelte-1ou0lab {
    color: #F2F2F7 !important;
}

/* Quick-Select Pills */
.quick-pills-row {
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
    margin-bottom: 12px !important;
    flex-wrap: wrap !important;
}
.pills-label {
    font-size: 0.84rem !important;
    color: #007AFF !important;
    font-weight: 700 !important;
    margin-right: 4px !important;
}
:is(.dark) .pills-label {
    color: #5AC8FA !important;
}
.lang-pill-btn {
    border-radius: 9999px !important;
    padding: 3px 12px !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    background: rgba(0, 122, 255, 0.09) !important;
    border: 1px solid rgba(0, 122, 255, 0.22) !important;
    color: #007AFF !important;
    cursor: pointer !important;
    transition: all 0.15s ease !important;
}
.lang-pill-btn:hover {
    background: #007AFF !important;
    color: #FFFFFF !important;
    transform: translateY(-1px) !important;
}
:is(.dark) .lang-pill-btn {
    background: rgba(10, 132, 255, 0.18) !important;
    border-color: rgba(90, 200, 250, 0.3) !important;
    color: #5AC8FA !important;
}
:is(.dark) .lang-pill-btn:hover {
    background: #0A84FF !important;
    color: #FFFFFF !important;
}

/* Hover and Selected States */
li.item:hover,
.item:hover,
[role="option"]:hover,
li[data-testid="dropdown-option"]:hover,
.item.svelte-1ou0lab:hover,
.item.selected,
.active.svelte-1ou0lab,
[role="option"][aria-selected="true"] {
    background: rgba(0, 122, 255, 0.14) !important;
    color: #007AFF !important;
    font-weight: 700 !important;
    padding-left: 22px !important;
}

:is(.dark) li.item:hover,
:is(.dark) .item:hover,
:is(.dark) [role="option"]:hover,
:is(.dark) li[data-testid="dropdown-option"]:hover,
:is(.dark) .item.svelte-1ou0lab:hover,
:is(.dark) .item.selected,
:is(.dark) .active.svelte-1ou0lab,
:is(.dark) [role="option"][aria-selected="true"] {
    background: rgba(10, 132, 255, 0.3) !important;
    color: #5AC8FA !important;
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
# Client-Side Event Delegator (Injected via launch(head=...))
# Guarantees that clicks on inner spans/text always set data-index,
# and clicking anywhere on the selector box opens the dropdown list.
# -------------------------------------------------------------------------
DROPDOWN_FIX_JS = """
<script>
(function() {
    // 1. Guarantee option clicks land on or have valid data-index
    function fixDropdownTarget(e) {
        var target = e.target;
        if (!target) return;
        if (target.nodeType === 3) {
            target = target.parentElement;
        }
        if (!target) return;

        // Check if click is on or inside an option item
        var li = target.closest('li[data-index], [role="option"][data-index], .item[data-index], li[data-testid="dropdown-option"][data-index]');
        if (li && li.dataset && li.dataset.index !== undefined) {
            if (target !== li && target.dataset) {
                target.dataset.index = li.dataset.index;
            }
        }
    }

    // 2. Guarantee touching/clicking anywhere on the selector box opens the dropdown
    function handleDropdownWrapClick(e) {
        var wrap = e.target.closest('.ios-dropdown-picker .wrap, div[data-testid="dropdown"] .wrap, .ios-dropdown-picker');
        if (wrap) {
            // Do not steal focus if user is already clicking inside the open listbox menu
            if (!e.target.closest('.options, [role="listbox"], ul.options')) {
                var input = wrap.querySelector('input[role="combobox"], input');
                if (input && document.activeElement !== input) {
                    input.focus();
                }
            }
        }
    }

    // Capture phase listeners (runs before Gradio's internal handlers)
    window.addEventListener('mousedown', fixDropdownTarget, true);
    window.addEventListener('pointerdown', fixDropdownTarget, true);
    window.addEventListener('touchstart', fixDropdownTarget, true);
    window.addEventListener('click', fixDropdownTarget, true);
    window.addEventListener('click', handleDropdownWrapClick, true);
})();
</script>
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
        with gr.Column(elem_classes=["main-input-card"]):
            with gr.Row(elem_classes=["language-picker-row"]):
                source_dropdown = gr.Dropdown(
                    choices=source_choices,
                    value="English",
                    label="Selected Language (From)",
                    info="Choose input language or Auto Detect (130+ languages)",
                    interactive=True,
                    scale=1,
                    min_width=320,
                    num_choices_shown=None,
                    elem_classes=["ios-dropdown-picker"]
                )
                target_dropdown = gr.Dropdown(
                    choices=target_choices,
                    value="Telugu",
                    label="Translation Language (To)",
                    info="Choose destination language (130+ languages)",
                    interactive=True,
                    scale=1,
                    min_width=320,
                    num_choices_shown=None,
                    elem_classes=["ios-dropdown-picker"]
                )

            # Quick-Select Apple Pills for instant 1-tap switching
            with gr.Row(elem_classes=["quick-pills-row"]):
                gr.Markdown("✦ **Quick From:**", elem_classes=["pills-label"])
                auto_src_btn = gr.Button("Auto Detect", size="sm", elem_classes=["lang-pill-btn"])
                en_src_btn = gr.Button("English", size="sm", elem_classes=["lang-pill-btn"])
                es_src_btn = gr.Button("Spanish", size="sm", elem_classes=["lang-pill-btn"])
                fr_src_btn = gr.Button("French", size="sm", elem_classes=["lang-pill-btn"])
                de_src_btn = gr.Button("German", size="sm", elem_classes=["lang-pill-btn"])
                hi_src_btn = gr.Button("Hindi", size="sm", elem_classes=["lang-pill-btn"])
                te_src_btn = gr.Button("Telugu", size="sm", elem_classes=["lang-pill-btn"])

            with gr.Row(elem_classes=["quick-pills-row"]):
                gr.Markdown("✦ **Quick To:**", elem_classes=["pills-label"])
                te_tgt_btn = gr.Button("Telugu", size="sm", elem_classes=["lang-pill-btn"])
                hi_tgt_btn = gr.Button("Hindi", size="sm", elem_classes=["lang-pill-btn"])
                ta_tgt_btn = gr.Button("Tamil", size="sm", elem_classes=["lang-pill-btn"])
                kn_tgt_btn = gr.Button("Kannada", size="sm", elem_classes=["lang-pill-btn"])
                ml_tgt_btn = gr.Button("Malayalam", size="sm", elem_classes=["lang-pill-btn"])
                bn_tgt_btn = gr.Button("Bengali", size="sm", elem_classes=["lang-pill-btn"])
                es_tgt_btn = gr.Button("Spanish", size="sm", elem_classes=["lang-pill-btn"])
                fr_tgt_btn = gr.Button("French", size="sm", elem_classes=["lang-pill-btn"])
                de_tgt_btn = gr.Button("German", size="sm", elem_classes=["lang-pill-btn"])
                ja_tgt_btn = gr.Button("Japanese", size="sm", elem_classes=["lang-pill-btn"])
                ar_tgt_btn = gr.Button("Arabic", size="sm", elem_classes=["lang-pill-btn"])
                ru_tgt_btn = gr.Button("Russian", size="sm", elem_classes=["lang-pill-btn"])

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

        # Quick-Select Source Pill Buttons (Instant 1-Tap Switching)
        auto_src_btn.click(fn=lambda: "Auto Detect", inputs=[], outputs=[source_dropdown])
        en_src_btn.click(fn=lambda: "English", inputs=[], outputs=[source_dropdown])
        es_src_btn.click(fn=lambda: "Spanish", inputs=[], outputs=[source_dropdown])
        fr_src_btn.click(fn=lambda: "French", inputs=[], outputs=[source_dropdown])
        de_src_btn.click(fn=lambda: "German", inputs=[], outputs=[source_dropdown])
        hi_src_btn.click(fn=lambda: "Hindi", inputs=[], outputs=[source_dropdown])
        te_src_btn.click(fn=lambda: "Telugu", inputs=[], outputs=[source_dropdown])

        # Quick-Select Target Pill Buttons (Instant 1-Tap Switching)
        te_tgt_btn.click(fn=lambda: "Telugu", inputs=[], outputs=[target_dropdown])
        hi_tgt_btn.click(fn=lambda: "Hindi", inputs=[], outputs=[target_dropdown])
        ta_tgt_btn.click(fn=lambda: "Tamil", inputs=[], outputs=[target_dropdown])
        kn_tgt_btn.click(fn=lambda: "Kannada", inputs=[], outputs=[target_dropdown])
        ml_tgt_btn.click(fn=lambda: "Malayalam", inputs=[], outputs=[target_dropdown])
        bn_tgt_btn.click(fn=lambda: "Bengali", inputs=[], outputs=[target_dropdown])
        es_tgt_btn.click(fn=lambda: "Spanish", inputs=[], outputs=[target_dropdown])
        fr_tgt_btn.click(fn=lambda: "French", inputs=[], outputs=[target_dropdown])
        de_tgt_btn.click(fn=lambda: "German", inputs=[], outputs=[target_dropdown])
        ja_tgt_btn.click(fn=lambda: "Japanese", inputs=[], outputs=[target_dropdown])
        ar_tgt_btn.click(fn=lambda: "Arabic", inputs=[], outputs=[target_dropdown])
        ru_tgt_btn.click(fn=lambda: "Russian", inputs=[], outputs=[target_dropdown])

    return demo


# -------------------------------------------------------------------------
# Application Entry Point
# -------------------------------------------------------------------------
if __name__ == "__main__":
    app = create_app()
    print("Launching Apple iOS-Style AI Language Translation Tool...")
    theme = get_ios_theme()
    app.launch(theme=theme, css=APPLE_IOS_CSS, head=DROPDOWN_FIX_JS, share=False, allowed_paths=["assets"])
