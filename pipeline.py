# pipeline.py

import requests
import time
import schedule
from shapely.geometry import Point
from db_manager import get_db_connection, setup_db_table, insert_earthquake_data
from config import API_URL


def extract_transform_load():
    """الخطوات الرئيسية لخط الأنابيب: استخراج، تحويل، تحميل."""
    print("Starting data pipeline...")

    # 1. استخراج البيانات (Extract)
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # رفع خطأ إذا فشل الطلب
        geojson_data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data from API: {e}")
        return

    # 2. تحويل البيانات (Transform)
    earthquakes_to_load = []
    for feature in geojson_data['features']:
        properties = feature['properties']
        geometry = feature['geometry']

        # استخدام Shapely للتحقق من صحة البيانات الجغرافية
        if geometry['type'] == 'Point':
            point = Point(geometry['coordinates'])
            if point.is_valid:
                earthquakes_to_load.append({
                    'id': feature['id'],
                    'mag': properties['mag'],
                    'place': properties['place'],
                    'time': properties['time'],
                    'lon': point.x,
                    'lat': point.y
                })
    print(f"Found {len(earthquakes_to_load)} valid earthquake records.")

    # 3. تحميل البيانات (Load)
    conn = get_db_connection()
    if conn:
        setup_db_table(conn)
        insert_earthquake_data(conn, earthquakes_to_load)
        conn.close()


def main():
    """جدولة مهمة خط الأنابيب."""
    print("Scheduling earthquake data pipeline to run daily...")
    schedule.every().day.at("01:00").do(extract_transform_load)

    # تشغيل المهمة فورًا عند بدء البرنامج
    extract_transform_load()

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()