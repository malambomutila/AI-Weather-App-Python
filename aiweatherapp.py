# The depth of the comments serve as helpful notes to those new to Python - to be moved to documentation/readme
# -------------------------------------------------------------------------------------------------------------#

# Import libraries
import sys
import requests
import json
import datetime as dt

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