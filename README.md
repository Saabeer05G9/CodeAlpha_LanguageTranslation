# AI Language Translation Tool 🌐

An interactive, AI-powered multi-language translation web application developed with **Python**, **Gradio**, **deep-translator**, and **Google Text-to-Speech (gTTS)**.

---

## 📌 CodeAlpha Internship Context

This project was developed as **Task 1: Language Translation Tool** for the **CodeAlpha Artificial Intelligence Internship**.

- **Organization:** CodeAlpha
- **Track:** Artificial Intelligence Internship
- **Task:** Task 1 — Language Translation Tool
- **Developer:** Saabeer
- **Repository:** `Saabeer05G9/CodeAlpha_LanguageTranslation`

---

## 📖 Project Overview

The **AI Language Translation Tool** enables users to translate text across multiple languages with speed, accuracy, and ease. In addition to high-fidelity translation, the application provides pronunciation playback using Text-to-Speech, live text metrics (character & word count), one-click language swapping, and an ongoing translation history log.

The project is structured to run smoothly in both local environments (`app.py`) and cloud environments like **Google Colab** (`notebooks/translation_tool.ipynb`).

---

## ✨ Features

### Core Features (Required)
* **Text Input Area:** Multi-line text box for typing or pasting content to translate.
* **Source Language Selection:** Dropdown supporting 15+ major global and regional languages plus **Auto-Detect**.
* **Target Language Selection:** Select desired destination language from standard ISO-supported options.
* **Translate Engine:** Performs real translation using `deep-translator` with automatic fallback handling.
* **Clear Output Display:** Clean, read-only translated text box.

### Professional & Usability Enhancements
* 🔄 **Swap Languages:** Instantly swaps source and target languages and reverses the translated text for reverse verification.
* 🧹 **Clear Text:** One-click reset for inputs, outputs, live counters, and audio players.
* 📋 **Copy to Clipboard:** Convenient one-click copy button integrated into text cards.
* 🔊 **Text-to-Speech (TTS):** Uses `gTTS` to generate natural voice pronunciation of translated text.
* 📊 **Live Word & Character Counter:** Real-time metrics updating dynamically as you type.
* 📜 **Translation History:** Chronological log tracking recent translations with timestamp, source, target, and results.
* 🛡️ **Graceful Error Handling:** Protects against empty input, network errors, and unsupported requests without crashing the UI.

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
CodeAlpha_LanguageTranslation/
│
├── app.py                      # Main standalone web application (Gradio)
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
git clone https://github.com/Saabeer05G9/CodeAlpha_LanguageTranslation.git
cd CodeAlpha_LanguageTranslation
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

### Option A: Run Standalone Web App
Execute `app.py`:
```bash
python app.py
```
After launch, open your browser at the local URL displayed in the terminal (typically `http://127.0.0.1:7860`).

---

## ☁️ Running in Google Colab

1. Open [Google Colab](https://colab.research.google.com/).
2. Select **File → Open Notebook → GitHub** (or upload `notebooks/translation_tool.ipynb`).
3. Enter `Saabeer05G9/CodeAlpha_LanguageTranslation` and open `notebooks/translation_tool.ipynb`.
4. Run each cell sequentially from top to bottom.
5. In the final cell, `demo.launch(share=True)` will generate a public `.gradio.live` link to interact with the tool from any device.

---

## 📸 Screenshots

*(Add screenshots of your running app and translation examples here)*

| Interface View | Feature Demonstration |
| :---: | :---: |
| *App Overview* | *Translation & TTS in Action* |

---

## 🔮 Future Improvements

- **Document Translation:** Support uploading `.txt`, `.docx`, or `.pdf` files for full document translation.
- **Speech-to-Text Input:** Allow microphone voice input using OpenAI Whisper or Web Speech API.
- **Offline Translation:** Integrate lightweight offline models (such as HuggingFace `Helsinki-NLP/opus-mt`).
- **Export History:** Download recent translation records as `.csv` or `.json`.

---

## 📄 License & Attribution

Developed with ❤️ by **Saabeer** as part of the **CodeAlpha AI Internship Program**.  
Feel free to star ⭐ the repository if you found this helpful!
