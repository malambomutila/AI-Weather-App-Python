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
        city_name = input("Enter City: ").strip().title()
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
    temp_kelvin, feels_like_kelvin, humidity, wind_speed, description =  query_response(response)

    # Convert Temperature from Kelvin to Celsius and Fahrenheit
    temp_celsius, temp_fahrenheit = temp_converter(temp_kelvin)
    feels_like_celsius, feels_like_fahrenheit = temp_converter(feels_like_kelvin)

    # Output
    print(f"Temperature in {city_name} is {temp_celsius:.2f}°C / {temp_fahrenheit:.2f}°F / {temp_kelvin:.2f}°K")
    print("")
    print(f"Despite a temperature of {temp_celsius:.2f}°C, the temperature feels like {feels_like_celsius:.2f}°C / {feels_like_fahrenheit:.2f}°F / {feels_like_kelvin}°K.")
    print("")
    print(f"The humidity is {humidity}%.")
    print("")
    print(f"The wind speed is {wind_speed:.2f} m/s.")
    print("")
    print(f"The general weather has: {description}.")

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


# Query the API response
def query_response(response):
    temp_kelvin = response['main']['temp']

    feels_like_kelvin = response['main']['feels_like']

    humidity = response['main']['humidity']

    wind_speed = response['wind']['speed']

    description = response['weather'][0]['description']

#     # sunrise = dt.datetime.utcfromtimestamp(['sys']['sunrise'] + response['timezone'])
#     # sunset = dt.datetime.utcfromtimestamp(['sys']['sunset'] + response['timezone'])

    return temp_kelvin, feels_like_kelvin, humidity, wind_speed, description # sunrise, sunset)


# Temperature converter to convert Kelvin to Celsius and Fahrenheit
def temp_converter(temp_kelvin):
    temp_celsius = temp_kelvin - 273
    temp_fahrenheit = temp_celsius * (9/5) + 32
    return temp_celsius, temp_fahrenheit


if __name__ == "__main__":
    main()





# --------------------------------------------------------------------------------------- #
# GUI Draft 
# ---------------------------------------------------------------------------------------- #

# # Function to get weather info from API
# def get_weather(city_name):
#     API_Key = "fjdabfajdbajdbjd"
#     url = f"hdshdhsvdh{city_name}bdhfbhdbfhd{API_Key}"
#     response = requests.get(url)

#     if res.status_code == 404:
#         messagebox.showerror("Error", "City not found.")
#         return None
    
#     # Parse the response JSON
#     weather = response.json()
#     icon_id = weather['weather'][0]['icon']
#     temp_celsius = weather['main']['temp'] - 273.15
#     description = weather['weather'][0]['description']
#     city_name = weather['name']
#     country = weather['sys']['country']

#     # Icon Url and weather info
#     icon_url = f"http://openweathermap.org/img/wn/{icon_id}@2x.png"
#     return (icon_url, temp_celsius, description, city_name, country)

#     # If the city is found, unpack the weather information, icon_url, temp, descr...
#     location_label.configure(text=f"{city_name}, {country}")

#     # Get the weather icon image from the URL and update the icon label
#     Image = Image.open(requests.get(icon_url, stream=True).raw)
#     icon = ImageTk.PhotoImage(Image)
#     icon_label.configure(image=icon)
#     icon_label.image = icon

#     # Update the temperature and decription labels
#     temp_celsius_label.configure(text=f"Temperature: {temp_celsius:.2f}oC")
#     description_label.configure(text=f"Description: {description:.2f}")

# # Function to search weather for a city
# def search():
#     city = city_name_entry.get()
#     result = get_weather(city)
#     if result in None:
#         return

# # Frontend
# # Set window
# root = ttkbootstrap.Window(themename="morph")
# # App Title on title bar
# root.title("Weather App")
# # Window size
# root.geometry("400x400")


# # Entry widget to enter the city name
# city_name_entry = ttkbootstrap.Entry(root, font="Helvetica, 18")
# city_name_entry.pack(pady=10)

# # Button widget to search for the weather information
# search_button = ttkbootstrap.Button(root, text="Search", command=search, bootstyle="warning")
# search_button.pack(pady=10)

# # Label widget to show the city/country name
# location_label = tk.Label(root, font="Helvetica, 25")
# location_label.pack(pady=20)

# # Label widget to show the weather icon
# icon_label = tk.Label(root)
# icon_label.pack()

# # Label widget to show the temperature
# temp_celsius_label = tk.Label(root, font="Helvetica, 20")
# temp_celsius_label.pack()

# # Label widget to show the description
# description_label = tk.Label(root, font="Helvetica, 20")
# description_label.pack()


# root.mainloop()
