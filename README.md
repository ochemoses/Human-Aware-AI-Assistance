# Human-Aware AI Assistance – Real-Time Conversation System

A Python-based AI assistant that **detects when a person is present**, **listens to their voice**, **understands their question using an LLM**, and **responds out loud** using text-to-speech. The entire interaction is hands-free and happens automatically in real time.

---

## Table of Contents

* [Project Overview](#project-overview)
* [Features](#features)
* [System Requirements](#system-requirements)
* [Installation Guide](#installation-guide)
* [Project Structure](#project-structure)
* [How It Works](#how-it-works)
* [Running the Project](#running-the-project)
* [Troubleshooting](#troubleshooting)
* [Configuration Tips](#configuration-tips)
* [Future Enhancements](#future-enhancements)
* [Contributing](#contributing)
* [License](#license)
* [FAQ](#faq)

---

## Project Overview

**Human-Aware AI Assistance** is an intelligent, vision-driven conversational system that activates only when a person is detected by the webcam.

The pipeline works as follows:

1. **Person Detection** – YOLO detects a human in the camera frame
2. **Speech Recognition (STT)** – Vosk listens and converts speech to text
3. **Language Understanding** – Google Gemini processes the request
4. **Speech Output (TTS)** – pyttsx3 speaks the AI response

This creates a natural, real-time conversational experience with no buttons, clicks, or manual triggers.

---

## Features

* ✅ Real-time person detection using YOLO
* ✅ Hands-free interaction (no keyboard or mouse)
* ✅ Offline speech-to-text with Vosk
* ✅ AI-powered responses using Google Gemini
* ✅ Natural text-to-speech responses (pyttsx3)
* ✅ Continuous conversation flow
* ✅ Voice-based exit commands ("bye", "exit", "quit")

---

## System Requirements

### Minimum Requirements

* **OS**: Windows 10/11 (Linux/macOS supported with minor changes)
* **Python**: 3.10 or higher (3.10–3.11 recommended)
* **RAM**: 8 GB minimum (16 GB recommended)
* **Webcam**: Built-in or USB camera
* **Microphone**: Built-in or USB microphone
* **Speakers / Headphones**

### Recommended Hardware

* NVIDIA GPU (CUDA) for faster YOLO inference
* Multi-core CPU (Intel i5/i7 or AMD Ryzen 5+)

---

## Installation Guide

### Step 1: Clone the Repository

```bash
git clone https://github.com/ochemoses/Human-Aware-AI-Assistance.git
cd Human-Aware-AI-Assistance
```

---

### Step 2: Create and Activate a Virtual Environment

```bash
python -m venv AI_Assistance_venv

# Windows
AI_Assistance_venv\Scripts\activate

# macOS / Linux
source AI_Assistance_venv/bin/activate
```

---

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install ultralytics vosk pysoundfile pyttsx3 opencv-python genai
```

#### PyAudio Installation (Important)

**Windows**

```bash
pip install pipwin
pipwin install pyaudio
```

**macOS**

```bash
brew install portaudio
pip install pyaudio
```

**Linux**

```bash
sudo apt-get install portaudio19-dev
pip install pyaudio
```

---

### Step 4: Download the Vosk Model

Download and extract the following model into the project root:

* `vosk-model-small-en-us-0.15`

Download from: [https://alphacephei.com/vosk/models](https://alphacephei.com/vosk/models)

---

### Step 5: Environment Configuration

1. Copy the example environment file:

```bash
# Windows
Copy-Item config.example.env .env

# macOS / Linux
cp config.example.env .env
```

2. Add your **Gemini API key** to `.env`
3. (Optional) Install dotenv support:

```bash
pip install python-dotenv
```

4. Load environment variables in `main.py`:

```python
from dotenv import load_dotenv
load_dotenv()
```

---

## Project Structure

```
Human-Aware-AI-Assistance/
│
├── main.py                  # Entry point (run this)
├── README.md
│
├── Yolo.py                  # Person detection module
├── STT.py                   # Speech-to-text (Vosk)
├── LLM.py                   # Gemini AI logic
├── TTS.py                   # Text-to-speech (pyttsx3)
│
├── vosk-model-small-en-us-0.15/
│   ├── am/
│   ├── conf/
│   ├── graph/
│   ├── ivector/
│   └── README
│
└── AI_Assistance_venv/       # Virtual environment (do not commit)
```

> ⚠️ Add `AI_Assistance_venv/` to `.gitignore`

---

## How It Works

```
Webcam
  ↓
YOLO (Person Detection)
  ↓
Speech-to-Text (Vosk)
  ↓
LLM (Gemini)
  ↓
Text-to-Speech (pyttsx3)
  ↓
Speakers
```

Each module runs sequentially, creating a smooth real-time conversation loop.

---

## Running the Project

### Prerequisites

* Virtual environment activated
* Vosk model present
* `GEMINI_API_KEY` set in `.env` or system environment

### Start the System

```bash
python main.py
```

### Usage Flow

1. Look at the camera
2. AI detects your presence
3. AI greets you
4. Speak naturally
5. AI responds out loud
6. Say **"bye"** to exit

---

## Troubleshooting

### Gemini Import Errors

```bash
pip install genai
# or
pip install google-generativeai
```

### Webcam Not Detected

Try different camera indices or DirectShow:

```python
cv2.VideoCapture(0, cv2.CAP_DSHOW)
```

### PyAudio Issues

Follow the OS-specific installation steps above.

---

## Configuration Tips

### Adjust YOLO Accuracy / Speed

```python
conf=0.6  # higher = fewer false positives
```

### Change TTS Speed

```python
self.tts_rate = 150
self.tts_volume = 1.0
```

### Gemini Model Naming

✅ Correct:

```python
gemini-2.5-flash
```

❌ Incorrect:

```python
gemini 2.5 flash
```

---

## Future Enhancements

* Wake-word detection
* Multi-language support
* Emotion recognition
* Conversation memory
* Face recognition
* Web dashboard
* Database logging
* Multi-threading
* GPU acceleration

---

## Contributing

Contributions are welcome!

* Open an issue
* Submit a pull request
* Clearly document changes

---

## License

This project is open source and intended for learning and research purposes.

---

## FAQ

**Do I need internet?**
Yes, for Gemini responses. YOLO and Vosk work offline.

**Is it cross-platform?**
Yes. Windows, Linux, and macOS are supported.

**Can I change the AI personality?**
Yes. Edit the system prompt in `LLM.py`.

---

**Made with ❤️ for AI and Computer Vision Enthusiasts**
