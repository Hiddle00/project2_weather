from flask import Blueprint, request, jsonify
from app_ezenfood.modules.recommend.reco_service import RestaurantRecommendService
from app_ezenfood.modules.recommend.review_service import ReviewService
from app_ezenfood.modules.recommend.review_dao import ReviewDAO
from app_ezenfood.modules.utils.get_conn import get_root_conn
import pandas as pd

recommend_bp = Blueprint(
    "recommend",
    __name__,
    url_prefix="/api/recommend"
)

service = RestaurantRecommendService()

# 음식점 추천 API
@recommend_bp.route("/restaurants", methods=["GET"])
def recommend_restaurants():
    """
    필수 파라미터:
      - sub_id
      - lat
      - lon
    선택:
      - max_distance_km
      - top_n
    """

    try:
        sub_id = int(request.args.get("sub_id"))
        user_lat = float(request.args.get("lat"))
        user_lon = float(request.args.get("lon"))
    except (TypeError, ValueError):
        return jsonify({
            "error": "sub_id, lat, lon은 필수이며 숫자여야 합니다."
        }), 400

    max_distance_km = float(request.args.get("distance", 1.0))
    top_n = int(request.args.get("top_n", 5))

    result_df = service.recommend_restaurants(
        sub_id=sub_id,
        user_lat=user_lat,
        user_lon=user_lon,
        max_distance_km=max_distance_km,
        top_n=top_n
    )

    return jsonify({
        "count": len(result_df),
        "restaurants": result_df.to_dict(orient="records")
    })
    
# 리뷰 insert API
@recommend_bp.route("/reviews/import", methods=["POST"])
def import_reviews():

    review_service = ReviewService()
    review_dao = ReviewDAO(get_root_conn)

    df = pd.read_csv("app_ezenfood/csv/reviews_repredicted.csv")
    mapped_df = review_service.attach_rest_id(df)

    success_df = mapped_df[mapped_df['rest_id'].notna()]
    review_dao.insert_reviews(success_df)

    return jsonify({
        "inserted": len(success_df),
        "failed": len(mapped_df) - len(success_df)
    })