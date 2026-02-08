import vosk
import pyaudio
import json
import pyttsx3
from google import genai
import sys
import os
import time
from ultralytics import YOLO
import cv2
import threading

class VoiceChatbotWithPersonDetection:
    def __init__(self, gemini_api_key, vosk_model_path="vosk-model-small-en-us-0.15", yolo_model_path="yolov8n.pt"):
        """Initialize the chatbot with all necessary components including YOLO"""
        
        # Initialize YOLO for person detection
        print("🤖 Loading YOLO model...")
        self.yolo_model = YOLO("yolov8n.pt")
        self.person_detected = False
        self.camera = None
        self.detection_active = False
        print("✓ YOLO model loaded")
        
        # Initialize Gemini AI
        print("🧠 Initializing Gemini AI...")
        self.gemini_client = genai.Client(api_key=gemini_api_key)
        print("✓ Gemini AI initialized")
        
        # Initialize Vosk STT
        print("🎤 Loading speech recognition model...")
        self.vosk_model = vosk.Model(vosk_model_path)
        self.recognizer = vosk.KaldiRecognizer(self.vosk_model, 16000)
        print("✓ Speech recognition loaded")
        
        # Initialize PyAudio for microphone
        self.mic = pyaudio.PyAudio()
        self.stream = self.mic.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=8192
        )
        self.stream.start_stream()
        
        # Store TTS settings (don't keep engine running)
        self.tts_rate = 160
        self.tts_volume = 1.0
        self.tts_voice_id = None
        
        # Get voice ID once at startup
        try:
            temp_engine = pyttsx3.init()
            voices = temp_engine.getProperty('voices')
            if voices:
                self.tts_voice_id = voices[0].id
                print(f"✓ Using voice: {voices[0].name}")
            del temp_engine
        except Exception as e:
            print(f"⚠️ Warning initializing TTS: {e}")
        
        # Conversation history for context
        self.conversation_history = []
        
    def initialize_camera(self):
        """Initialize the camera for person detection"""
        if self.camera is None:
            print("📷 Initializing camera...")
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                print("❌ Failed to open camera")
                return False
            print("✓ Camera initialized")
        return True
    
    def release_camera(self):
        """Release the camera when not needed"""
        if self.camera is not None:
            self.camera.release()
            cv2.destroyAllWindows()
            self.camera = None
            print("📷 Camera released")
    
    def detect_person(self, show_video=False):
        """
        Detect if a person is in front of the camera
        Returns: True if person detected, False otherwise
        """
        if not self.initialize_camera():
            return False
        
        ret, frame = self.camera.read()
        if not ret:
            print("❌ Failed to read from camera")
            return False
        
        # Run YOLO detection
        results = self.yolo_model.predict(
            source=frame,
            conf=0.5,  # Confidence threshold
            verbose=False,  # Don't print detection info
            stream=False
        )
        
        person_found = False
        
        # Check if any detected object is a person (class 0 in COCO dataset)
        for result in results:
            if result.boxes is not None:
                for cls in result.boxes.cls:
                    class_id = int(cls)
                    class_name = self.yolo_model.names[class_id]
                    
                    if class_name.lower() == 'person':
                        person_found = True
                        
                        # Draw bounding box if showing video
                        if show_video:
                            boxes = result.boxes.xyxy.cpu().numpy()
                            for box in boxes:
                                x1, y1, x2, y2 = map(int, box)
                                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                                cv2.putText(frame, 'Person Detected', (x1, y1-10), 
                                          cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
        # Show video feed if requested
        if show_video:
            status_text = "Person Detected ✓" if person_found else "No Person Detected"
            cv2.putText(frame, status_text, (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) if person_found else (0, 0, 255), 2)
            cv2.imshow('Person Detection', frame)
            cv2.waitKey(1)
        
        return person_found
    
    def wait_for_person(self):
        """
        Wait until a person is detected in front of the camera
        Shows live video feed while waiting
        """
        print("\n" + "=" * 60)
        print("👁️  WAITING FOR PERSON...")
        print("=" * 60)
        print("Please stand in front of the camera")
        print("Press 'q' to skip person detection")
        print("=" * 60)
        
        self.detection_active = True
        
        while self.detection_active:
            person_detected = self.detect_person(show_video=True)
            
            if person_detected:
                print("\n✓ Person detected!")
                self.person_detected = True
                
                # Give feedback beep/message
                self.speak("I can see you now. How can I help you?")
                
                # Wait a bit before closing detection
                time.sleep(1)
                self.release_camera()
                return True
            
            # Check for 'q' key press to skip
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("\n⚠️ Person detection skipped by user")
                self.release_camera()
                return False
            
            # Small delay between checks
            time.sleep(0.1)
        
        return False
    
    def check_person_presence(self):
        """
        Quick check if person is still present (no video display)
        Used during conversation to verify person is still there
        """
        return self.detect_person(show_video=False)
    
    def clean_text_for_speech(self, text):
        """
        Clean text for speech by removing markdown and unwanted characters.
        """
        import re
        
        # Remove markdown bold/italic (** and *)
        text = re.sub(r'\*+', '', text)
        
        # Remove markdown underscores (_ and __)
        text = re.sub(r'_+', '', text)
        
        # Remove hashtags (used for headers in markdown)
        text = re.sub(r'#+\s*', '', text)
        
        # Remove backticks (used for code)
        text = re.sub(r'`+', '', text)
        
        # Remove markdown links but keep the text [text](url) -> text
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def listen(self):
        """Listen to microphone and return transcribed text"""
        print("\n🎤 Listening...")
        
        while True:
            data = self.stream.read(4096, exception_on_overflow=False)
            if self.recognizer.AcceptWaveform(data):
                result = json.loads(self.recognizer.Result())
                text = result['text'].strip()
                
                if text:
                    print(f"✓ You said: {text}")
                    return text
    
    def get_ai_response(self, user_input):
        """Send text to Gemini and get response"""
        print("🤔 Thinking...")
        
        try:
            # Add user input to conversation history
            self.conversation_history.append(f"User: {user_input}")
            
            # Create context from recent conversation (last 10 exchanges)
            context = "\n".join(self.conversation_history[-10:])
            
            # Add system instruction for concise voice responses
            system_instruction = """You are a voice assistant. Keep your responses:
- Concise and brief (2-3 sentences maximum)
- Conversational and natural for spoken dialogue
- Clear and direct without unnecessary details
- Avoid using markdown formatting (no *, _, #, etc.)
- Summarize information rather than giving long explanations
"""
            
            prompt = f"""{system_instruction}

Previous conversation:
{context}

User: {user_input}
Assistant (respond briefly and conversationally):"""
            
            # Use the correct model name format (hyphenated)
            model_name = "gemini-2.5-flash"
            try:
                print(f"🧾 Sending request to Gemini model: {model_name}")
                response = self.gemini_client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
            except Exception as e:
                # If the API complains about model name format, try to normalize and retry
                err_str = str(e)
                print(f"⚠️ Gemini request failed: {err_str}")
                if 'unexpected model name format' in err_str.lower() or 'invalid_argument' in err_str.lower():
                    alt_model = model_name.replace(' ', '-').replace('__', '-').strip()
                    print(f"🔁 Retrying with normalized model name: {alt_model}")
                    try:
                        response = self.gemini_client.models.generate_content(
                            model=alt_model,
                            contents=prompt
                        )
                    except Exception as e2:
                        print(f"❌ Retry also failed: {e2}")
                        raise
                else:
                    raise

            ai_response = getattr(response, 'text', '') or ''
            
            # Add AI response to conversation history
            self.conversation_history.append(f"Assistant: {ai_response}")
            
            print(f"💬 AI: {ai_response}")
            return ai_response
            
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            print(f"❌ Error: {error_msg}")
            return error_msg
    
    def speak(self, text):
        """
        Convert text to speech and play it.
        Creates a FRESH TTS engine for each call to avoid the silent bug.
        """
        # Clean the text first
        cleaned_text = self.clean_text_for_speech(text)
        
        print("🔊 Speaking...")
        print(f"   📝 Original length: {len(text)} characters")
        print(f"   ✨ Cleaned length: {len(cleaned_text)} characters")
        
        try:
            # Create a FRESH engine for this specific speech
            engine = pyttsx3.init()
            
            # Set properties
            engine.setProperty('rate', self.tts_rate)
            engine.setProperty('volume', self.tts_volume)
            
            if self.tts_voice_id:
                engine.setProperty('voice', self.tts_voice_id)
            
            # Clear any pending speech
            engine.stop()
            
            # Add the CLEANED text to speak
            engine.say(cleaned_text)
            
            # THIS IS CRITICAL - runAndWait MUST complete
            engine.runAndWait()
            
            # Force cleanup
            del engine
            
            # Small delay to ensure audio completes
            time.sleep(0.1)
            
            print("✓ Finished speaking")
            return True
            
        except Exception as e:
            print(f"❌ Error in speak: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def conversation_loop(self):
        """Main conversation loop after person is detected"""
        try:
            interaction_count = 0
            
            while True:
                # Step 1: Listen to user
                user_input = self.listen()
                
                # Check for exit commands
                if user_input.lower() in ['exit', 'quit', 'stop', 'goodbye', 'bye']:
                    farewell = "Goodbye! Have a great day!"
                    print(f"\n💬 AI: {farewell}")
                    self.speak(farewell)
                    break
                
                # Skip empty inputs
                if not user_input:
                    continue
                
                # Step 2: Get AI response
                ai_response = self.get_ai_response(user_input)
                
                # Step 3: Speak the response
                self.speak(ai_response)
                
                interaction_count += 1
                
                # Every 5 interactions, check if person is still there
                if interaction_count % 5 == 0:
                    print("\n🔍 Checking if you're still there...")
                    if not self.check_person_presence():
                        print("⚠️ Person no longer detected. Pausing conversation...")
                        self.speak("I can't see you anymore. I'll wait for you to return.")
                        self.release_camera()
                        
                        # Wait for person to return
                        if not self.wait_for_person():
                            break
                
                print("-" * 60)
                
        except KeyboardInterrupt:
            print("\n\n⚠️ Chatbot stopped by user")
    
    def run(self):
        """Main loop to run the chatbot with person detection"""
        print("=" * 60)
        print("🤖 VOICE CHATBOT WITH PERSON DETECTION")
        print("=" * 60)
        
        # Initial greeting (before checking for person)
        greeting = "Hello! I'm your voice assistant. How can I help you today?"
        print(f"\n💬 AI: {greeting}")
        self.speak(greeting)
        
        # Wait for person to be detected
        person_present = self.wait_for_person()
        
        if person_present:
            # Person detected, start conversation
            print("\n" + "=" * 60)
            print("🎙️  CONVERSATION MODE ACTIVATED")
            print("=" * 60)
            print("Say 'exit', 'quit', or 'stop' to end the conversation")
            print("=" * 60)
            
            # Run the main conversation loop
            self.conversation_loop()
        else:
            print("\n⚠️ No person detected. Exiting...")
            self.speak("No person detected. Goodbye!")
        
        # Cleanup
        self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        print("\n🧹 Cleaning up resources...")
        
        self.detection_active = False
        
        if hasattr(self, 'stream') and self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if hasattr(self, 'mic') and self.mic:
            self.mic.terminate()
        
        self.release_camera()
        
        print("✓ Cleanup complete. Goodbye!")


def main():
    # Configuration (read from environment with sensible defaults)
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
    VOSK_MODEL_PATH = os.getenv("VOSK_MODEL_PATH", "vosk-model-small-en-us-0.15")
    YOLO_MODEL_PATH = os.getenv("YOLO_MODEL_PATH", "yolov8n.pt")
    TTS_RATE = int(os.getenv("TTS_RATE", "160"))
    TTS_VOLUME = float(os.getenv("TTS_VOLUME", "1.0"))

    if not GEMINI_API_KEY:
        print("⚠️ WARNING: GEMINI_API_KEY not set. Set GEMINI_API_KEY env var or create a .env from config.example.env")
    else:
        print("✓ Gemini API key loaded from environment")

    print("\n📋 Starting Voice Chatbot with Person Detection...")
    print(f"📁 Vosk Model: {VOSK_MODEL_PATH}")
    print(f"📁 YOLO Model: {YOLO_MODEL_PATH}")
    print(f"🤖 AI Model: Gemini (model: gemini-2.5-flash)\n")

    # Create and run the chatbot
    chatbot = VoiceChatbotWithPersonDetection(
        gemini_api_key=GEMINI_API_KEY,
        vosk_model_path=VOSK_MODEL_PATH,
        yolo_model_path=YOLO_MODEL_PATH
    )

    # Apply TTS configuration from environment
    try:
        chatbot.tts_rate = TTS_RATE
        chatbot.tts_volume = TTS_VOLUME
    except Exception:
        pass

    chatbot.run()


if __name__ == "__main__":
    main()