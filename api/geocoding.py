import os
import requests

API_KEY = os.getenv("GEOAPIFY_API_KEY")


def search_place(location):

    url = (
        "https://api.geoapify.com/v1/geocode/search"
        f"?text={location}"
        "&limit=1"
        f"&apiKey={API_KEY}"
    )

    response = requests.get(url)

    if response.status_code != 200:

        print("Geocoding Error:", response.text)

        return {
            "results": []
        }

    data = response.json()

    results = []

    for feature in data.get("features", []):

        results.append({

            "name": feature["properties"].get(
                "formatted",
                location
            ),

            "lat": feature["properties"]["lat"],

            "lon": feature["properties"]["lon"]

        })

    return {
        "results": results
    }