from flask import Blueprint, request, jsonify
from .service import search_recommendation

search_bp = Blueprint("search", __name__, url_prefix="/search")

@search_bp.route("/", methods=["GET"])
def search():
    query = request.args.get("q")
    
    if not query:
        return jsonify({"error": "검색어 없음"}), 400
    
    result = search_recommendation(query)

    return jsonify(result)
