import os
import requests
from math import radians, sin, cos, sqrt, atan2
from datetime import datetime

from api.prediction import predict_crowd
from api.weather import get_weather

API_KEY = os.getenv("GEOAPIFY_API_KEY")


# ---------------------------------------
# Distance Calculation
# ---------------------------------------

def calculate_distance(lat1, lon1, lat2, lon2):

    R = 6371

    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)

    a = (
        sin(dLat / 2) ** 2 +
        cos(radians(lat1)) *
        cos(radians(lat2)) *
        sin(dLon / 2) ** 2
    )

    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a)
    )

    return R * c


# ---------------------------------------
# Nearby Stations
# ---------------------------------------

def nearbyStations(latitude,
                   longitude,
                   prediction_time=None):

    url = (
        "https://api.geoapify.com/v2/places"
        f"?categories=service.vehicle.fuel"
        f"&filter=circle:{longitude},{latitude},5000"
        "&limit=20"
        f"&apiKey={API_KEY}"
    )

    response = requests.get(url)

    if response.status_code != 200:

        print(response.text)

        return {
            "features": []
        }

    data = response.json()

    stations = []

    if prediction_time:

        prediction_time = datetime.fromisoformat(
            prediction_time
        )

    # ---------------------------------------
    # Fetch Weather ONLY ONCE
    # ---------------------------------------

    weather = get_weather(
        latitude,
        longitude
    )["weather"]

    for station in data.get("features", []):

        lat = station["geometry"]["coordinates"][1]
        lon = station["geometry"]["coordinates"][0]

        distance = calculate_distance(
            latitude,
            longitude,
            lat,
            lon
        )

        station["distance"] = round(
            distance,
            2
        )

        station = predict_crowd(
            station,
            weather,
            prediction_time
        )

        stations.append(station)

    # ---------------------------------------
    # Sort Stations
    # ---------------------------------------

    stations.sort(
        key=lambda x: (
            x["waiting_time"],
            x["distance"]
        )
    )

    # Return Best 5 Stations

    return {
        "features": stations[:5]
    }