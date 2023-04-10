import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import time

# Initialize the speech recognizer and text-to-speech engine
r = sr.Recognizer()
engine = pyttsx3.init()

# Define a function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Define a function to listen for commands and perform tasks
def listen():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)  # Adjust microphone for ambient noise
        print("Listening...")
        audio = r.listen(source)

        # Use Google's speech recognition service to convert audio to text
        try:
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that.")
            return ""
        except sr.RequestError:
            speak("Sorry, I'm having trouble connecting to the internet.")
            return ""

# Define a function to set a reminder
def set_reminder():
    speak("What would you like me to remind you about?")
    reminder_text = listen()
    if reminder_text:
        speak("When would you like to be reminded?")
        reminder_time = listen()
        if reminder_time:
            try:
                reminder_time_obj = datetime.datetime.strptime(reminder_time, '%I:%M %p')
                now = datetime.datetime.now()
                time_diff = (reminder_time_obj - now).total_seconds()
                if time_diff > 0:
                    speak(f"I will remind you to {reminder_text} in {time_diff/60} minutes.")
                    time.sleep(time_diff)
                    speak(f"Reminder: {reminder_text}")
                else:
                    speak("Sorry, that time has already passed.")
            except ValueError:
                speak("Sorry, I didn't understand the time.")

# Define a function to create a to-do list
def create_todo_list():
    speak("What tasks would you like to add to your to-do list?")
    tasks = []
    task = listen()
    while task:
        tasks.append(task)
        speak(f"Added {task} to your to-do list. What else?")
        task = listen()
    if tasks:
        speak("Your to-do list for today:")
        for i, task in enumerate(tasks):
            speak(f"{i+1}. {task}")

# Define a function to search the web
def search_web():
    speak("What would you like to search for?")
    query = listen()
    if query:
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        speak(f"Here are the search results for {query}.")

# Define the main function to run the voice assistant
def main():
    speak("Hi, how can I help you?")
    while True:
        command = listen()
        if "reminder" in command:
            set_reminder()
        elif "to-do list" in command:
            create_todo_list()
        elif "search" in command or "web" in command:
            search_web()
        elif "stop" in command or "quit" in command or "exit" in command:
            speak("Goodbye!")
            break
        else:
            speak("Sorry, I didn't understand that.")

if __name__ == '__main__':
    main()
