import google.generativeai as genai  # Import Gemini AI
import pyttsx3  # For text-to-speech
import speech_recognition as sr  # For speech recognition
import wikipedia  # For Wikipedia searches
import webbrowser  # To open web pages
import psutil  # To check battery status
from youtubesearchpython import VideosSearch  # To search for YouTube videos
import yt_dlp
import os
import time
import subprocess
import pyautogui  # Added for volume and brightness control
from   ecapture import ecapture as ec
import requests
import screen_brightness_control as sbc
import random
from pytube import Search  # Added for YouTube Music playback
import datetime

# Set up Gemini AI with API Key
GEMINI_API_KEY = "ENTER API KEY"
genai.configure(api_key=GEMINI_API_KEY)

# Global variable to track last used joke/riddle
last_joke = None
last_riddle = None

print('Loading your AI personal assistant - G One')

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(text):
    """ Converts text to speech """
    engine.say(text)
    engine.runAndWait()
    
def wishMe():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak("Hello, Good Morning")
        print("Hello, Good Morning")
    elif hour >= 12 and hour < 18:
        speak("Hello, Good Afternoon")
        print("Hello, Good Afternoon")
    else:
        speak("Hello, Good Evening")
        print("Hello, Good Evening")

def takeCommand():
    """ Captures voice command and returns text """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        
    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio).lower()
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        speak("Sorry, I couldn't understand that.")
        return ""
    except sr.RequestError:
        speak("Speech recognition service is unavailable.")
        return ""

def search_google(query):
    """ Searches Google and opens the results """
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(search_url)
    speak(f"Here are the search results for {query}")

def play_music(song_name):
    """ Searches YouTube and plays the first song automatically """
    search_query = f"ytsearch:{song_name}"  # Search query for yt_dlp

    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(search_query, download=False)['entries'][0]
            video_url = info['webpage_url']  # Get video link
            speak(f"Playing {song_name} on YouTube")
            webbrowser.open(video_url)
            print(f"Playing: {video_url}")
    except Exception as e:
        speak("Sorry, I couldn't find the song.")
        print("Error finding song:", e)
        
# Function to tell a joke
def tell_joke():
    global last_joke
    jokes = [
        "Why don't skeletons fight each other? They don't have the guts.",
        "I told my wife she was drawing her eyebrows too high. She looked surprised.",
        "Why don't programmers like nature? It has too many bugs.",
        "Why did the computer go to the doctor? It had a virus.",
        "Why did the scarecrow win an award? Because he was outstanding in his field.",
        "I asked the librarian if the library had any books on paranoia. She whispered, 'They're right behind you.'",
        "I told my computer I needed a break, and it froze."
    ]
    
    # Ensuring a new joke is picked that hasn't been told before
    joke = random.choice(jokes)
    while joke == last_joke:
        joke = random.choice(jokes)
    
    last_joke = joke
    speak(joke)
    print(joke)


# Function to tell a riddle
def tell_riddle():
    global last_riddle
    riddles = [
        {"question": "What has keys but can't open locks?", "answer": "A piano."},
        {"question": "What can travel around the world while staying in the corner?", "answer": "A stamp."},
        {"question": "What is full of holes but still holds a lot of weight?", "answer": "A net."},
    ]
    
    # Ensuring a new riddle is picked that hasn't been told before
    riddle = random.choice(riddles)
    while riddle == last_riddle:
        riddle = random.choice(riddles)
    
    last_riddle = riddle
    speak(f"Here's a riddle: {riddle['question']}")
    print(f"Riddle: {riddle['question']}")
    answer = takeCommand()
    
    if answer.lower() == riddle["answer"].lower():
        speak("Correct!")
        print("Correct!")
    else:
        speak(f"Wrong. The correct answer is: {riddle['answer']}")
        print(f"Wrong. The correct answer is: {riddle['answer']}")

#system battery
        
def system_status():
    battery = psutil.sensors_battery()
    battery_percent = battery.percent if battery else "Unknown"
    
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    memory_usage = memory.percent
    
    status = f"Battery is at {battery_percent} percent. CPU usage is at {cpu_usage} percent. Memory usage is at {memory_usage} percent."
    return status
    
        
