# Human Aware AI Assistance - Real-Time Conversation System

A Python-based AI assistant that detects people using computer vision, listens to their voice, processes their queries with AI, and responds using text-to-speech. It creates a real-time conversational experience without any manual interaction needed.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation Guide](#installation-guide)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Running the Project](#running-the-project)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)

---

## Project Overview

This project creates an intelligent AI assistant that:
1. **Detects** when a person appears on your webcam using YOLO (You Only Look Once)
2. **Listens** to your voice using Vosk speech recognition
3. **Understands** your questions using Gemini LLM (Language Model)
4. **Responds** with spoken answers using pyttsx3 text-to-speech

It works like a real-time conversation with an AI that only activates when it sees you!

---

## Features

- ✅ Real-time person detection (no button needed)
- ✅ Offline speech recognition for STT (Vosk) — no internet required for speech transcription
- ✅ AI-powered responses using Google Gemini (requires internet and a valid API key)
- ✅ Natural speech output
- ✅ Automatic conversation flow
- ✅ Exit by saying "bye", "goodbye", "exit", or "quit"

---

## System Requirements

### Minimum Requirements:
- **OS**: Windows 10/11 (or Linux/Mac with minor adjustments)
- **Python**: 3.10 or higher (3.10/3.11 recommended for package compatibility)
- **RAM**: 8GB minimum (16GB recommended)
- **Webcam**: Built-in or external USB camera
- **Microphone**: Built-in or USB microphone
- **Speakers**: For hearing AI responses

### Hardware Recommendations:
- GPU (NVIDIA with CUDA) for faster YOLO processing
- Multi-core processor (Intel i5/i7 or AMD Ryzen 5+)

---

## Installation Guide

### Step 1: Download the Project

```bash
# Clone from GitHub 
git clone https://github.com/ochemoses/Human-Aware-AI-Assistance.git
cd Human-Aware-AI-Assistance
```

### Step 2: Create a Virtual Environment

A virtual environment keeps project packages separate from your system Python.

```bash
# Create virtual environment
python -m venv AI_Asistance_venv

# Activate it (Windows)
AI_Asistance_venv\Scripts\activate

# Activate it (Mac/Linux)
source AI_Asistance_venv/bin/activate
```

You should see `(AI_Asistance_venv)` in your terminal after activation.

### Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install all required packages
pip install ultralytics
pip install vosk pysoundfile
pip install pyaudio
pip install genai
pip install pyttsx3
pip install opencv-python
```

**Important Note for PyAudio on Windows:**
If you get errors installing PyAudio, use this instead:
```bash
pip install pipwin
pipwin install pyaudio
```

### Step 4: Download Vosk Model

The Vosk model is needed for speech recognition. The project folder includes a folder called `vosk-model-small-en-us-0.15`. If not present, download it:

1. Download from: https://alphacephei.com/vosk/models
2. Extract the `vosk-model-small-en-us-0.15` folder to your project directory

### Step 5: Verify Installation

```bash
# Test if all packages are installed correctly
python -c "import ultralytics, vosk, pyaudio, genai, pyttsx3, cv2; print('✓ All packages installed!')"
```

Note: The package name for Gemini SDK can appear as `google-generativeai` or `genai` depending on the pip package; `pip install genai` should work in this repo's environment.

### Step 6: Configure environment

1. Copy the example config to a local `.env` file:

- Windows PowerShell:
```powershell
Copy-Item -Path config.example.env -Destination .env
```

- macOS / Linux:
```bash
cp config.example.env .env
```

2. Edit `.env` and set your `GEMINI_API_KEY` and other settings (Vosk/YOLO paths, TTS rate/volume).

3. Optional but recommended: install `python-dotenv` to auto-load `.env` in development:
```bash
pip install python-dotenv
```

4. To load `.env` in scripts automatically, add near the top of `main.py` (after imports):
```py
from dotenv import load_dotenv
load_dotenv()
```

This project reads configuration from the environment (see `main.py`) so you can safely keep secrets out of source control.

---

## Project Structure

```
Human-Aware-AI-Assistance/
│
├── main.py                           #  MAIN FILE - Run this to start!
├── README.md                         # This file
│
├── LLM.py                           # AI response module
├── STT.py                           # Speech-to-text module
├── TTS.py                           # Text-to-speech module
├── Yolo.py                          # Person detection module
│
├── vosk-model-small-en-us-0.15/    # Speech recognition model
│   ├── am/
│   ├── conf/
│   ├── graph/
│   ├── ivector/
│   └── README
│
└── AI_Asistance_venv/              # Virtual environment (auto-created)

> Tip: Do NOT commit your virtual environment to git. Add `AI_Asistance_venv/` to `.gitignore` to keep the repo clean.
```

---

## How It Works

### System Architecture

```
┌─────────────────────────────────────────────────────┐
│  WEBCAM (Input)                                     │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  YOLO.PY (Person Detection)                         │
│  - Analyzes video frames                            │
│  - Detects if person is present                     │
└────────────────┬────────────────────────────────────┘
                 │
        [Person Detected?]
         │               │
        YES             NO
         │               └─→ [Wait/Loop]
         ▼
┌─────────────────────────────────────────────────────┐
│  STT.PY (Speech Recognition)                        │
│  - Listens to microphone                            │
│  - Converts voice to text                           │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  LLM.PY (AI Processing via Gemini)                  │
│  - Receives transcribed text                        │
│  - Generates AI response                            │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  TTS.PY (Text-to-Speech)                            │
│  - Converts response to audio                       │
│  - Plays through speakers                           │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  SPEAKERS (Output)                                  │
└─────────────────────────────────────────────────────┘
```

### File-by-File Explanation

| File | Purpose |
|------|---------|
| **main.py** | Orchestrates entire workflow - detects person → listens → processes → responds |
| **LLM.py** | Contains chatbot logic using Google Gemini (`google.generativeai` / `genai`) |
| **STT.py** | Handles speech-to-text using Vosk |
| **TTS.py** | Handles text-to-speech using pyttsx3 |
| **Yolo.py** | Demonstrates YOLO person detection |

---

## Running the Project

### Prerequisites Before Running:
1. **Gemini (Google Generative AI) API key**
   - Obtain an API key from Google Cloud (or your Google Cloud project that has access to Gemini APIs).
   - Set it as an environment variable instead of hardcoding it:
     - Windows (PowerShell): `setx GEMINI_API_KEY "your_key_here"`
     - Linux/macOS: `export GEMINI_API_KEY="your_key_here"`
   - Alternatively, you may pass the key into the script for quick testing, but **do not commit it to source control**.

2. **Virtual environment must be activated**
   ```bash
   AI_Asistance_venv\Scripts\activate  # Windows
   ```

3. **Vosk model downloaded**: Ensure `vosk-model-small-en-us-0.15` is present in the project directory (see Installation Guide).

### Start the Program

```bash
# Make sure you're in the project directory and venv is activated
python main.py
```

### What You'll See

```
=== Real-Time Conversation System ===
Starting YOLO detection, STT, LLM, and TTS pipeline...
Press 'q' in the video window to stop

Starting YOLO person detection...
```

### Using the Program

1. **Look at your webcam** - A video window will open showing the detection
2. **When detected**, the AI says: "Hello! I detected you. How can I help?"
3. **Speak your question** clearly
4. **Wait for transcription** - The system will show what it heard
5. **AI responds** - Speaking the answer out loud
6. **Continue conversing** - Ask more questions naturally
7. **Exit** - Say "bye", "goodbye", "exit", or "quit" OR press 'q' in video window

### Example Conversation

```
[Video opens, you appear in frame]

AI: "Hello! I detected you. How can I help?"

You: "What is Python?"

STT Output: "What is Python"

AI Response: "Python is a high-level programming language known for its simplicity 
and readability. It's widely used in web development, data science, artificial 
intelligence, and automation..."

[AI speaks response]

You: "Tell me about machine learning"

[Conversation continues...]

You: "Bye"

AI: "Goodbye!"
[Program stops]
```

---

## Troubleshooting

### Issue: "Import 'genai' (google.generativeai) could not be resolved"

**Solution:** Ensure the virtual environment is activated and install the Gemini SDK
```bash
AI_Asistance_venv\Scripts\activate
pip install genai
# or
pip install google-generativeai
```

If you still see import issues, check `python -m pip list` inside your venv and confirm the interpreter used by VS Code is the venv interpreter.

### Issue: "No module named 'pyaudio'"

**Solution on Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

**Solution on Mac:**
```bash
brew install portaudio
pip install pyaudio
```

**Solution on Linux:**
```bash
sudo apt-get install portaudio19-dev
pip install pyaudio
```

### Issue: Webcam not detected

**Solution:**
- Check if another application is using the webcam
- Grant camera permissions to Python/VS Code
- Try: `python -c "import cv2; cap = cv2.VideoCapture(0); print(cap.isOpened())"`

### Issue: Microphone not working

**Solution:**
- Check Windows Sound settings
- Set default recording device
- Run: `python -c "import pyaudio; p = pyaudio.PyAudio(); print(p.get_device_count())"`

### Issue: Gemini API / Network error

**Symptoms:** Errors like `400 INVALID_ARGUMENT`, `unexpected model name format`, authentication errors, or network timeouts.

**Solution:**
- Verify your `GEMINI_API_KEY` is set correctly (environment variable or the method you use to pass it into the script).
  - Windows (PowerShell): `setx GEMINI_API_KEY "your_key_here"`
  - macOS/Linux: `export GEMINI_API_KEY="your_key_here"`
- Check your network connectivity and any firewalls that may block API calls.
- Ensure you are using a supported model name (e.g., `gemini-2.5-flash`, **use hyphens not spaces**).
- Update the Gemini SDK: `pip install -U genai` or `pip install -U google-generativeai`.
- If you see `unexpected model name format`, confirm the `model=` string in `main.py` or `LLM.py` matches the exact model name expected by the API.

### Issue: YOLO model not downloading

**Solution:**
```bash
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

### Issue: "can't grab frame. Error: -2147483638" - Webcam Not Working

This error means OpenCV can't access your webcam. Try these solutions in order:

**Solution 1: Check if webcam is in use**
- Close Zoom, Teams, Discord, or any app using camera
- Restart your computer

**Solution 2: Check camera permissions**
- Windows 10/11: Settings → Privacy & Security → Camera
- Make sure "Camera access" is enabled
- Make sure Python is allowed to access camera

**Solution 3: Try different camera index**

Create a test file `test_camera.py`:
```python
import cv2

# Try different camera indices
for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Camera found at index {i}")
        ret, frame = cap.read()
        if ret:
            print(f"  ✓ Camera {i} works!")
            cv2.imshow(f"Camera {i}", frame)
            cv2.waitKey(1000)
            cv2.destroyAllWindows()
        cap.release()
```

Run it:
```bash
python test_camera.py
```

Note which camera index works, then edit `main.py` line ~130:
```python
cap = cv2.VideoCapture(0)  # Change 0 to working index (e.g., 1, 2, etc.)
```

**Solution 4: Update camera driver**
- Go to Device Manager (Windows)
- Find your camera under "Imaging devices"
- Right-click → Update driver
- Choose "Search automatically"

**Solution 5: Try with DirectShow backend**

Edit `main.py` around line 130, change:
```python
cap = cv2.VideoCapture(0)
```

To:
```python
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Use DirectShow backend
```

**Solution 6: Reinstall camera-related packages**
```bash
pip uninstall opencv-python -y
pip install opencv-python
```

**Solution 7: Run as Administrator**
- Right-click PowerShell
- Select "Run as administrator"
- Then run `python main.py`

---

## Future Enhancements

- [ ] Add wake word detection ("Hey AI" trigger)
- [ ] Support for multiple languages
- [ ] Emotion detection in voice
- [ ] Memory/context from previous conversations
- [ ] Custom AI model fine-tuning
- [ ] Face recognition for personalized responses
- [ ] Database to log conversations
- [ ] Web interface dashboard
- [ ] Multi-threaded response generation
- [ ] GPU acceleration support

---

## Configuration Tips

### Speed Up / Tune Person Detection ⚡
- The detection happens inside `detect_person()` which calls the YOLO model like:
```py
results = self.yolo_model.predict(
    source=frame,
    conf=0.5,       # confidence threshold: increase for fewer false positives
    verbose=False,
    stream=False
)
```
- To change speed/accuracy:
  - Increase `conf` (e.g. `conf=0.6`) to reduce false positives (may be faster on CPU)
  - Reduce frequency of detection by adding a small sleep in `wait_for_person()` (e.g. `time.sleep(0.2)`) or implement a frame counter to run detection every N frames to reduce CPU/GPU load.

Example (run every 3rd frame):
```py
frame_counter = getattr(self, '_frame_counter', 0) + 1
self._frame_counter = frame_counter
if frame_counter % 3 != 0:
    return False
# otherwise run detection
```

### Adjust TTS Speed 🔊
- The project stores TTS settings in the class as `self.tts_rate` and `self.tts_volume`.
- Change the default in the `__init__()` of `main.py` / `chatbot.py`:
```py
# In __init__
self.tts_rate = 150   # Lower = slower, Higher = faster
self.tts_volume = 1.0
```
- Or pass these as constructor arguments (you can add params to the class if you prefer dynamic configuration).

### Change AI Model / Model Name Format 🤖
- The code uses Google Gemini via `genai` and sets the model name in `get_ai_response()` like:
```py
model_name = "gemini-2.5-flash"
response = self.gemini_client.models.generate_content(
    model=model_name,
    contents=prompt
)
```
- Important: **use the hyphenated model name** (e.g. `gemini-2.5-flash`), not `gemini-2.5 flash` — the API rejects unexpected formats.
- To try another Gemini model, change `model_name` accordingly to a supported model string from the Gemini docs.

---

## Contributing

Found a bug? Have an improvement? 
- Create an issue on GitHub
- Submit a pull request with your changes
- Document your changes clearly

---

## 📄 License

This project is open source. Feel free to modify and use for learning purposes.

---

## FAQ

**Q: Do I need internet for this to work?**
A: Partially. Speech recognition (Vosk) and YOLO person detection can run fully offline. However, Google Gemini (LLM) requires internet access and a valid API key to generate responses.

**Q: Can I use this on Mac/Linux?**
A: Yes! Most code is cross-platform. PyAudio installation might differ (see troubleshooting). On Linux/macOS, use native audio packages (portaudio) and install PyAudio accordingly.

**Q: How accurate is the speech recognition?**
A: Vosk is ~80-90% accurate for clear English when audio is clean. Speak clearly and minimize background noise for best results.

**Q: Can I change the AI personality?**
A: Yes! You can modify the system prompt used in `main.py` / `LLM.py` (the `system_instruction` string) to change the assistant's tone and behavior.

**Q: Why is it slow the first time?**
A: Initial startup can be slow because models (YOLO, Vosk) are loading into memory and the first Gemini API call may take longer due to network latency. Subsequent runs and cached models are typically faster.

---

## 📞 Support

For issues, questions, or suggestions:
- Check this README troubleshooting section
- Search closed GitHub issues
- Create a new GitHub issue with detailed description

---

**Made with ❤️ for AI Enthusiasts**

#   H u m a n - A w a r e - A I - A s s i s t a n c e 
 
 #   H u m a n - A w a r e - A I - A s s i s t a n c e 
 
 
