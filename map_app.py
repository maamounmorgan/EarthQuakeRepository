# map_app.py (نسخة جديدة لإنشاء خريطة HTML)

import folium
import psycopg2
from config import DB_CONFIG


def create_earthquake_map():
    """
    يتصل بقاعدة البيانات ويستخدم Folium لإنشاء خريطة HTML
    تعرض مواقع الزلازل.
    """
    print("Connecting to the database to create an interactive HTML map...")

    # 1. الاتصال بقاعدة البيانات
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

    # 2. استخراج البيانات من PostGIS
    cur.execute("SELECT magnitude, ST_X(geom), ST_Y(geom) FROM earthquakes;")
    earthquakes = cur.fetchall()

    cur.close()
    conn.close()

    if not earthquakes:
        print("No earthquake data found in the database. Please run pipeline.py first.")
        return None

    # 3. إنشاء خريطة Folium
    m = folium.Map(location=[20, 0], zoom_start=2)

    # 4. إضافة علامات على الخريطة
    for mag, lon, lat in earthquakes:
        # تحويل نوع البيانات من Decimal إلى float
        mag_float = float(mag)

        # تخصيص لون العلامة حسب شدة الزلزال
        if mag_float >= 7.0:
            color = 'red'
        elif mag_float >= 5.0:
            color = 'orange'
        else:
            color = 'blue'

        folium.CircleMarker(
            location=[lat, lon],
            radius=mag_float * 2,  # حجم العلامة يتناسب مع الشدة
            popup=f"Magnitude: {mag_float}",
            color=color,
            fill=True,
            fill_color=color
        ).add_to(m)

    # 5. حفظ الخريطة كملف HTML
    output_file = "earthquake_map.html"
    m.save(output_file)
    print(f"Interactive map saved to {output_file}. Open this file in your browser.")
    return output_file


if __name__ == "__main__":
    create_earthquake_map()