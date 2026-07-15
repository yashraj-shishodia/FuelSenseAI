import sqlite3
import os

DB_PATH = "database/history.db"


def get_connection():

    os.makedirs("database", exist_ok=True)

    return sqlite3.connect(DB_PATH)


def initialize_database():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS prediction_history(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        station_name TEXT,

        brand TEXT,

        latitude REAL,

        longitude REAL,

        prediction_time TEXT,

        weather TEXT,

        queue_length INTEGER,

        waiting_time REAL,

        crowd TEXT,

        score INTEGER,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    conn.commit()

    conn.close()


def save_prediction(

    station_name,

    brand,

    latitude,

    longitude,

    prediction_time,

    weather,

    queue_length,

    waiting_time,

    crowd,

    score

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO prediction_history(

        station_name,

        brand,

        latitude,

        longitude,

        prediction_time,

        weather,

        queue_length,

        waiting_time,

        crowd,

        score

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

        waiting_time,

        crowd,

        score

    ))

    conn.commit()

    conn.close()