from flask import Flask

from database.db import initialize_database

app = Flask(__name__)

initialize_database()

@app.route("/")
def home():
    return "Working"