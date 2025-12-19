import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from matplotlib import rc

# ------------------------------
# 0. 기본 설정 및 경로
# ------------------------------
rc("font", family="gulim")
plt.rcParams['axes.unicode_minus'] = False 

CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__)) 
BASE_DIR = os.path.dirname(CURRENT_FILE_DIR) 
DATA_DIR = os.path.join(BASE_DIR, 'data')

# ------------------------------
# 1. 데이터 로드 및 전처리 (X_scaled 생성)
# ------------------------------
file_path = r"D:\project2\project2\data\기타\날씨데이터.csv"
weather = pd.read_csv(file_path)

weather['시간'] = pd.to_datetime(weather['시간'])
weather['시'] = weather['시간'].dt.hour

def get_season(month):
    if month in [3, 4, 5]: return 1    # 봄
    elif month in [6, 7, 8]: return 2  # 여름
    elif month in [9, 10, 11]: return 3 # 가을
    else: return 4                     # 겨울
    
weather['계절'] = weather['시간'].dt.month.apply(get_season)

features = ["계절", "시", "기온", "강수량", "풍속", "습도"]
X = weather[features].fillna(0)

# 필수: X_scaled 생성
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 필수: kmeans 모델 및 클러스터 할당
kmeans = KMeans(n_clusters=20, random_state=80, n_init=10)
weather["cluster"] = kmeans.fit_predict(X_scaled)

# ------------------------------
# 2. 음식 이름 맵핑 딕셔너리
# ------------------------------
cluster_name_map = {
    0: '토스트·샌드위치', 1: '백반·한정식', 2: '냉·밀면', 3: '국·탕', 4: '국수',
    5: '곱창', 6: '소고기', 7: '일식 돈가스·덮밥', 8: '빵', 9: '분식',
    10: '닭요리', 11: '마라탕', 12: '해산물 구이·찜', 13: '경양식', 14: '베트남식',
    15: '횟집', 16: '회·초밥', 17: '일식 면', 18: '전·부침개', 19: '돼지고기'
}

# ------------------------------
# 3. PCA 차원 축소 및 시각화
# ------------------------------
pca = PCA(n_components=2)
weather_pca = pca.fit_transform(X_scaled)

plt.figure(figsize=(12, 10))
cmap = plt.cm.get_cmap('tab20', 20)

for i in range(20):
    indices = weather["cluster"] == i
    label = cluster_name_map.get(i, f'Cluster {i}')
    plt.scatter(weather_pca[indices, 0], weather_pca[indices, 1], 
                c=[cmap(i)], s=10, alpha=0.6, label=label)

# Centroids 표시
centers_pca = pca.transform(kmeans.cluster_centers_)
plt.scatter(centers_pca[:, 0], centers_pca[:, 1], c='red', s=200, marker='X', label='Centroids')

plt.title("날씨 데이터 군집 분석 시각화 (PCA)")
plt.xlabel("시간/대기 활동성 (PC1)")
plt.ylabel("온도/계절 상태 (PC2)")
plt.legend(title='음식 클러스터', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()

# 결과 저장
save_path = r"D:\project2\project2\data\기타\weather_clusters_pca_food.png"
plt.savefig(save_path, dpi=300)
plt.show()

# ------------------------------
# 4. 날씨 변수 간 상관관계 시각화 (Only Matplotlib)
# ------------------------------
plt.figure(figsize=(10, 8))

# 상관계수 계산
corr_matrix = weather[features].corr()

# 히트맵 그리기
img = plt.imshow(corr_matrix, cmap='RdBu_r', vmin=-1, vmax=1)

# 컬러바 추가
cbar = plt.colorbar(img, fraction=0.046, pad=0.04)
cbar.set_label('상관계수 (Correlation)', rotation=270, labelpad=15)

# 축 설정
plt.xticks(range(len(features)), features, rotation=45)
plt.yticks(range(len(features)), features)

# 각 칸에 수치(텍스트) 표시
for i in range(len(features)):
    for j in range(len(features)):
        text_color = 'white' if abs(corr_matrix.iloc[i, j]) > 0.5 else 'black'
        plt.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',  ha='center', va='center', color=text_color, fontweight='bold')

plt.title("날씨 변수 간 상관관계 히트맵", pad=20, fontsize=15)
plt.tight_layout()

# 이미지 저장
corr_save_path = r"D:\project2\project2\data\기타\weather_correlation_matplotlib.png"
plt.savefig(corr_save_path, dpi=300)
plt.show()

print(f"상관관계 히트맵 저장 완료: {corr_save_path}")