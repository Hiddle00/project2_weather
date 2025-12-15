# map/map_service.py
from .map_dao import MapDAO

class MapService:
    """
    map_router와 DAO 사이의 서비스 계층
    """
    def __init__(self):
        self.dao = MapDAO()

    def get_restaurants(self, lat, lon, food_sort=None, limit=30):
        """
        DAO에서 음식점 데이터 가져와서 필요 시 가공 후 반환
        """
        return self.dao.fetch_restaurants(lat, lon, food_sort, limit)
