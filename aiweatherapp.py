# The depth of the comments serve as helpful notes to those new to Python - to be moved to documentation/readme
# -------------------------------------------------------------------------------------------------------------#

# Import libraries
import speech_recognition as sr
import pyttsx3
import sys
import requests
import json
import datetime as dt
import ttkbootstrap
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


'''
-- API Key Grammar --
We use the api url to view current data by city name. Openweathermap provides it as follows:
- https://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}

To use it we replace the "city name" by an actual city name such as "London" 
"API key" is replaced by the actual API key from your Openweathermap account
e.g. "12345678910abcdefghijklmnopqrstuvwxyz"

Using "London" as the city name this becomes:
- https://api.openweathermap.org/data/2.5/weather?q=London&appid=12345678910abcdefghijklmnopqrstuvwxyz

We can make our replacements using f-strings:
- f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
or string concatenation:
- "api.openweathermap.org/data/2.5/weather?q=" + {city name} + "&appid=" + {API key} 

-- API Security --
To prevent unwanted use of your API key make sure to keep it hidden from others.
In this case, the API key was placed in a text file in the same directory as aiweatherapp.py
The text file was then added to ignored files in .gitignore
The API should be the only text in the text file.
'''

# Collect the city name from the user and read API key from text file.
def main(event=None, use_voice=False):
    # Use the voice as input if voice is chosen
    if use_voice:
        city_name = listen_for_city()
        if not city_name:
            return
    else:
        try:
            city_name = city_name_entry.get().strip().title() # If voice is not given
        except (KeyboardInterrupt, EOFError):
            sys.exit(1)
    
    # Read API key from file and strip any extra whitespace/newlines
    with open('api_key.txt', 'r') as f:
        api_key = f.read().strip()
    
    # API URL
    api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
    
    # Get a response from the api by making a request
    response = get_response(api_url)
    
    # Query the response for weather data
    temp_kelvin, feels_like_kelvin, humidity, wind_speed, description, country, icon_id =  query_response(response)

    # Convert Temperature from Kelvin to Celsius and Fahrenheit
    temp_celsius, temp_fahrenheit = temp_converter(temp_kelvin)
    feels_like_celsius, feels_like_fahrenheit = temp_converter(feels_like_kelvin)

    # Collect icon using icon_id
    icon = get_icon(icon_id)

    # ----- Output // Frontend Label Configuration -------------------------------
    
    # Location: City, Country short code
    location_label.configure(text=f"{city_name}, {country}")

    # Icon
    icon_label.configure(image=icon)
    icon_label.image = icon

    # Temperature
    temp_label.configure(text=f"Temperature in {city_name}, {country} is {temp_celsius:.2f}°C ({temp_fahrenheit:.2f}°F / {temp_kelvin:.2f}°K).")

    # Feels Like
    feels_like_temp_label.configure(text=f"But it feels like {feels_like_celsius:.2f}°C ({feels_like_fahrenheit:.2f}°F / {feels_like_kelvin}°K).")

    # Humidity
    humidity_label.configure(text=f"The humidity is {humidity}%.")

    # Wind Speed
    wind_speed_label.configure(text=f"The wind speed is {wind_speed:.2f} m/s.")

    # Weather Description
    description_label.configure(text=f"The general weather has: {description}.")

    # print(f"Sunrise is at {sunrise} and sunset is at {sunset}.")

    # Update GUI
    root.update()

    # --------------- AI Reads the weather ------------------------------------------
    # ----- Prepare Weather data for AI Voice -----------------------------------

    weather_info = f"The weather in {city_name}, {country} is as follows. "
    weather_info += f"The temperature is {temp_celsius:.2f} degrees Celsius which equates to {temp_fahrenheit:.2f} degrees Fahrenheit and {temp_kelvin:.2f} degrees Kelvin. "
    weather_info += f"Despite that, it actually feels like {feels_like_celsius:.2f} degrees celsius. "
    weather_info += f"The humidity is {humidity} percent. "
    weather_info += f"AND the wind speed is {wind_speed:.2f} meters per second. "
    weather_info += f"In summary, the general weather is {description}."

    if use_voice:
        speak_weather(weather_info)


