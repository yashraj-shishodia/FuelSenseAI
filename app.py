import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

from flask import Flask, render_template, request, jsonify

from api.geocoding import search_place
from api.places import nearbyStations

from database.db import initialize_database
from database.feedback import (
    initialize_feedback_database,
    save_feedback
)

app = Flask(__name__)
PORT = int(os.environ.get("PORT", 5000))

initialize_database()
initialize_feedback_database()


# -----------------------------------
# Home
# -----------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------------
# Browser Location
# -----------------------------------

@app.route("/location", methods=["POST"])
def location():

    data = request.get_json()

    latitude = data.get("latitude")
    longitude = data.get("longitude")

    return jsonify({

        "status": "success",

        "latitude": latitude,

        "longitude": longitude

    })


# -----------------------------------
# Search Location
# -----------------------------------

@app.route("/search", methods=["POST"])
def search():

    data = request.get_json()

    location = data["location"]

    result = search_place(location)

    return jsonify(result)


# -----------------------------------
# Station Prediction
# -----------------------------------

@app.route("/stations", methods=["POST"])
def stations():

    data = request.get_json()

    latitude = data["latitude"]
    longitude = data["longitude"]

    prediction_time = data.get("prediction_time")

    result = nearbyStations(

        latitude,

        longitude,

        prediction_time

    )

    return jsonify(result)


# -----------------------------------
# Save User Feedback
# -----------------------------------

@app.route("/feedback", methods=["POST"])
def feedback():

    try:

        data = request.get_json()

        save_feedback(

            station_name=data["station_name"],

            brand=data["brand"],

            latitude=data["latitude"],

            longitude=data["longitude"],

            prediction_time=data["prediction_time"],

            weather=data["weather"],

            queue_length=data["queue_length"],

            predicted_waiting=data["predicted_waiting"],

            actual_waiting=data["actual_waiting"],

            rating=data["rating"]

        )

        return jsonify({

            "success": True

        })

    except Exception as e:

        print(e)

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# -----------------------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=PORT,
        debug=(os.environ.get("FLASK_DEBUG", "false").lower() == "true")
    )