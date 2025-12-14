import pandas as pd
from reco_rest import RestaurantRecommendationEngine
engine = RestaurantRecommendationEngine()

df_rest  = pd.read_csv("../../../csv/filter_list.csv")
df_review  = pd.read_csv("../../../csv/reviews_repredicted.csv")

print(df_rest.info())
print(df_review.info())

df_rest_map = (
    df_review[['rest_code', 'rest', 'review_count']]
    .drop_duplicates(subset='rest').rename(columns={'rest':'상호명'})
)
print(df_rest_map.info())

df_rest = df_rest.merge(
    df_rest_map,
    on='상호명',
    how='left'
)
print(df_rest.info())

result = engine.recommend_top_n(
    user_lat = 35.8150,
    user_lon = 127.1500,
    rest_df  = df_rest,   # DAO에서 가져온 DF라고 가정
    top_n    = 5
)

print(result[['rest_name', 'final_score', 'distance_km']])