# map/map_router.py
from flask import Blueprint, request, jsonify
from .map_service import MapService

# 블루프린트 정의
map_bp = Blueprint("map_bp", __name__)
service = MapService()

@map_bp.route("/restaurants", methods=["GET"])
def restaurants():
    """
    GET /api/map/restaurants?lat=...&lon=...&food_sort=...&limit=...
    HTML/JS에서 fetch로 호출
    """
    # 요청 파라미터 읽기
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)
    food_sort = request.args.get("food_sort", default=None, type=str)
    limit = request.args.get("limit", default=30, type=int)

    # 필수 파라미터 검증
    if lat is None or lon is None:
        return jsonify({"error": "lat, lon 필요"}), 400

    # Service 호출 → DAO에서 데이터 가져옴
    data = service.get_restaurants(lat, lon, food_sort, limit)
    return jsonify(data)
