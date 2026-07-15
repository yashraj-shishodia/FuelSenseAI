import sqlite3

DB_PATH = "database/history.db"


def get_prediction_history(limit=100):

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM prediction_history

    ORDER BY created_at DESC

    LIMIT ?

    """, (limit,))

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]