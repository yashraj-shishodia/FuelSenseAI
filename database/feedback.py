import sqlite3
import os

DB_PATH = "database/feedback.db"


def get_connection():

    os.makedirs("database", exist_ok=True)

    return sqlite3.connect(DB_PATH)


def initialize_feedback_database():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS verified_predictions(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        station_name TEXT,

        brand TEXT,

        latitude REAL,

        longitude REAL,

        prediction_time TEXT,

        weather TEXT,

        queue_length INTEGER,

        predicted_waiting REAL,

        actual_waiting REAL,

        rating INTEGER,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    conn.commit()

    conn.close()


def save_feedback(

    station_name,

    brand,

    latitude,

    longitude,

    prediction_time,

    weather,

    queue_length,

    predicted_waiting,

    actual_waiting,

    rating

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO verified_predictions(

        station_name,

        brand,

        latitude,

        longitude,

        prediction_time,

        weather,

        queue_length,

        predicted_waiting,

        actual_waiting,

        rating

    )

    VALUES(?,?,?,?,?,?,?,?,?,?)

    """,

    (

        station_name,

        brand,

        latitude,

        longitude,

        prediction_time,

        weather,

        queue_length,

        predicted_waiting,

        actual_waiting,

        rating

    ))

    conn.commit()

    conn.close()