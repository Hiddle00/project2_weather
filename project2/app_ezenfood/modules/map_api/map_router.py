from flask import Blueprint, request, jsonify
from .map_service import MapService
import os

map_bp = Blueprint("map_bp", __name__)
service = MapService()

WEATHER_KEY = os.getenv("WEATHER_API_KEY")


@map_bp.route("/restaurants", methods=["GET"])
def restaurants():
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)
    food_sort = request.args.get("food_sort", default=None, type=str)
    limit = request.args.get("limit", default=30, type=int)

    if lat is None or lon is None:
        return jsonify({"error": "lat, lon 필요"}), 400

    data = service.get_restaurants(lat, lon, food_sort, limit)
    return jsonify(data)

@map_bp.route("/weather", methods=["GET"])
def weather():
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)
    print("WEATHER API HIT", lat, lon)
    if lat is None or lon is None:
        return jsonify({"error": "lat, lon 필요"}), 400
    data = service.get_weather(lat, lon, WEATHER_KEY)
    return jsonify(data)
