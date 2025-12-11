import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # test.py 있는 폴더
csv_path = os.path.join(BASE_DIR, '..', 'csv', 'filter_list.csv')  # 상대경로 수정

df = pd.read_csv(csv_path)
print(df.info())


print("현재 작업 디렉터리:", os.getcwd())