import os, pickle
import pandas as pd
import numpy as np
from app_ezenfood import PKL_DIR

def load_models():
    try:
        with open(os.path.join(PKL_DIR, 'kmeans_model.pkl'), 'rb') as f:
            kmeans = pickle.load(f)
        with open(os.path.join(PKL_DIR, 'scaler_model.pkl'), 'rb') as f:
            scaler = pickle.load(f)
        with open(os.path.join(PKL_DIR, 'cluster_name_map.pkl'), 'rb') as f:
            cluster_map = pickle.load(f)
        print("모델 로드 완료 ✅")
        return kmeans, scaler, cluster_map
    except Exception as e:
        print("모델 로드 오류:", e)
        return None, None, None

KMEANS_MODEL, SCALER_MODEL, CLUSTER_NAME_MAP = load_models()

def recommend_food(input_data):
    if not KMEANS_MODEL:
        return {"error": "모델 없음"}

    # 삼항 연산자 참 if 조건 else 거짓
    effective_rain = 1.0 if input_data['pty'] in [1,2,3,4,5,6,7] else input_data['강수량']
    print("effective_rain : ", effective_rain)
    input_data['강수량'] = effective_rain
    print("input_data['강수량'] : ", input_data['강수량'])

    df = pd.DataFrame([input_data])
    print("df : ", df)
    X_scaled = SCALER_MODEL.transform(df)
    print("X_scaled : ", X_scaled)

    distances = np.linalg.norm(KMEANS_MODEL.cluster_centers_ - X_scaled, axis=1)
    print("distances : ", distances)
    print("--" * 25)
    top3_ids = np.argsort(distances)[:3]
    top3_foods = [CLUSTER_NAME_MAP.get(i, "추천 정보 없음") for i in top3_ids]

    return {
        "top3_clusters": [int(i) for i in top3_ids],
        "recommendations": top3_foods
    }
