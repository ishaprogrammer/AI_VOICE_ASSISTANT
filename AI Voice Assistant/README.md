--------------------------------------------------------------------------------------------------------------------
if any problem in gemini_api then reset it from:
https://aistudio.google.com/app/u/1/apikey?_gl=1*qja8r1*_ga*MTY0ODk5NzkzLjE3MzM0OTY4ODI.*_ga_P1DBVKWT6V*MTczMzU1MjgwNy4yLjEuMTczMzU1MzAzNS4xOC4wLjExOTY1OTgwOA.

if any problem in whether_api then reset it from:
TRIAL Ends on 20/Dec/2024
https://www.weatherapi.com/

if any problem in groq_api then reset it from:
https://console.groq.com/keys
reset every 24hr

--------------------------------------------------------------------------------------------------------------------
what does AI Voice Assistant does overall:

1. Provides real-time weather updates based on user requests.  
2. Assists with clipboard management for quick access to copied data.  
3. Analyzes webcam images and describes detected activities or objects.  
4. Opens applications on voice command for seamless multitasking.  
5. Captures screen snapshots and narrates the current screen activity.  
6. Determines and shares the user's current geographic location.  
7. Saves conversation history for context-aware interactions.  
8. Stops responding or reactivates based on user-defined voice commands. 

--------------------------------------------------------------------------------------------------------------------
Get response from Groq LLaMA model:
model="llama-3.2-90b-vision-preview"
The groq API KEY must be reset every 24hr

take_snapshot_and_describe:
model = genai.GenerativeModel("gemini-1.5-flash")

clipboard_assistance:
get_groq_response 
model="llama-3.2-90b-vision-preview"

get_current_location:
API_website = https://ipinfo.io

get_weather:
API_website = http://api.weatherapi.com/v1/current.json

capture_and_describe:
model = genai.GenerativeModel('gemini-1.5-flash-latest')

--------------------------------------------------------------------------------------------------------------------

