# ==============================
# HUMAN-AWARE AI ASSISTANT CORE
# ==============================

# --------- Imports ----------
import json
import vosk
import pyaudio
import pyttsx3
from google import genai


# --------- CONFIG ----------
GEMINI_API_KEY = "AIzaSyAwckPwImB4dw0yma3AI2IhG_rtZBS6R-4"
GEMINI_MODEL = "gemini-2.5-flash"
VOSK_MODEL_PATH = "vosk-model-small-en-us-0.15"
SAMPLE_RATE = 16000


# ==============================
# AI BRAIN (GEMINI)
# ==============================
def init_gemini():
    client = genai.Client(api_key=GEMINI_API_KEY)
    return client


def ask_gemini(client, text):
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=text
    )
    return response.text


# ==============================
# TEXT TO SPEECH (TTS)
# ==============================
def init_tts():
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)
    engine.setProperty('volume', 1.0)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # change index if needed
    return engine


def speak(engine, text):
    print("AI:", text)
    engine.say(text)
    engine.runAndWait()


# ==============================
# SPEECH TO TEXT (STT)
# ==============================
def init_stt():
    model = vosk.Model("vosk-model-small-en-us-0.15")
    recognizer = vosk.KaldiRecognizer(model, SAMPLE_RATE)

    mic = pyaudio.PyAudio()
    stream = mic.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=8192
    )
    stream.start_stream()
    return recognizer, stream, mic


def listen(recognizer, stream):
    while True:
        data = stream.read(4096, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get("text", "")
            if text.strip() != "":
                return text


# ==============================
# MAIN AI LOOP
# ==============================
def main():
    print("Initializing systems...")

    # Init systems
    gemini_client = init_gemini()
    tts_engine = init_tts()
    recognizer, stream, mic = init_stt()

    print("Human-Aware AI Assistant is running...")
    speak(tts_engine, "Human aware AI assistant activated")

    try:
        while True:
            print("\nListening...")
            user_text = listen(recognizer, stream)
            print("User:", user_text)

            # Termination word
            if user_text.lower() in ["exit", "stop", "sleep", "shutdown"]:
                speak(tts_engine, "Going to idle mode. Goodbye.")
                break

            # AI reasoning
            ai_reply = ask_gemini(gemini_client, user_text)

            # Speak response
            speak(tts_engine, ai_reply)

    except KeyboardInterrupt:
        print("Shutting down assistant...")

    finally:
        stream.stop_stream()
        stream.close()
        mic.terminate()


# ==============================
# START SYSTEM
# ==============================
if __name__ == "__main__":
    main()
