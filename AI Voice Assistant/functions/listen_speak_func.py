import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv
import threading
import queue

# Load environment variables
load_dotenv()

# Initialize components
recognizer = sr.Recognizer()
speaker = pyttsx3.init()
stop_speaking = threading.Event()
audio_queue = queue.Queue()

# Configure voice settings
voices = speaker.getProperty('voices')
speaker.setProperty('voice', voices[1].id)  # Index 1 for female voice
speaker.setProperty('rate', 150)  # Speed of speech

WAKE_WORD = "assistant"  # Define the wake word

def speak(text):
    """Convert text to speech, with interrupt handling."""
    print(f"{WAKE_WORD}: {text}")
    stop_speaking.clear()
    speaker.say(text)
    try:
        speaker.runAndWait()
    except RuntimeError:
        # Handle interruption gracefully
        print("Speaking was interrupted.")

def background_listener():
    """Listen for the 'stop speaking' command in the background."""
    with sr.Microphone() as source:
        while True:
            try:
                audio = recognizer.listen(source, timeout=1, phrase_time_limit=2)
                text = recognizer.recognize_google(audio)
                if "stop speaking" in text.lower():
                    stop_speaking.set()
                    speaker.stop()
                    print("Stopped speaking.")
            except (sr.WaitTimeoutError, sr.UnknownValueError):
                pass
            except sr.RequestError:
                print("Error with speech recognition service")

def listen():
    """Listen for user input through the microphone with enhanced settings."""
    with sr.Microphone() as source:
        print("Listening...")
        
        # Dynamically adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source, duration=0.5)  
        
        # Lower the energy threshold to make it more sensitive
        recognizer.energy_threshold = 100  
        
        # Adjust pause threshold for smoother recognition of normal speech
        recognizer.pause_threshold = 0.8  
        
        try:
            # Listen with a longer timeout to ensure smooth input
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            # Recognize speech using Google Speech Recognition
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        
        except sr.UnknownValueError:
            # Return None if speech was not understood
            print("Sorry, I couldn't understand that.")
            return None
        
        except sr.RequestError as e:
            # Handle API errors
            print(f"Speech recognition service error: {e}")
            return None
        
        except sr.WaitTimeoutError:
            # Handle cases where no speech is detected within the timeout period
            print("No speech detected within the timeout period.")
            return None