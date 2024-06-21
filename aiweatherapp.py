# The depth of the comments serve as helpful notes to those new to Python - to be moved to documentation/readme
# -------------------------------------------------------------------------------------------------------------#

# Import libraries
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
def main():
    try:
        city_name = city_name_entry.get()
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

    # ----- Output // Label Configuration ----------------------------------------
    
    # Location: City, Country short code
    location_label.configure(text=f"{city_name}, {country}")

    # Icon
    icon_label.configure(image=icon)
    icon_label.image = icon

    # Temperature
    temp_label.configure(text=f"Temperature in {city_name}, {country} is {temp_celsius:.2f}°C / {temp_fahrenheit:.2f}°F / {temp_kelvin:.2f}°K")

    # Feels Like
    feels_like_temp_label.configure(text=f"Despite a temperature of {temp_celsius:.2f}°C, the temperature feels like {feels_like_celsius:.2f}°C / {feels_like_fahrenheit:.2f}°F / {feels_like_kelvin}°K.")

    # Humidity
    humidity_label.configure(text=f"The humidity is {humidity}%.")

    # Wind Speed
    wind_speed_label.configure(text=f"The wind speed is {wind_speed:.2f} m/s.")

    # Weather Description
    description_label.configure(text=f"The general weather has: {description}.")

    # print(f"Sunrise is at {sunrise} and sunset is at {sunset}.")


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

# -------- Frontend // GUI --------------------------------------------------

# Set window
root = ttkbootstrap.Window(themename="morph")
# App Title on title bar
root.title("Weather App")
# Window size
root.geometry("400x400")


# Entry widget to enter the city name
city_name_entry = ttkbootstrap.Entry(root, font="Inter, 18")
city_name_entry.pack(pady=10)

# Button widget to search for the weather information
search_button = ttkbootstrap.Button(root, text="Search", command=main, bootstyle="warning")
search_button.pack(pady=10)

# Label widget to show the city/country name
location_label = tk.Label(root, font="Inter, 25")
location_label.pack(pady=20)

# Label widget to show the weather icon
icon_label = tk.Label(root)
icon_label.pack()

# Label widget to show the temperature
temp_label = tk.Label(root, font="Inter, 20")
temp_label.pack()

# Label widget to show what temperature feels like
feels_like_temp_label = tk.Label(root, font="Inter, 20")
feels_like_temp_label.pack()

# Label widget to show the humidity
humidity_label = tk.Label(root, font="Inter, 20")
humidity_label.pack()

# Label widget to show the wind speed
wind_speed_label = tk.Label(root, font="Inter, 20")
wind_speed_label.pack()

# Label widget to show the description
description_label = tk.Label(root, font="Inter, 20")
description_label.pack()


root.mainloop()
