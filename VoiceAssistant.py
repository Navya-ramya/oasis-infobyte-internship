import pyttsx3
import speech_recognition as sr
import pyautogui
import time
import datetime
import wikipedia
import webbrowser
import os
import random
import smtplib
import pyjokes
import psutil
import requests
from googletrans import Translator
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import threading

# Initialize the speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Dictionary of email recipients
email_dict = {"friend": "friend@example.com", "family": "family@example.com"}

# Dictionary of applications to open
apps = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
}

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Hunterdii. Please tell me how may I help you")

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('navyahoney216@gmail.com', 'Navya@6300')  
    server.sendmail('navyahani549@gmail.com', to, content)
    server.close()

def get_weather(city="Chittoor"):
    api_key = "66c16fa61744c93de945c7b48f006d3f" 
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    data = response.json()
    if data["cod"] == 200:
        main = data["main"]
        weather = data["weather"][0]["description"]
        temp = main["temp"]
        speak(f"The weather in {city} is {weather} with a temperature of {temp} degrees Celsius.")
    else:
        speak("City not found.")

def get_news():
    news_url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=your_newsapi_key" 
    response = requests.get(news_url).json()
    articles = response["articles"][:5]
    for i, article in enumerate(articles, start=1):
        speak(f"News {i}: {article['title']}")

def set_volume(level):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(level / 100.0, None)

def translate_to_hindi(text):
    translator = Translator()
    result = translator.translate(text, dest='hi')
    speak(f"The translation in Hindi is: {result.text}")

def reminder_after_delay(seconds, task):
    time.sleep(seconds)
    speak(f"Reminder: {task}")

if __name__ == "__main__":
    wishMe()
    while True:
        query = takecommand().lower()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'tell me a joke' in query:
            joke = pyjokes.get_joke()
            print(joke)
            speak(joke)

        elif 'open' in query:
            app = query.replace('open', '').strip()
            if app in apps:
                os.system(f"start {apps[app]}")
                speak(f"Opening {app}")
            else:
                speak("I don't know that application.")

        elif 'play music' in query:
            music_url = "https://music.youtube.com/"
            webbrowser.open(music_url)
            time.sleep(5)
            pyautogui.press('space')

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The current time is {strTime}")

        elif 'the date' in query:
            date = datetime.datetime.now().strftime("%A, %d %B %Y")
            speak(f"Today's date is {date}")

        elif 'search google for' in query:
            search_query = query.replace('search google for', '')
            webbrowser.open(f"https://www.google.com/search?q={search_query}")

        elif 'search youtube for' in query:
            search_query = query.replace('search youtube for', '')
            webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")

        elif 'send email to' in query:
            try:
                speak("What should I say?")
                content = takecommand()
                speak("Who should I send it to?")
                recipient = takecommand().lower()
                to = email_dict.get(recipient, None)
                if to:
                    sendEmail(to, content)
                    speak("Email has been sent!")
                else:
                    speak("I don't have that contact.")
            except Exception as e:
                print(e)
                speak("Sorry, I am not able to send this email.")

        elif 'take screenshot' in query:
            screenshot = pyautogui.screenshot()
            screenshot.save("screenshot.png")
            speak("Screenshot taken and saved as screenshot.png")

        elif 'remember that' in query:
            speak("What should I remember?")
            memory = takecommand()
            with open("memory.txt", "w") as f:
                f.write(memory)
            speak("I will remember that.")

        elif 'what do you remember' in query:
            try:
                with open("memory.txt", "r") as f:
                    remembered = f.read()
                speak(f"You asked me to remember: {remembered}")
            except FileNotFoundError:
                speak("I don’t remember anything yet.")

        elif 'battery' in query:
            battery = psutil.sensors_battery()
            percent = battery.percent
            speak(f"Battery is at {percent} percent")

        elif 'lock the system' in query:
            speak("Locking the system")
            os.system("rundll32.exe user32.dll,LockWorkStation")

        elif 'shutdown' in query:
            speak("Shutting down the system")
            os.system("shutdown /s /t 1")

        elif 'restart' in query:
            speak("Restarting the system")
            os.system("shutdown /r /t 1")

        elif 'exit' in query or 'quit' in query:
            speak("Goodbye! Have a great day.")
            break

        elif 'weather' in query:
            speak("For which city?")
            city = takecommand()
            get_weather(city)

        elif 'news' in query:
            speak("Fetching the latest news headlines.")
            get_news()

        elif 'set volume to' in query:
            try:
                vol = int([int(s) for s in query.split() if s.isdigit()][0])
                set_volume(vol)
                speak(f"Volume set to {vol} percent")
            except:
                speak("Sorry, I couldn't set the volume.")

        elif 'translate to hindi' in query:
            speak("What should I translate?")
            phrase = takecommand()
            translate_to_hindi(phrase)

        elif 'take a break' in query:
            speak("Okay, I will take a 5 minute break. Call me if you need me.")
            time.sleep(300)
            speak("I'm back. How can I assist you?")

        elif 'remind me to' in query:
            speak("In how many seconds?")
            delay = int(takecommand())
            task = query.replace("remind me to", "").strip()
            speak(f"I will remind you to {task} in {delay} seconds")
            threading.Thread(target=reminder_after_delay, args=(delay, task)).start()
