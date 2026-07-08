from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

from api.geocoding import search_place
from api.places import nearbyStations

load_dotenv()

app = Flask(__name__)


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
# Crowd Prediction
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

if __name__ == "__main__":
    app.run(debug=True)