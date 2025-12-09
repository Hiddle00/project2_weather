import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, classification_report

# 1. 데이터 로드
df = pd.read_csv("reviews_tokenized.csv")
df_emotionset = df
print(df.info())

# 결측행 제거
df_emotionset = df_emotionset.dropna(subset=['tokens'])
df_emotionset = df_emotionset.dropna(subset=['emotion'])
print(df_emotionset.info())

# 텍스트와 라벨
X = df_emotionset['tokens'].astype(str)
y = df_emotionset['emotion']   # 0 / 1 라벨


# 2. 훈련 / 테스트셋 분리
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)


# 3. TF-IDF 벡터화
tfidf = TfidfVectorizer(
    max_features=20000,      # 단어 최대 수 (5만 리뷰 기준 적절)
    ngram_range=(1, 2),      # bigram 포함하면 성능 상승
    min_df=3                 # 3회 미만 등장 단어 제거
)

X_train_tfidf = tfidf.fit_transform(X_train)
X_test_tfidf = tfidf.transform(X_test)


# 4. 모델 학습
lr = LogisticRegression(
    max_iter=300,
    C=1.0,
    class_weight='balanced',   # 데이터 불균형 대비
    n_jobs=-1
)
lr.fit(X_train_tfidf, y_train)


# 5. 예측&평가
y_pred = lr.predict(X_test_tfidf)

print("Accuracy :", accuracy_score(y_test, y_pred))
print("F1 Score :", f1_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))


# 6. 새로운 리뷰 예측 함수
def predict_sentiment(text):
    vec = tfidf.transform([text])
    pred = lr.predict(vec)[0]
    prob = lr.predict_proba(vec)[0]
    return pred, prob

print(predict_sentiment("음식이 정말 맛있고 친절했어요"))
print(predict_sentiment("짜고 서비스가 별로였습니다"))
