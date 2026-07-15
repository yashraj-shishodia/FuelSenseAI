import os
import subprocess
import sys
from datetime import datetime
import joblib
import pandas as pd

from api.weather import get_weather
from database.db import save_prediction

# -----------------------------
# Load ML Model
# -----------------------------

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")
TRAIN_SCRIPT = os.path.join(BASE_DIR, "ml", "train_model.py")

os.makedirs(MODEL_DIR, exist_ok=True)

required_models = [
    "crowd_model.pkl",
    "weather_encoder.pkl",
    "brand_encoder.pkl",
    "poi_encoder.pkl"
]

missing_models = [
    model_name for model_name in required_models
    if not os.path.exists(os.path.join(MODEL_DIR, model_name))
]


model = joblib.load(os.path.join(MODEL_DIR, "crowd_model.pkl"))

weather_encoder = joblib.load(
    os.path.join(MODEL_DIR, "weather_encoder.pkl")
)

brand_encoder = joblib.load(
    os.path.join(MODEL_DIR, "brand_encoder.pkl")
)

poi_encoder = joblib.load(
    os.path.join(MODEL_DIR, "poi_encoder.pkl")
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

    return "LOW"


# -----------------------------
# Prediction
# -----------------------------

def predict_crowd(
    station,
    weather,
    prediction_time=None
):

    if prediction_time is None:

        prediction_time = datetime.now()

    hour = prediction_time.hour

    weekday = prediction_time.weekday()

    month = prediction_time.month

    holiday = 1 if weekday >= 5 else 0

    brand = station["properties"].get(
        "brand",
        "Indian Oil"
    )

    poi_level = get_poi_level(station)

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

    queue = int(round(model.predict(features)[0]))

    queue = max(0, min(queue, 35))

    waiting = round(
        queue * service_time / pump_count,
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

    # -----------------------------
    # Save Prediction History
    # -----------------------------

    try:

        save_prediction(

            station_name=station["properties"].get(
                "name",
                "Fuel Station"
            ),

            brand=brand,

            latitude=station["geometry"]["coordinates"][1],

            longitude=station["geometry"]["coordinates"][0],

            prediction_time=str(prediction_time),

            weather=weather,

            queue_length=queue,

            waiting_time=waiting,

            crowd=crowd,

            score=score

        )

    except Exception as e:

        print("Database Error:", e)

    return station