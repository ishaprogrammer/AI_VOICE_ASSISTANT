import os
from dotenv import load_dotenv
import requests
import pyperclip
from PIL import ImageGrab
import pytesseract
import google.generativeai as genai
import cv2
import subprocess
from PIL import Image
from datetime import datetime
from main import get_groq_response
from functions.listen_speak_func import speak


# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
gemini_api_key = os.getenv('GEMINI_API_KEY')
whether_api_key = os.getenv('WEATHER_API_KEY')

def open_application(app_name):
    """Open a specified application based on the user's voice command."""
    app_name = app_name.lower()

    try:
        if "youtube" in app_name:
            # Open YouTube in the default browser
            subprocess.run(["start", "https://www.youtube.com"], check=True, shell=True)
            speak("Opening YouTube now.")
        
        elif "chrome" in app_name:
            # Open Google Chrome (if installed)
            subprocess.run(["start", "chrome"], check=True, shell=True)
            speak("Opening Google Chrome.")
        
        # elif "firefox" in app_name:
        #     # Open Firefox (if installed)
        #     subprocess.run(["start", "firefox"], check=True, shell=True)
        #     speak("Opening Firefox.")
        
        elif "notepad" in app_name:
            # Open Notepad
            subprocess.run(["start", "notepad"], check=True, shell=True)
            speak("Opening Notepad.")
        
        # Add more applications as needed
        else:
            speak(f"Sorry, I don't know how to open {app_name}.")
    
    except Exception as e:
        speak(f"Sorry, I couldn't open {app_name}. Error: {e}")

def take_snapshot_and_describe():
    """Take a screenshot, save it, and describe it using the Gemini model."""

    # Step 1: Capture the screen
    try:
        speak("Taking Snapshot Now")
        screenshot = ImageGrab.grab()  # Capture the screen
        screenshot.save("screenshot.png")  # Save the screenshot as PNG
    except Exception as e:
        return f"Error capturing screenshot: {e}"
    
    # Step 2: Extract text using OCR
    try:
        extracted_text = pytesseract.image_to_string("screenshot.png").strip()
        if not extracted_text:
            return "No text found in the screenshot."
    except Exception as e:
        return f"Error extracting text with OCR: {e}"

    # Step 3: Generate description with Gemini
    try:
        genai.configure(api_key=gemini_api_key)  # Ensure API key is valid
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"Describe this content extracted from the image: {extracted_text}")
        return response.text if response.text else "Unable to generate a description."
    except Exception as e:
        return f"Error generating description with Gemini: {e}"
    
def clipboard_assistance():
    """Provide assistance based on the text currently in the clipboard."""
    try:
        # Get the text from the clipboard
        clipboard_text = pyperclip.paste()
        
        if clipboard_text:
            speak(f" Assisting you with Clipboard")
            
            # You can add custom logic to process the clipboard text, 
            # for example, you can send it to your AI model to analyze and respond.
            response = get_groq_response(clipboard_text)  # Using your existing AI response function
            speak(response)
        else:
            speak("There is no text in the clipboard.")
    
    except Exception as e:
        print(f"Error accessing clipboard: {e}")
        speak("Sorry, I encountered an error while accessing the clipboard.")
          
def get_current_location():
    """Get the current location using IP-based geolocation."""
    try:
        response = requests.get('https://ipinfo.io')
        data = response.json()
        location = data['city'] + ", " + data['region']  # Default location
        if location == "Bengaluru, Karnataka":
            location = "Belgaum, Karnataka"  # Adjust for your specific case
        return location
    except Exception as e:
        print(f"Error detecting location: {e}")
        return None

            
def get_weather(location):
    """Fetch weather information for a given location."""
    API_KEY = whether_api_key  # Ensure the API key is stored in your .env file
    BASE_URL = "http://api.weatherapi.com/v1/current.json"  # Correct WeatherAPI endpoint
    
    # Clean up location input (capitalize for better readability)
    location = location.strip().title()
    
    try:
        # Query the weather API
        response = requests.get(BASE_URL, params={"key": API_KEY, "q": location})
        data = response.json()
        
        # Debugging: Print the API response
        # print(f"Assistent: {data}")
        
        if "current" in data:  # Check if the "current" key exists in the response
            weather_desc = data["current"]["condition"]["text"]
            temperature = data["current"]["temp_c"]
            return f"The current weather in {location} is {weather_desc} with a temperature of {temperature}°C."
        elif "error" in data:  # Handle errors from WeatherAPI
            error_message = data["error"]["message"]
            return f"Sorry, I couldn't fetch the weather for {location}. Error: {error_message}."
        else:
            return f"Sorry, I couldn't fetch the weather for {location}. Please try again."
    
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return "Sorry, there was an error while retrieving the weather information."

def capture_and_describe():
    # Initialize Gemini
    GOOGLE_API_KEY = gemini_api_key
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    speak("Capturing your WebCam")
    
    # Capture image from webcam
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
   
    if ret:
        # Save image
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"webcam_capture_{timestamp}.jpg"
        cv2.imwrite(filename, frame)
       
        # Convert BGR to RGB for Gemini
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_frame)
       
        # Create vision prompt
        prompt = (
            'You are the vision analysis AI that provides semantic meaning from images to provide context '
            'to send to another AI that will create a response to the user. Do not respond as the AI assistant '
            'to the user. Instead, take the user prompt input and try to extract all meaning from the photo '
            'relevant to the user prompt. Then generate as much objective data about the image for the AI '
            'assistant who will respond to the user. \nUSER PROMPT: Analyze this webcam capture'
        )
       
        # Get description from Gemini
        response = model.generate_content([prompt, pil_image])
        description = response.text
       
        cap.release()
        return f"Image captured .\n Description: {description}"
    else:
        cap.release()
        return "Failed to capture image"