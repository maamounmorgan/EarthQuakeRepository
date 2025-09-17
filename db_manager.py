# db_manager.py

import psycopg2
from config import DB_CONFIG

def get_db_connection():
    """يتصل بقاعدة البيانات ويعيد كائن الاتصال."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

def setup_db_table(conn):
    """ينشئ جدول الزلازل إذا لم يكن موجودًا."""
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS earthquakes (
                id VARCHAR(50) PRIMARY KEY,
                magnitude NUMERIC,
                place VARCHAR(255),
                time TIMESTAMP,
                geom GEOMETRY(Point, 4326)
            );
        """)
        conn.commit()
    print("Database table ready.")

def insert_earthquake_data(conn, earthquake_list):
    """يضيف قائمة من الزلازل إلى الجدول."""
    if not earthquake_list:
        print("No new data to insert.")
        return

    with conn.cursor() as cur:
        for eq in earthquake_list:
            cur.execute("""
                INSERT INTO earthquakes (id, magnitude, place, time, geom)
                VALUES (%s, %s, %s, to_timestamp(%s), ST_SetSRID(ST_MakePoint(%s, %s), 4326))
                ON CONFLICT (id) DO NOTHING;
            """, (eq['id'], eq['mag'], eq['place'], eq['time'] / 1000, eq['lon'], eq['lat']))
        conn.commit()
    print(f"Successfully inserted {len(earthquake_list)} records.")