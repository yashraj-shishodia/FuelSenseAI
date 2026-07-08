import os
import requests

API_KEY = os.getenv("GEOAPIFY_API_KEY")


def calculate_population_score(latitude, longitude):

    categories = ",".join([
        "commercial.supermarket",
        "commercial.shopping_mall",
        "education.school",
        "education.college",
        "healthcare.hospital",
        "service.financial.bank",
        "catering.restaurant",
        "public_transport",
        "office"
    ])

    url = (
        "https://api.geoapify.com/v2/places"
        f"?categories={categories}"
        f"&filter=circle:{longitude},{latitude},1500"
        "&limit=200"
        f"&apiKey={API_KEY}"
    )

    try:

        response = requests.get(url)

        data = response.json()

        features = data.get("features", [])

        score = 0

        for place in features:

            category = ",".join(
                place["properties"].get(
                    "categories",
                    []
                )
            )

            if "shopping_mall" in category:
                score += 8

            elif "supermarket" in category:
                score += 6

            elif "hospital" in category:
                score += 6

            elif "school" in category:
                score += 5

            elif "college" in category:
                score += 6

            elif "bank" in category:
                score += 3

            elif "restaurant" in category:
                score += 3

            elif "public_transport" in category:
                score += 8

            elif "office" in category:
                score += 7

        score = min(score, 100)

        estimated_people = int(
            score * 18
        )

        avg_people_vehicle = 1.8

        estimated_vehicles = int(
            estimated_people /
            avg_people_vehicle
        )

        return {

            "population_score": score,

            "estimated_people": estimated_people,

            "estimated_vehicles": estimated_vehicles

        }

    except:

        return {

            "population_score": 50,

            "estimated_people": 900,

            "estimated_vehicles": 500

        }