import re
import pandas as pd
from konlpy.tag import Okt

df = pd.read_csv('../../data/01.원본데이터/리뷰/review_list3.csv')
print(df.info())
print(df.head())
print("--" * 25)

# 정규화 함수
def normalize(text):
    # 한글, 숫자, 공백만 남기고 나머지 제거
    text = re.sub(r'[^ㄱ-ㅎ가-힣0-9\s]', '', text)

    # 반복 문자 축소 (예: ㅋㅋㅋㅋ → ㅋㅋ)
    text = re.sub(r'([ㄱ-ㅎ])\1{2,}', r'\1\1', text)

    # 공백 정리
    text = re.sub(r'\s+', ' ', text).strip()

    return text

pattern = r'^[가-힣0-9]+$'
#.apply(lambda x: bool(re.search(r'[^가-힣0-9]', x)))

df = df[df['rest'].astype(str).str.match(pattern)]
clean_review = ~df['review'].astype(str).str.match(pattern)

#print(df['clean_review'].sum())
#print(df[df['clean_review']])
print(clean_review.sum())


df['rest'] = df['rest'].astype(str)
df['clean_review'] = df['review'].apply(normalize).astype(str)
print(df.info())

okt = Okt()

#df['clean_review']

#df.to_csv('../../data/04.전처리_리뷰/list_clean3.csv', index=False)
#df.to_csv('../../data/04.전처리_리뷰/list_clean3_utf8.csv', encoding='utf-8-sig', index=False)