def get_response(api_url):
    try:
        rq = requests.get(api_url)
        # Raise an exception for bad responses (4xx or 5xx errors)
        rq.raise_for_status()
        # Convert response to JSON format to view the response better
        response = rq.json()
        return response
        # # Print formatted JSON response
        # print(json.dumps(response, indent=2))  
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        sys.exit(1)
    except response.status_code == 404:
        messagebox.showerror("Error", "City not found.")
        return None


# Query the API response
def query_response(response):
    temp_kelvin = response['main']['temp']
    feels_like_kelvin = response['main']['feels_like']
    humidity = response['main']['humidity']
    wind_speed = response['wind']['speed']
    description = response['weather'][0]['description']
    country = response['sys']['country']
    icon_id = response['weather'][0]['icon']

#     # sunrise = dt.datetime.utcfromtimestamp(['sys']['sunrise'] + response['timezone'])
#     # sunset = dt.datetime.utcfromtimestamp(['sys']['sunset'] + response['timezone'])

    return temp_kelvin, feels_like_kelvin, humidity, wind_speed, description, country, icon_id # sunrise, sunset)


# Temperature converter to convert Kelvin to Celsius and Fahrenheit
def temp_converter(temp_kelvin):
    temp_celsius = temp_kelvin - 273
    temp_fahrenheit = temp_celsius * (9/5) + 32
    return temp_celsius, temp_fahrenheit

def get_icon(icon_id):
    # Icon Url from Openweathermap
    icon_url = f"http://openweathermap.org/img/wn/{icon_id}@2x.png"
    # Get the weather icon image from the icon_url
    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image)
    return icon

# -------- AI Voice --------------------------------------------------------

def listen_for_city():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for city name...")
        audio = recognizer.listen(source)
    
    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return extract_city_name(text)
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
        return None
    except sr.RequestError:
        print("Sorry, there was an error with the speech recognition service.")
        return None

def extract_city_name(text):
    # Simple extraction - assumes the city name is the last word
    words = text.split()
    if len(words) > 0 and "weather" in text.lower():
        return words[-1]
    return None

def speak_weather(weather_info):
    engine = pyttsx3.init()
    engine.say(weather_info)
    engine.runAndWait()


# -------- Frontend // GUI --------------------------------------------------

# Set window
root = ttkbootstrap.Window(themename="morph")
# App Title on title bar
root.title("Weather App - Malambo Mutila 2024")
# Window size (width (horiz) x height (vert))
root.geometry("600x600")


# Entry widget to enter the city name
city_name_entry = ttkbootstrap.Entry(root, width=40, font=("Inter Light", 12))
city_name_entry.pack(pady=(64,24))
city_name_entry.bind("<Return>", main) # Respond to "enter"/"return"

# Button widget to search for the weather information
search_button = ttkbootstrap.Button(root, text="Search", command=main, bootstyle="warning")
search_button.pack()

# ----- Voice Search Button ----------
voice_button = ttkbootstrap.Button(root, text="Voice Search", command=lambda: main(use_voice=True), bootstyle="info")
voice_button.pack(pady=10)

# Label widget to show the city/country name
location_label = tk.Label(root, font=("Inter Light", 12))
location_label.pack(pady=(48,8))

# Label widget to show the weather icon
icon_label = tk.Label(root)
icon_label.pack()

# Label widget to show the temperature
temp_label = tk.Label(root, font=("Inter Light", 12))
temp_label.pack(pady=8)

# Label widget to show what temperature feels like
feels_like_temp_label = tk.Label(root, font=("Inter Light", 12))
feels_like_temp_label.pack()

# Label widget to show the humidity
humidity_label = tk.Label(root, font=("Inter Light", 12))
humidity_label.pack(pady=8)

# Label widget to show the wind speed
wind_speed_label = tk.Label(root, font=("Inter Light", 12))
wind_speed_label.pack()

# Label widget to show the description
description_label = tk.Label(root, font=("Inter Light", 12))
description_label.pack(pady=(8,0))


root.mainloop()
