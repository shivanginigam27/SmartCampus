
import os
import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error

load_dotenv()

def get_connection():
    try:
        return mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME", "SmartCampus")
        )
    except Error as e:
        print("Database connection error:", e)
        return None


def get_events():
    conn = get_connection()

    if not conn:
        return []

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT event_id, title, category, description,
                   event_date, venue, capacity
            FROM events
            WHERE event_date IS NULL OR event_date >= CURDATE()
            ORDER BY event_date
        """)
        return cursor.fetchall()

    except Error as e:
        print("Error fetching events:", e)
        return []

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
