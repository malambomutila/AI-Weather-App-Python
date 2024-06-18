# Import libraries
import sys
import requests
import json
import datetime as dt

# API Key Grammar: https://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}
# --- Example: https://api.openweathermap.org/data/2.5/weather?q=London&appid=12345678910abcdefghijklmnopqrstuvwxyz

# We replace the city "London" with user desired city and "12345678910abcdefghijklmnopqrstuvwxyz" by the actual API key.
# We do this using f-strings or string concatenation:
# --- "api.openweathermap.org/data/2.5/weather?q=" + {city name} + "&appid=" + {API key}

def main():
    # Catch errors
    try:
        city_name = input("Enter City: ").strip().title()
    except (KeyboardInterrupt,EOFError):
        sys.exit(1)
    api_key = open('api_key.txt', 'r').read()

    api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
    response = requests.get(api_url).json

    print(json.dumps(response.json(), indent=2))
    # Catch errors
    # get_response(city_name, api_key)
    
    # # Query
    # (temp_kelvin, feels_like_kelvin, humidity, description) = api_query(response)
    # # Convert Temperatures
    # temp_celsius, temp_fahrenheit = temp_converter(temp_kelvin)
    # feels_like_celsius, feels_like_fahrenheit = temp_converter(feels_like_kelvin)

    # print(f"Temperature in {city_name} is {temp_celsius:.2f}C / {temp_fahrenheit:.2f}F / {temp_kelvin:.2f}K")
    
    # print(f"Despite a temperature of {temp_celsius:.2f}C, the temperature feels like {feels_like_celsius:.2f}C / {feels_like_fahrenheit}F / {feels_like_kelvin}K.")
    
    # print(f"The humidity is {humidity}%.")
    # print(f"The general weather is {description}.")
    # print(f"Sunrise is at {sunrise} and sunset is at {sunset}.")

# Get response from the API
# def get_response(city_name, api_key):
#     try:
#         api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
#         response = requests.get(api_url).json
#     except (KeyboardInterrupt, EOFError):
#         sys.exit(1)
#     # Error types
#     # response = requests.get(api_url).json

#     # Preview the response
#     print(json.dumps(response.json(), indent=2))

# # Query the API
# def api_query(response):
#     temp_kelvin = response['main']['temp']

#     feels_like_kelvin = response['main']['feels like']

#     humidity = response['main']['humidity']

#     description = response['weather'][0]['description']

#     # sunrise = dt.datetime.utcfromtimestamp(['sys']['sunrise'] + response['timezone'])
#     # sunset = dt.datetime.utcfromtimestamp(['sys']['sunset'] + response['timezone'])

#     return (temp_kelvin, feels_like_kelvin, humidity, description) # sunrise, sunset)


# # Convert temperature to celsius and Fahrenheit
# def temp_converter(temp_kelvin):
#     temp_celsius = temp_kelvin - 273
#     temp_fahrenheit = temp_celsius * (9/5) + 32
#     return (temp_celsius, temp_fahrenheit)


if __name__ == "__main__":
    main()