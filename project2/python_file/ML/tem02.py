import pandas as pd
from konlpy.tag import Okt
# 불용어, 토큰화, 벡터화 등

df = pd.read_csv('reviews.csv')
df.info()

okt = Okt()
index = 2
print(df.index)
text = df['clean_review'].iloc[index]
print(text)

# 추출할 품사 정의
target_pos = ['Noun', 'Adjective', 'Verb']

#all = okt.morphs(text, stem=True)
#pos = okt.pos(text, stem=True)
#nouns = okt.nouns(text)
#print(pos)
#print(pos[0][1])


#불용어 집합
#set(집합)을 사용하면 조회성능이 향상
stopwords = set()
with open('stopwords-ko.txt', 'r', encoding='utf-8') as f:   #r : 읽기모드
    for line in f:
        #stopwords.append(line.strip())
        stopwords.add(line.strip())
print(stopwords)
#print(f"불용어 개수: {len(stopwords)}개")
#print(f"일부 불용어: {'나' in stopwords, '너' in stopwords, '우리' in stopwords, '가' in stopwords}")

#startswith()
#기능: 문자열이 괄호 안의 특정 문자열로 시작하는지 검사
#반환: 시작하면 True, 시작하지 않으면 False를 반환


#filtered_word = [word for word in words if word not in stopwords]
extracted_tokens = []
for text in df['clean_review']:
    pos_result = okt.pos(text, stem=True)
    
    print("토큰화 진행률" )
    # 품사 필터링, 불용어 제거
    tokens = [
        word
        for word, tag in pos_result
        if tag in target_pos
        and word not in stopwords # 불용어 제거
    ]
    
    # 토큰들을 공백으로 연결하여 하나의 문자열로 변환
    filtered_word = ' '.join(tokens)  # 처리된 리뷰 문자열
    extracted_tokens.append(filtered_word) # 리스트에 추가

df['tokens'] = extracted_tokens
