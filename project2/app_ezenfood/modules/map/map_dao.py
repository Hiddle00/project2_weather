# map/map_dao.py
class MapDAO:
    """
    음식점 데이터 접근 계층
    실제 DB가 없으면 더미 데이터 반환
    """
    def __init__(self):
        # 실제 DB 없으므로 더미 사용
        self.use_db = False

    def fetch_restaurants(self, lat, lon, food_sort=None, limit=30):
        """
        lat/lon 기준 근처 음식점 데이터 반환
        """
        if self.use_db:
            # 실제 DB 쿼리 구현 가능
            pass
        else:
            # 더미 데이터
            sample = []
            for i in range(1, limit+1):
                sample.append({
                    "r_name": f"맛집{i}",
                    "x": lon + 0.001 * i,  # 경도
                    "y": lat + 0.001 * i,  # 위도
                    "sort": food_sort or "한식",
                    "addr": f"테스트 주소 {i}",
                    "distance": 100 * i  # JS에서 거리 표시용
                })
            return sample
