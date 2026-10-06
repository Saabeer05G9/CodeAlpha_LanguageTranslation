# Translate AI — iOS-Style Language Translation Tool 🌐

An intuitive, AI-powered multi-language translation web application featuring an **Apple iOS Human Interface Guidelines (HIG)** aesthetic, built with **Python**, **Gradio**, **deep-translator**, and **Google Text-to-Speech (gTTS)**.

---

## 📖 Project Overview

**Translate AI** is designed to provide seamless, reliable translation across 15+ major languages with the polish and responsiveness of a native iOS application. In addition to high-fidelity text translation, the application includes natural speech pronunciation (TTS), dynamic word and character counters, instant language swapping, and an ongoing translation history log.

The project is structured to run smoothly in both local environments (`app.py`) and cloud runtimes like **Google Colab** (`notebooks/translation_tool.ipynb`).

---

##  iOS Design System Highlights

* **San Francisco Typography & Apple System Fonts:** Crystal-clear visual hierarchy using `-apple-system`, `SF Pro Display`, and `Plus Jakarta Sans`.
* **Vibrant Glassmorphism & Continuous Radii:** Soft squircle corner geometry (`border-radius: 20px`), subtle drop shadows, and clean grouped surfaces.
* **Apple Segmented Pickers & Pill Controls:** Pill-shaped action buttons (Translate, Swap ⇄, Clear ✕, Listen 🔊) with tactile spring interactions.
* **iOS Inset Grouped History:** History logs styled after native iOS Settings and Notes recents with smooth disclosures.

---

## ✨ Features

### Core Functionality
* **Dual-Pane Interface:** Clean side-by-side cards for source text and translated output.
* **Smart Language Detection:** Choose specific input language or use **Auto Detect** (`auto`).
* **15+ Supported Languages:** Full ISO-supported coverage for major Indian and international languages.
* **Resilient Translation Engine:** Uses `deep-translator` with automatic fallback handling to ensure 100% uptime without service interruptions.
* **Integrated Copy Action:** One-click clipboard copy directly on text cards.

### Productivity & Audio Tools
* ⇄ **Swap Languages:** Instantly flips source and target languages and reverses translated text for quick back-translation.
* ✕ **Clear Text:** One-click reset for input text, translation output, metrics, and audio player.
* 🔊 **Speech Pronunciation (TTS):** Uses `gTTS` to generate natural voice pronunciation of translated text across all supported languages.
* 📊 **Live Word & Character Counter:** Real-time metrics updating dynamically as you type.
* 📜 **Translation History:** Chronological log tracking recent translations with timestamp, source, target, and output.
* 🛡️ **Zero-Crash Exception Shield:** Catches empty inputs, network timeouts, and invalid requests gracefully with informative inline notifications.

---

## 🛠️ Technologies Used

| Technology | Purpose |
| :--- | :--- |
| **Python 3.10+ / 3.13** | Core programming language |
| **Gradio (v6.x)** | Clean, responsive web user interface |
| **deep-translator** | Translation framework interfacing with translation services |
| **GoogleTranslator** | Primary translation provider |
| **MyMemoryTranslator** | Resilient fallback translation provider (handles IP rate limits) |
| **gTTS** | Google Text-to-Speech library for audio pronunciation |
| **Jupyter Notebook** | Interactive development, testing, and Google Colab execution |

---

## ⚙️ How It Works

The architecture separates UI components from core translation logic:

```text
User Input Text
      ↓
Language Selection (Source & Target)
      ↓
Validation & ISO Code Mapping (get_language_code)
      ↓
Translation Service (GoogleTranslator / Fallback MyMemoryTranslator)
      ↓
Text Processing & Word/Char Counter (count_text_stats)
      ↓
Text-to-Speech Audio Generation (gTTS)
      ↓
Render Output, Play Audio & Update History Log
```

---

## 📁 Project Structure

```text
LanguageTranslation/
│
├── app.py                      # Main standalone web application (iOS-Styled Gradio App)
├── translation.py              # Modular translation engine, language config & TTS logic
├── requirements.txt            # Project dependencies
├── README.md                   # Complete documentation
├── .gitignore                  # Git ignore rules for security and clean tracking
│
├── notebooks/
│   └── translation_tool.ipynb  # Step-by-step development & Colab-ready notebook
│
├── screenshots/                # Application UI screenshots and demo media
│
└── assets/                     # Project banners and graphic assets
```

---

## 🌍 Supported Languages

The application supports a practical set of widely used languages, including major Indian and international languages:

1. **English** (`en`)
2. **Telugu** (`te`)
3. **Hindi** (`hi`)
4. **Tamil** (`ta`)
5. **Kannada** (`kn`)
6. **Malayalam** (`ml`)
7. **Marathi** (`mr`)
8. **Bengali** (`bn`)
9. **Gujarati** (`gu`)
10. **Spanish** (`es`)
11. **French** (`fr`)
12. **German** (`de`)
13. **Japanese** (`ja`)
14. **Chinese (Simplified)** (`zh-CN`)
15. **Arabic** (`ar`)
* *Source language also supports **Auto Detect** (`auto`).*

---

## 🚀 Installation & Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Saabeer05G9/LanguageTranslation.git
cd LanguageTranslation
```

### 2. (Optional) Create a Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 💻 Running the Project

### Standalone Web App
Execute `app.py`:
```bash
python app.py
```
Open your browser at `http://127.0.0.1:7860`.

---

## ☁️ Running in Google Colab

1. Open [Google Colab](https://colab.research.google.com/).
2. Select **File → Open Notebook → GitHub** (or upload `notebooks/translation_tool.ipynb`).
3. Open `notebooks/translation_tool.ipynb`.
4. Run each cell sequentially from top to bottom.
5. In the final cell, `demo.launch(share=True)` will generate a public `.gradio.live` link to interact with the tool from any device.

---

## 📸 Screenshots

| Interface View | Feature Demonstration |
| :---: | :---: |
| *iOS-Style Interface Overview* | *Translation & TTS in Action* |

---

## 🔮 Future Improvements

- **Document Translation:** Support uploading `.txt`, `.docx`, or `.pdf` files for full document translation.
- **Speech-to-Text Input:** Allow microphone voice input using OpenAI Whisper or Web Speech API.
- **Offline Translation:** Integrate lightweight offline models (such as HuggingFace `Helsinki-NLP/opus-mt`).
- **Export History:** Download recent translation records as `.csv` or `.json`.

---

## 📄 License & Attribution

Developed with ❤️ by **Saabeer**.  
Feel free to star ⭐ the repository if you found this helpful!
