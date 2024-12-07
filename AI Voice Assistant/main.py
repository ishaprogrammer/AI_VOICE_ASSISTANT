import speech_recognition as sr
import pyttsx3
from groq import Groq
import os
from dotenv import load_dotenv
import threading
import queue
from functions.tasks_functions import *
from functions.listen_speak_func import *
from functions.assistant_func import *

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
groq_client = Groq(api_key=GROQ_API_KEY)

# Initialize components
recognizer = sr.Recognizer()
speaker = pyttsx3.init()
stop_speaking = threading.Event()
audio_queue = queue.Queue()

# Configure voice settings
voices = speaker.getProperty('voices')
speaker.setProperty('voice', voices[1].id)  # Index 1 for female voice
speaker.setProperty('rate', 150)  # Speed of speech

def get_groq_response(prompt):
    """Get response from Groq LLaMA model."""
    try:
        completion = groq_client.chat.completions.create(
            model="llama-3.2-90b-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stream=False
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error getting response from Groq: {e}")
    return "Sorry, I encountered an error while processing your request."

def handle_command():
    """Handle commands after the wake word is detected."""
    assistant_name = get_assistant_name() 
    speak("I'm here. How can I assist you?")
    
    while True:
        user_input = listen()
        if user_input:
            assistant_response = ""  # Initialize response

            if "exit" in user_input.lower() or "goodbye" in user_input.lower():
                assistant_response = "Goodbye! Have a great day!"
                speak(assistant_response)
                stop_speaking.set()
                speaker.stop()
                save_conversation_history(user_input, assistant_response)
                break
            elif "stop speaking" in user_input.lower():
                assistant_response = "Stopped speaking."
                speak(assistant_response)
                stop_speaking.set()
                speaker.stop()
                save_conversation_history(user_input, assistant_response)
                continue
                
            elif "weather" in user_input.lower():
                # Extract location from the user input
                location = user_input.lower().replace("how is the weather in", "").replace("what's the weather in", "").strip()
                # Fetch and respond with weather information
                if location:
                    weather_info = get_weather(location)
                    assistant_response = weather_info
                    speak(weather_info)
                else:
                    assistant_response = "Please specify a location for the weather."
                    speak(assistant_response)
            
            elif "current location" in user_input.lower():
                location = get_current_location()
                if location:
                    assistant_response = f"Your current location is {location}."
                else:
                    assistant_response = "Sorry, I couldn't detect your current location."
                speak(assistant_response)
            
            elif "clipboard" in user_input.lower() or "assist with clipboard" in user_input.lower():
                clipboard_assistance()  # Call the clipboard assistance function
                assistant_response = "I helped you with the clipboard."  # Dummy response for saving
            
            elif "take a snapshot" in user_input.lower():
                snapshot_text = take_snapshot_and_describe()
                assistant_response = f"I detected the following text: {snapshot_text}"
                speak(assistant_response)
            
            elif "capture my webcam" in user_input.lower():
                snapshot_text = capture_and_describe()
                assistant_response = snapshot_text
                speak(assistant_response)

            
            elif "open" in user_input.lower():  # Add this block to open apps
                app_name = user_input.lower().replace("open", "").strip()
                open_application(app_name)
                assistant_response = f"Opening {app_name}."
            
            elif "what's your name" in user_input.lower():
                assistant_response = f"My name is {assistant_name}."
                speak(assistant_response)
            
            elif "clear conversation" in user_input.lower():
                clear_conversation_history()
                assistant_response = "The conversation history has been cleared."
                speak(assistant_response)
                continue
            
            else:
                # Get response from Groq
                response = get_groq_response(user_input)
                assistant_response = response
                speak(response)

            # Save conversation history after each response
            save_conversation_history(user_input, assistant_response)

    print("Listening..")

def main():
    # Start background listener thread
    listener_thread = threading.Thread(target=background_listener, daemon=True)
    listener_thread.start()
    speak("Hello! Say 'Assistant' to wake me up.")

    while True:
        # Passive listening for wake word
        user_input = listen()
        if user_input and WAKE_WORD in user_input.lower():
            handle_command()

if __name__ == "__main__":
    main()
    