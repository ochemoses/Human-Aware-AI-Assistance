import pyttsx3

# Initialize TTS engine
engine = pyttsx3.init()

# Optional: Adjust settings
engine.setProperty('rate', 160)     # Speed (default ~200)
engine.setProperty('volume', 1.0)   # Volume (0.0 to 1.0)

# Get available voices
voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[0].id)  # Male voice (usually)
engine.setProperty('voice', voices[0].id)  # Female voice (usually)

# Speak text
text = "Hello! This is offline text to speech working perfectly.  Arduino is an open-source electronics platform that serves as the brain of electronic projects by reading inputs from sensors and controlling outputs like LEDs. The Arduino Uno board contains key parts such as the microcontroller (ATmega328P) for processing programs, a USB port for uploading code, a power jack for external power, digital pins for on/off signals, and analog pins for reading varying signals.The Arduino IDE is the software used to write and upload programs. It contains two main functions: setup(), which runs once for initialization, and loop(), which runs continuously to control the project.Proteus is a simulation software that allows Arduino circuits to be tested virtually without physical components. To simulate an Arduino project in Proteus, the program’s .hex file must be exported from the Arduino IDE and loaded into the Arduino component."
engine.say(text)
engine.runAndWait()

# Or save to file
# engine.save_to_file(text, 'output.mp3')
# engine.runAndWait()