from datetime import datetime
import joblib
import pandas as pd

from api.weather import get_weather

# -----------------------------
# Load ML Model
# -----------------------------

model = joblib.load("models/crowd_model.pkl")

weather_encoder = joblib.load(
    "models/weather_encoder.pkl"
)

brand_encoder = joblib.load(
    "models/brand_encoder.pkl"
)

poi_encoder = joblib.load(
    "models/poi_encoder.pkl"
)


# -----------------------------
# POI Level
# -----------------------------

def get_poi_level(station):

    props = station.get("properties", {})

    text = (
        str(props.get("formatted", "")) + " " +
        str(props.get("city", "")) + " " +
        str(props.get("district", ""))
    ).lower()

    score = 0

    keywords = {

        "mall": 3,
        "market": 3,
        "metro": 3,
        "station": 2,
        "hospital": 2,
        "school": 1,
        "college": 2,
        "office": 2,
        "airport": 4,
        "industrial": 3,
        "bus": 2

    }

    for key, value in keywords.items():

        if key in text:

            score += value

    if score >= 8:

        return "HIGH"

    elif score >= 4:

        return "MEDIUM"

    else:

        return "LOW"


# -----------------------------
# Prediction
# -----------------------------

def predict_crowd(
    station,
    latitude,
    longitude,
    prediction_time=None
):

    if prediction_time is None:

        prediction_time = datetime.now()

    hour = prediction_time.hour

    weekday = prediction_time.weekday()

    month = prediction_time.month

    holiday = 1 if weekday >= 5 else 0

    weather = get_weather(
        latitude,
        longitude
    )["weather"]

    brand = station["properties"].get(
        "brand",
        "Indian Oil"
    )

    poi_level = get_poi_level(
        station
    )

    # Estimated Pump Count

    brand_lower = brand.lower()

    if "indian" in brand_lower:

        pump_count = 8

    elif "hp" in brand_lower:

        pump_count = 7

    elif "bp" in brand_lower:

        pump_count = 7

    elif "shell" in brand_lower:

        pump_count = 6

    else:

        pump_count = 5

    service_time = 2.5

    # -----------------------
    # Encoding
    # -----------------------

    try:

        weather_encoded = weather_encoder.transform(
            [weather]
        )[0]

    except:

        weather_encoded = weather_encoder.transform(
            ["Clear"]
        )[0]

    try:

        brand_encoded = brand_encoder.transform(
            [brand]
        )[0]

    except:

        brand_encoded = 0

    poi_encoded = poi_encoder.transform(
        [poi_level]
    )[0]

    # -----------------------
    # Prediction
    # -----------------------

    features = pd.DataFrame([{

        "hour": hour,

        "weekday": weekday,

        "month": month,

        "holiday": holiday,

        "weather": weather_encoded,

        "brand": brand_encoded,

        "poi_level": poi_encoded,

        "pump_count": pump_count,

        "service_time": service_time

    }])

    queue = int(

        round(

            model.predict(features)[0]

        )

    )

    queue = max(

        0,

        min(queue, 35)

    )

    waiting = round(

        queue *

        service_time /

        pump_count,

        1

    )

    if waiting <= 5:

        crowd = "LOW"

    elif waiting <= 10:

        crowd = "MEDIUM"

    elif waiting <= 18:

        crowd = "HIGH"

    else:

        crowd = "VERY HIGH"

    score = max(

        60,

        100 - int(waiting * 2)

    )

    station["queue_length"] = queue

    station["waiting_time"] = waiting

    station["predicted_crowd"] = crowd

    station["prediction_score"] = score

    return station