# Function to open PC applications
def open_application(app_name):
    try:
        if app_name.lower() == "notepad":
            subprocess.run("notepad", shell=True)
            speak("Opening Notepad.")
        elif app_name.lower() == "calculator":
            subprocess.run("calc", shell=True)
            speak("Opening Calculator.")
        elif app_name.lower() == "microsoft word":
            os.system("start winword")  # Opens Microsoft Word
            speak("Opening Microsoft Word.")
        elif app_name.lower() == "microsoft excel":
            os.system("start excel")  # Opens Microsoft Excel
            speak("Opening Microsoft Excel.")
        elif app_name.lower() == "microsoft powerpoint":
            os.system("start powerpnt")  # Opens Microsoft PowerPoint
            speak("Opening Microsoft PowerPoint.")
        elif app_name.lower() == "microsoft edge":
            os.system("start msedge")  # Opens Microsoft Edge
            speak("Opening Microsoft Edge.")
        elif app_name.lower() == "settings":
            os.system("start ms-settings:")  # Opens Windows Settings
            speak("Opening PC Settings.")
        else:
            speak("Sorry, I couldn't find that application.")
    except Exception as e:
        speak("Sorry, I couldn't open the application.")
        print(f"Error opening application: {e}")
        
# Function to control volume
def adjust_volume(action):
    if action == "increase":
        pyautogui.press("volumedown")  # Decrease volume
    elif action == "decrease":
        pyautogui.press("volumeup")  # Increase volume
    speak(f"Volume has been {action}d.")
    print(f"Volume {action}d.")

# Function to control brightness
def adjust_brightness(action):
    try:
        current_brightness = sbc.get_brightness(display=0)[0]  # Get current brightness
        if "increase" in action:
            new_brightness = min(current_brightness + 20, 100)
        elif "decrease" in action:
            new_brightness = max(current_brightness - 20, 0)
        else:
            return "Please specify increase or decrease."

        sbc.set_brightness(new_brightness, display=0)  # Set new brightness
        speak(f"Brightness adjusted to {new_brightness} percent.")
        print(f"Brightness adjusted to {new_brightness} percent.")
    except Exception as e:
        speak(f"Failed to adjust brightness: {str(e)}")
        print(f"Failed to adjust brightness: {str(e)}")



def ask_gemini(query):
    """ Gets responses from Gemini AI for general queries, limited to 2 lines """
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")  # Load Gemini Model
        response = model.generate_content(query)  # Generate response
        answer = response.text
        # Limit response to 2 lines
        answer = "\n".join(answer.splitlines()[:2])
        speak(answer)  # Speak the response
        print(f"AI Response: {answer}") # Print response
        return answer
    except Exception as e:
        error_msg = f"Error with Gemini AI: {e}"
        speak("Sorry, I couldn't process that request.")
        print(error_msg)
        return error_msg

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio).lower()
            print("User said:", text)
            return text
        except sr.UnknownValueError:
            print("Could not understand the audio")
            return None
        except sr.RequestError:
            print("Speech recognition service is unavailable")
            return None


def get_weather():
    """ Fetch weather information from OpenWeatherMap API """
    battery = psutil.sensors_battery()
    
    speak("Please tell me the city name.")
    city_name = takeCommand()

    api_key = "ENTER WEATHER API KEY"
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    
    # Construct final URL
    complete_url = f"{base_url}q={city_name}&appid={api_key}&units=metric"

    # Make API request
    try:
        response = requests.get(base_url)
        x = response.json()  # Get the JSON response

        # Check if the response contains "cod" key and if it's not 200 (error)
        if x.get("cod") != 200:
            speak("City Not Found. Please try again.")
            return

        # Extract weather details
        y = x.get("main", {})
        current_temperature_kelvin = y.get("temp", "N/A")
        current_temperature_celsius = round(current_temperature_kelvin - 273.15, 2) if isinstance(current_temperature_kelvin, (int, float)) else "N/A"
        current_humidity = y.get("humidity", "N/A")

        z = x.get("weather", [{}])
        weather_description = z[0].get("description", "N/A")

        # Output and speech
        speak(f"Temperature is {current_temperature_kelvin} degree Celsius. "
              f"Humidity is {current_humidity} percent. "
              f"Weather description: {weather_description}.")
        
        print(f"Temperature: {current_temperature_kelvin}°C")
        print(f"Humidity: {current_humidity}%")
        print(f"Weather: {weather_description}")

    except requests.exceptions.RequestException as e:
        speak("Sorry, I couldn't fetch the weather data.")
        print(f"Request error: {e}")
    except KeyError:
        speak("Sorry, I couldn't find weather details for this location.")
        print("Error: Unexpected response format. Check the API response.")



def main():
    while True:
        command = recognize_speech()
        if command:
            if "assistant" in command:
                query = command.replace("assistant", "").strip()
                if query:
                    ask_gemini(query)
                else:
                    speak("Yes, how can I assist you?")
    
speak("Loading your AI personal assistant G-One")
wishMe()


