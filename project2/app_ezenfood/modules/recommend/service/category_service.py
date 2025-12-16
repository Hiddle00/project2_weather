import pandas as pd

from app_ezenfood.modules.recommend.DAO.reco_dao import RecommendDAO
from app_ezenfood.modules.utils.get_conn import get_user_conn
from app_ezenfood.modules.recommend.engine.reco_rest import RestaurantRecommendationEngine

class CategoryRecommendService :
    
    def recommend_categorys(self, args) :
        try:
            input_data = {
                "계절": int(args.get('season', 1)),
                "시": datetime.now().hour,
                "기온": float(args.get('temp', 20.0)),
                "강수량": float(args.get('rain', 0.0)),
                "풍속": float(args.get('wind', 0.0)),
                "습도": float(args.get('humidity', 50.0)),
                "pty": int(args.get('pty', 0))
            }
            result = model_module.recommend_food(input_data)
            return jsonify(result)
        except Exception as e :
            return jsonify({"error": str(e)}), 500