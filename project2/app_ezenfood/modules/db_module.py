import mysql.connector
from .distance_module import haversine

# 디비 연결 모듈   
DB_CONFIG = {
    'user': 'root',
    'password': 'ezen',
    'host': '127.0.0.1',
    'database': 'whateatnow'
}

def get_nearby_restaurants(lat, lon, offset=0, limit=10, food_sort=None):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)

    where_clause = "WHERE 1=1"
    params = []

    if food_sort:
        where_clause += " AND sort LIKE %s"
        params.append(f"%{food_sort}%")

    haversine_formula = f"""
    (6371 * acos(
        cos(radians(%s)) * cos(radians(y)) 
        * cos(radians(x) - radians(%s)) 
        + sin(radians(%s)) * sin(radians(y))
    ))
    """
    query = f"""
        SELECT r_name, y, x, dong, sort, addr, ads,
               {haversine_formula} AS distance_km
        FROM map
        {where_clause}
        HAVING distance_km <= 1
        ORDER BY distance_km ASC
        LIMIT %s OFFSET %s
    """
    query_params = [lat, lon, lat] + params + [limit, offset]

    cursor.execute(query, query_params)
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    restaurants = [
        {
            "r_name": r["r_name"],
            "y": r["y"],
            "x": r["x"],
            "dong": r["dong"],
            "sort": r["sort"],
            "addr": r["addr"],
            "ads": r["ads"],
            "distance": round(r["distance_km"] * 1000),
        }
        for r in results
    ]
    return restaurants
