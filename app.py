from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


# Receive user's location from JavaScript
@app.route("/location", methods=["POST"])
def location():

    data = request.get_json()

    latitude = data.get("latitude")
    longitude = data.get("longitude")

    print(f"Latitude : {latitude}")
    print(f"Longitude: {longitude}")

    return jsonify({
        "status": "success",
        "latitude": latitude,
        "longitude": longitude
    })


if __name__ == "__main__":
    app.run(debug=True)