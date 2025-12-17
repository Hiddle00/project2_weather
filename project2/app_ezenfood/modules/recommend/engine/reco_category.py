import os, pickle
import pandas as pd
import numpy as np
from app_ezenfood import PKL_DIR

class CategoryRecommendEngine :
    def __init__(self) -> None :
        self.KMEANS_MODEL, self.SCALER_MODEL, self.CLUSTER_NAME_MAP = self._load_models()
        if self.KMEANS_MODEL is None:
            raise RuntimeError("카테고리 추천 모델 로드 실패")
        
    def _load_models(self) :
        try :
            with open(os.path.join(PKL_DIR, 'kmeans_model.pkl'), 'rb') as f :
                kmeans = pickle.load(f)
            with open(os.path.join(PKL_DIR, 'scaler_model.pkl'), 'rb') as f :
                scaler = pickle.load(f)
            with open(os.path.join(PKL_DIR, 'cluster_name_map.pkl'), 'rb') as f :
                cluster_map = pickle.load(f)
            print("모델 로드 완료 ✅")
            return kmeans, scaler, cluster_map
        except Exception as e :
            print("모델 로드 오류:", e)
            return None, None, None


    def recommend_food(self, features : dict) -> dict :
        features = features.copy()

        pty = features.get('pty', 0)
        rain = features.get('강수량', 0)

        # 삼항 연산자 참 if 조건 else 거짓
        features['강수량'] = 1.0 if pty in [1,2,3,4,5,6,7] else rain
        print("effective_rain : ", features['강수량'])

        df = pd.DataFrame([features])
        print("df : ", df)
        X_scaled = self.SCALER_MODEL.transform(df)
        print("X_scaled : ", X_scaled)

        # 중심점 거리 계산
        distances = np.linalg.norm(self.KMEANS_MODEL.cluster_centers_ - X_scaled, axis=1)
        print("distances : ", distances)
        print("--" * 25)
        top3_ids = np.argsort(distances)[:3]
        top3_foods = [self.CLUSTER_NAME_MAP.get(int(i), "추천 정보 없음") for i in top3_ids]

        return {
            "top3_clusters": [int(i) for i in top3_ids],
            "recommendations": top3_foods
        }
