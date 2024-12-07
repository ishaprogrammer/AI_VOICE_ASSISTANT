import os
from functions.listen_speak_func import speak, listen


def save_conversation_history(user_input, assistant_response):
    """Save the conversation history to a file."""
    # Define the file path for the conversation history
    history_file = "conversation_history.txt"

    # Ensure the file exists, if not create it
    if not os.path.exists(history_file):
        with open(history_file, "w") as file:
            file.write("Conversation History:\n\n")

    # Append the user input and assistant's response to the file
    with open(history_file, "a") as file:
        file.write(f"User: {user_input}\n")
        file.write(f"Assistant: {assistant_response}\n\n")

def clear_conversation_history():
    """Clear the conversation history file."""
    history_file = "conversation_history.txt"
    if os.path.exists(history_file):
        with open(history_file, "w") as file:
            file.write("Conversation History:\n\n")

def get_assistant_name():
    """Get the assistant's name either from a file or ask the user for it."""
    # Check if the name is already saved in a file
    if os.path.exists("assistant_name.txt"):
        with open("assistant_name.txt", "r") as file:
            assistant_name = file.read().strip()
    else:
        # If not, ask the user for the assistant's name
        speak("What should I call you?")
        assistant_name = listen()
        if assistant_name:
            with open("assistant_name.txt", "w") as file:
                file.write(assistant_name)
        else:
            assistant_name = "Assistant"  # Default name if nothing is provided
            with open("assistant_name.txt", "w") as file:
                file.write(assistant_name)
    
    return assistant_name