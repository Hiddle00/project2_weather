# map/map_dao.py
import mysql.connector

class MapDAO:
    """
    음식점 데이터 접근 계층
    MySQL DB 연결 버전
    """
    def __init__(self):
        self.use_db = True
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ezen",
            database="whateatnow",
            charset="utf8mb4"
        )
        self.cursor = self.conn.cursor(dictionary=True)

    def fetch_restaurants(self, lat, lon, food_sort=None, limit=30):
        """
        lat/lon 기준 근처 음식점 데이터 반환
        """
        if not self.use_db:
            # 더미 데이터
            sample = []
            for i in range(1, limit+1):
                sample.append({
                    "r_name": f"맛집{i}",
                    "x": lon + 0.001 * i,
                    "y": lat + 0.001 * i,
                    "sort": food_sort or "한식",
                    "addr": f"테스트 주소 {i}",
                    "distance": 100 * i
                })
            return sample

        # 실제 DB 조회
        sql = "SELECT r_name, x, y, sort, addr, distance FROM restaurants WHERE 1=1"
        params = []

        if food_sort:
            sql += " AND sort = %s"
            params.append(food_sort)

        # 거리 계산 (간단한 예: lat/lon 차이 기준)
        sql += " ORDER BY ABS(y - %s) + ABS(x - %s) LIMIT %s"
        params.extend([lat, lon, limit])

        self.cursor.execute(sql, params)
        result = self.cursor.fetchall()
        return result
