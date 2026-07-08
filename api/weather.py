import os
import requests

API_KEY = os.getenv("OPENWEATHER_API_KEY")


def get_weather(latitude, longitude):

    if not API_KEY:
        return {
            "weather": "Sunny",
            "temperature": 30
        }

    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?lat={latitude}"
        f"&lon={longitude}"
        f"&appid={API_KEY}"
        "&units=metric"
    )

    try:

        response = requests.get(url)

        data = response.json()

        return {

            "weather": data["weather"][0]["main"],

            "temperature": data["main"]["temp"]

        }

    except:

        return {

            "weather": "Sunny",

            "temperature": 30

        }