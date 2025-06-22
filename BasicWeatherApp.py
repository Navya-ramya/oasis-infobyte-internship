from tkinter import *
from tkinter import ttk
import requests
import pyttsx3
import speech_recognition as sr
import matplotlib.pyplot as plt
from datetime import datetime

# Initialize speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Predefined cities
cities = ["Chittoor", "Anantapur", "Chennai", "Hyderabad", "Bangalore", "Delhi", "Mumbai"]

#  Voice input
def recognize_city():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Please say the city name.")
        try:
            audio = recognizer.listen(source, timeout=5)
            city = recognizer.recognize_google(audio)
            com.set(city)
            speak(f"You said {city}")
        except:
            speak("Sorry, I couldn't recognize your voice.")

#  Get current weather
def get_weather():
    city = com.get()
    api_key = '253682c0bd759acfb4255d4aa08c3dd7'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'

    try:
        response = requests.get(url)
        data = response.json()

        temp_c = data['main']['temp'] - 273.15
        humidity = data['main']['humidity']
        condition = data['weather'][0]['description']
        wind = data['wind']['speed']
        pressure = data['main']['pressure']
        country = data['sys']['country']

        result = (f"City: {city}, {country}\n"
                  f"Temperature: {temp_c:.2f} °C\n"
                  f"Humidity: {humidity}%\n"
                  f"Condition: {condition}\n"
                  f"Wind Speed: {wind} m/s\n"
                  f"Pressure: {pressure} hPa")

        result_label.config(text=result)
        speak(f"The weather in {city} is {condition} with temperature {temp_c:.1f} degrees Celsius.")

    except:
        result_label.config(text="Error: City not found or no internet.")
        speak("Couldn't fetch the weather.")

#  3-Day Forecast
def get_forecast():
    city = com.get()
    api_key = '253682c0bd759acfb4255d4aa08c3dd7'
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}"

    try:
        response = requests.get(url)
        data = response.json()
        forecast_text = f"3-day forecast for {city}:\n\n"

        count = 0
        for item in data['list']:
            if '12:00:00' in item['dt_txt']:
                date = item['dt_txt'].split()[0]
                temp_c = item['main']['temp'] - 273.15
                condition = item['weather'][0]['description']
                forecast_text += f"{date}: {temp_c:.1f} °C, {condition}\n"
                count += 1
            if count == 3:
                break

        forecast_label.config(text=forecast_text)
        speak("Here is the 3-day forecast.")

    except:
        forecast_label.config(text="Unable to fetch forecast.")
        speak("Forecast fetch failed.")

#  5-Day Chart
def show_chart():
    city = com.get()
    api_key = '253682c0bd759acfb4255d4aa08c3dd7'
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}"

    try:
        response = requests.get(url)
        data = response.json()

        dates = []
        temps = []

        for item in data['list']:
            if '12:00:00' in item['dt_txt']:
                date = item['dt_txt'].split()[0]
                temp_c = item['main']['temp'] - 273.15
                dates.append(date)
                temps.append(temp_c)

        plt.figure(figsize=(8, 4))
        plt.plot(dates, temps, marker='o', color='tomato')
        plt.title(f"5-Day Temperature Forecast for {city}")
        plt.xlabel("Date")
        plt.ylabel("Temperature (°C)")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    except:
        speak("Sorry, unable to generate chart.")

# Autocomplete
def on_key_release(event):
    value = event.widget.get()
    if value:
        matches = [city for city in cities if value.lower() in city.lower()]
        listbox_update(matches)
    else:
        listbox_update([])

def listbox_update(matches):
    listbox.delete(0, END)
    for match in matches:
        listbox.insert(END, match)

def on_select(event):
    selected_city = listbox.get(ACTIVE)
    com.set(selected_city)
    listbox_update([])

# Safe live clock
def update_clock():
    try:
        now = datetime.now().strftime('%H:%M:%S')
        clock_label.config(text=f"Time: {now}")
        win.after(1000, update_clock)
    except:
        pass

# Graceful exit
def on_closing():
    win.destroy()

# GUI Setup 
win = Tk()
win.title("Weather Assistant")
win.geometry("700x600")
win.config(bg="#f0f0f0")

Label(win, text="Weather Assistant", font=("Helvetica", 24, "bold"), bg="#f0f0f0").place(x=200, y=20)

# Clock
clock_label = Label(win, font=("Helvetica", 12), bg="#f0f0f0", fg="black")
clock_label.place(x=560, y=20)
update_clock()

# Combobox for city
com = ttk.Combobox(win, values=cities, font=("Helvetica", 12))
com.place(x=240, y=80, width=200)
com.bind('<KeyRelease>', on_key_release)

# Listbox for suggestions
listbox = Listbox(win, font=("Helvetica", 12))
listbox.place(x=240, y=110, width=200, height=100)
listbox.bind('<<ListboxSelect>>', on_select)

# Buttons
Button(win, text=" Speak City", command=recognize_city, bg="#2196F3", fg="white", font=("Helvetica", 10)).place(x=100, y=230)
Button(win, text="Get Weather", command=get_weather, bg="#4CAF50", fg="white", font=("Helvetica", 10)).place(x=250, y=230)
Button(win, text=" 3-Day Forecast", command=get_forecast, bg="#FF9800", fg="white", font=("Helvetica", 10)).place(x=380, y=230)
Button(win, text=" Show Chart", command=show_chart, bg="#00BCD4", fg="white", font=("Helvetica", 10)).place(x=540, y=230)

# Output Labels
result_label = Label(win, text="", font=("Helvetica", 12), bg="#f0f0f0", justify=LEFT, wraplength=600)
result_label.place(x=50, y=300)

forecast_label = Label(win, text="", font=("Helvetica", 12), bg="#f0f0f0", justify=LEFT, wraplength=600)
forecast_label.place(x=50, y=430)

win.protocol("WM_DELETE_WINDOW", on_closing)
win.mainloop()
