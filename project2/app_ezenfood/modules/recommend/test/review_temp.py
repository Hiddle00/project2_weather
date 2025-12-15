import pandas as pd
from app_ezenfood import CSV_DIR


review_df = pd.read_csv(CSV_DIR / "reviews_repredicted.csv")


print(review_df.isna().sum())