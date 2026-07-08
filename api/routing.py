import os
import requests

API_KEY = os.getenv("GEOAPIFY_API_KEY")


def get_route(source_lat, source_lon,
              destination_lat, destination_lon):

    url = (
        "https://api.geoapify.com/v1/routing"
        f"?waypoints={source_lat},{source_lon}|"
        f"{destination_lat},{destination_lon}"
        "&mode=drive"
        "&details=instruction_details"
        "&units=metric"
        f"&apiKey={API_KEY}"
    )

    response = requests.get(url)

    if response.status_code != 200:
        print("Routing Error:", response.text)
        return None

    return response.json()