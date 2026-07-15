from flask import Flask

from database.db import initialize_database

from database.feedback import initialize_feedback_database

initialize_feedback_database()

app = Flask(__name__)

initialize_database()

@app.route("/")
def home():
    return "Working"