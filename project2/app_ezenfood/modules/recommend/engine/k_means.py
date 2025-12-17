import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
from matplotlib import rc
import pickle 
import os # os 라이브러리 추가

# 현재 파일(k_means.py)의 절대 경로를 얻습니다. (Exodia/backend/models/k_means.py)
CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__)) 

# BASE_DIR을 'backend' 폴더로 지정하기 위해 상위 디렉토리를 사용합니다.
# CURRENT_FILE_DIR의 부모 폴더, 즉 'backend' 폴더 경로를 BASE_DIR로 설정합니다.
BASE_DIR = os.path.dirname(CURRENT_FILE_DIR) 

# DATA_DIR은 'backend' 폴더 아래의 'data' 폴더입니다.
DATA_DIR = os.path.join(BASE_DIR, 'data') # ✨ 이제 .../backend/data가 됩니다.

# ------------------------------
# 0. 한글 폰트 설정 및 기본 설정
# ------------------------------
rc("font", family="gulim")
plt.rcParams['axes.unicode_minus'] = False 

# ------------------------------
# 1. 데이터 읽기 및 전처리
# ------------------------------
# 파일경로 
# weatherdata2.csv 파일은 backend/data 폴더에 있다고 가정
file_path = os.path.join(DATA_DIR, "weatherdata2.csv")
try:
    weather = pd.read_csv(file_path)
except FileNotFoundError:
    print(f"❌ 파일 위치 오류: {file_path}. 경로를 확인해주세요.")
    exit()

# 학습 특성 설정
features = ["계절","시","기온", "강수량", "풍속", "습도"] 

# Nan값 채우기: 0으로 대체
X = weather[features].fillna(0) 

# 데이터 스케일링
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ------------------------------
# 2. KMeans 학습
# ------------------------------
# 군집 수 설정 (K=20)
kmeans = KMeans(n_clusters=20, random_state=80, n_init=10)
kmeans.fit(X_scaled)
weather["cluster"] = kmeans.labels_

# **********************************************
# 클러스터 ID 바꿔줄 음식 소분류 딕셔너리
# **********************************************
cluster_name_map = {
    0: '국/탕/찌개류',
    1: '닭/오리고기 구이/찜',
    2: '마라탕/훠궈',
    3: '곱창 전골/구이',
    4: '소고기 구이/찜',
    5: '돼지고기 구이/찜',
    6: '해산물 구이/찜',
    7: '냉면/밀면',
    8: '백반/한정식',
    9: '김밥/만두/분식',
    10: '국수/칼국수',
    11: '일식 면 요리',
    12: '일식 카레/돈가스/덮밥',
    13: '경양식',
    14: '베트남식 전문',
    15: '횟집',
    16: '빵/도넛',
    17: '일식 회/초밥',
    18: '토스트/샌드위치/샐러드',
    19: '전/부침개'
}

# 맵핑을 데이터프레임에 새로운 열로 저장
weather["cluster_name"] = weather["cluster"].map(cluster_name_map)


pd.set_option('display.max_rows', None)     # 모든 행 표시
pd.set_option('display.max_columns', None) # 모든 열 표시

# 군집 중심점 확인
centers_df = pd.DataFrame(
    scaler.inverse_transform(kmeans.cluster_centers_), 
    columns=features
)

print("\n[군집 중심점 (K=20)]")
print(centers_df)

# 실루엣 점수 계산
if len(weather) > 20:
    score = silhouette_score(X_scaled, kmeans.labels_)
    print(f"\n[실루엣 점수]: {score:.20f}") 


# ------------------------------
# ✨ 3. 학습된 모델 및 관련 객체 저장 (backend/data 폴더에 저장)
# ------------------------------

# 저장할 파일 경로 설정 (backend/data 폴더 내에 저장)
kmeans_save_path = os.path.join(DATA_DIR, "kmeans_model.pkl")
scaler_save_path = os.path.join(DATA_DIR, "scaler_model.pkl")
map_save_path = os.path.join(DATA_DIR, "cluster_name_map.pkl") 

try:
    ### 1. KMeans 모델 저장
    with open(kmeans_save_path, 'wb') as file:
        pickle.dump(kmeans, file)
    print(f"✅ KMeans 모델 저장 완료: {kmeans_save_path}")

    ### 2. StandardScaler 객체 저장
    with open(scaler_save_path, 'wb') as file:
        pickle.dump(scaler, file)
    print(f"✅ Scaler 객체 저장 완료: {scaler_save_path}")

    ### 3. 클러스터-음식 맵핑 딕셔너리 저장
    with open(map_save_path, 'wb') as file:
        pickle.dump(cluster_name_map, file)
    print(f"✅ Cluster 맵핑 딕셔너리 저장 완료: {map_save_path}")

except Exception as e:
    print(f"❌ 모델 저장 중 오류 발생: {e}")


# ------------------------------
# 시각화 (PCA Scatter Plot)
# ------------------------------

# 몇 차원으로 볼것인가?
pca = PCA(n_components=2)
# 스케일링된 X_scaled를 2차원으로 축소합니다.
weather_pca = pca.fit_transform(X_scaled) 

plt.figure(figsize=(10, 8))

# K-Means 군집의 개수
n_clusters = kmeans.n_clusters

cmap = plt.cm.get_cmap('tab20', n_clusters) # 20개 색상을 위해 tab20 사용

# 1. 데이터 포인트를 군집 ID에 따라 색칠하여 그립니다. (각 군집별로 개별 scatter 호출)
for i in range(n_clusters):
    indices = weather["cluster"] == i
    
    # 범례(label)를 숫자 ID 대신 음식 이름으로 변경
    cluster_label = cluster_name_map.get(i, f'Cluster {i}')
    
    plt.scatter(
        weather_pca[indices, 0], 
        weather_pca[indices, 1], 
        c=[cmap(i)], 
        s=15,
        alpha=0.6,
        label=cluster_label # 새로운 음식 이름 사용
    )


# 2. 군집 중심점(Centroids)을 빨간색 'X' 마크로 그립니다.
centers_pca = pca.transform(kmeans.cluster_centers_)
plt.scatter(
centers_pca[:, 0], 
centers_pca[:, 1], 
c='red', 
s=200, 
marker='X', 
edgecolors='black', 
label='Centroids' 
) 


# ------------------------------
# 2-1. PCA 주성분 적재값 계산
# ------------------------------.
loadings = pd.DataFrame(
    pca.components_.T,
    columns=[f'PC{i}' for i in range(1, pca.n_components_+1)],
    index=features # 현재 컬럼 ["계절","시","기온", "강수량", "풍속", "습도"]
)
print("\n[PCA 주성분 적재값 (Loadings)]")
print(loadings.abs().sort_values(by='PC1', ascending=False))
# ------------------------------

plt.title("날씨 데이터 군집 분석 시각화 (PCA) 음식 이름")
plt.xlabel("시간/대기 활동성")
plt.ylabel("온도/계절 상태")                                                              

# 4. Centroids에 대한 범례를 표시합니다.
plt.legend(title='음식 클러스터') 

plt.grid(True, alpha=0.3)

# ------------------------------
# 시각화 저장
# ------------------------------
save_path = os.path.join(DATA_DIR, "weather_clusters_pca_음식.png")
plt.savefig(save_path, dpi=300, bbox_inches='tight') 
print(f"\n[시각화 저장 완료]: {save_path}")

plt.show()