if _name_ == "_main_":

    while True:
        speak("Tell me, how can I help you now?")
        statement = takeCommand()

        if statement == "":
            continue

        if "goodbye" in statement or "ok bye" in statement or "stop" in statement:
            speak('Your assistant is shutting down. Goodbye!')
            print('Your assistant is shutting down. Goodbye!')
            break

        elif "wikipedia" in statement:
            speak("Searching Wikipedia...")
            query = statement.replace("wikipedia", "").strip()
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except wikipedia.exceptions.DisambiguationError:
                speak("There are multiple results. Please be more specific.")
            except wikipedia.exceptions.PageError:
                speak("Sorry, no matching Wikipedia page was found.")

        elif 'play' in statement and 'song' in statement:
            song_name = statement.replace('play', '').replace('song', '').strip()
            play_music(song_name)
        
        elif 'increase volume' in statement:
            adjust_volume("increase")

        elif 'decrease volume' in statement:
            adjust_volume("decrease")

        elif 'increase brightness' in statement:
            adjust_brightness("increase")

        elif 'decrease brightness' in statement:
            adjust_brightness("decrease")
            
        elif 'open youtube' in statement:
            webbrowser.open_new_tab("https://www.youtube.com")
            speak("YouTube is open now")
            time.sleep(5)

        elif 'open google' in statement:
            webbrowser.open_new_tab("https://www.google.com")
            speak("Google Chrome is open now")
            time.sleep(5)

        elif 'open gmail' in statement:
            webbrowser.open_new_tab("gmail.com")
            speak("Google Mail is open now")
            time.sleep(5)

        elif "weather" in statement:
            api_key = "8ef61edcf1c576d65d836254e11ea420"
            base_url = "https://api.openweathermap.org/data/2.5/weather?"
            speak("What's the city name?")
            city_name = takeCommand()
            complete_url = base_url + "appid=" + api_key + "&q=" + city_name
            response = requests.get(complete_url)
            x = response.json()
            if x["cod"] != "404":
                y = x["main"]
                current_temperature = y["temp"]
                current_humidity = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                speak(f"Temperature in Kelvin unit is {current_temperature}, humidity in percentage is {current_humidity}, description {weather_description}")
                print(f"Temperature: {current_temperature} K\nHumidity: {current_humidity}%\nDescription: {weather_description}")
            else:
                speak("City Not Found")

        elif 'time' in statement:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        elif 'who are you' in statement or 'what can you do' in statement:
            speak('I am G-One, your personal assistant. I can open websites, search Wikipedia, predict weather, play songs, and much more!')

        elif "who made you" in statement or "who created you" in statement:
            speak("I was built by Shanthini")
            print("I was built by Shanthini")

        elif "open stackoverflow" in statement:
            webbrowser.open_new_tab("https://stackoverflow.com/login")
            speak("Here is Stack Overflow")

        elif 'web news' in statement:
            webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
            speak('Here are some headlines from the Times of India. Happy reading!')
            time.sleep(6)

        elif "camera" in statement or "take a photo" in statement:
            ec.capture(0, "robo camera", "img.jpg")

        elif 'search' in statement:
            statement = statement.replace("search", "").strip()
            search_google(statement)
     
        elif 'open notepad' in statement:
            open_application("notepad")

        elif 'open calculator' in statement:
            open_application("calculator")

        elif 'open microsoft word' in statement:
            open_application("microsoft word")

        elif 'open microsoft excel' in statement:
            open_application("microsoft excel")

        elif 'open microsoft powerpoint' in statement:
            open_application("microsoft powerpoint")

        elif 'open microsoft edge' in statement:
            open_application("microsoft edge")

        elif 'open settings' in statement:
            open_application("settings")

        elif "log off" in statement or "sign out" in statement:
            speak("Ok, your PC will log off in 10 seconds. Make sure you exit all applications.")
            subprocess.call(["shutdown", "/l"])

        elif 'joke' in statement:
            tell_joke()
        
        elif 'riddle' in statement:
            tell_riddle()
            
        if "battery status" in statement or "system status" in statement:

         status = system_status()  # Get the system status
         speak(status)  # Speak the system status
         print(status)  # Print the system status to the console

        elif "increase brightness" in statement:
         speak(adjust_brightness("increase"))

        elif "decrease brightness" in statement:
         speak(adjust_brightness("decrease"))

        elif "assistant" in statement:
            query = statement.replace("assistant", "").strip()
            if query:
                ask_gemini(query)  # Call Gemini AI
            else:
                speak("Yes, how can I assist you?")

            
        time.sleep(3)
