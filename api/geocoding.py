import os
import requests

def search_place(location):

    API_KEY = os.getenv("GEOAPIFY_API_KEY", "").strip()

    if not API_KEY:
        return {
            "results": [],
            "error": "Missing Geoapify API key"
        }

    url = (
        "https://api.geoapify.com/v1/geocode/search"
        f"?text={location}"
        "&limit=1"
        f"&apiKey={API_KEY}"
    )

    response = requests.get(url)

    if response.status_code != 200:

        error_message = None
        try:
            error_message = response.json().get("message")
        except Exception:
            pass

        error_message = error_message or response.text
        print("Geocoding Error:", error_message)

        return {
            "results": [],
            "error": error_message
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