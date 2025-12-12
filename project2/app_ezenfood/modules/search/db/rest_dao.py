import pandas as pd
from project2.app_ezenfood.modules.search.db.get_conn import get_conn
import pymysql
"""
    음식점의 카테고리 이름을 카테고리 테이블에서 조회 후
    해당 카테고리에서 id를 꺼내 음식점 테이블에 같이 insert
"""
def rest_insert(df) :
    # MySQL 연결
    conn = get_conn()
    try :
        cursor = conn.cursor()
        
        # sub_category 테이블 전체 조회해서 {sub_name: sub_id} 딕셔너리 생성
        cursor.execute("SELECT sub_id, sub_name FROM sub_category")
        sub_rows = cursor.fetchall()
        sub_dict = {name: sub_id for sub_id, name in sub_rows}
        
        # CSV 데이터에서 sub_id 매핑
        data_to_insert = []
        # iterrows : df 에서 행 단위로 꺼내줌 
        #   반환 형태 : (인덱스, 행(시리즈))
        for idx, row in df.iterrows():
            sub_name = row["상권업종소분류명"]
            sub_id = sub_dict.get(sub_name)  # 존재하지 않으면 None
            
            if sub_id is not None : 
                data_to_insert.append((
                    row["상호명"],       # rest_name
                    sub_id,             # sub_id
                    row["행정동명"],     # rest_dong
                    row["지번주소"],     # rest_old
                    row["도로명주소"],    # rest_addr
                    row["경도"],         # rest_x
                    row["위도"]          # rest_y
                ))
            else:
                print(f"소분류 '{sub_name}'에 해당하는 ID가 없습니다. 건너뜀.")
        
        # executemany로 한 번에 INSERT
        insert_query = """
            INSERT INTO rest 
            (rest_name, sub_id, rest_dong, rest_old, rest_addr, rest_x, rest_y)
            VALUES 
            (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.executemany(insert_query, data_to_insert)
        conn.commit()
        
    except Exception as e :
        print("DB 오류 :", e)
        conn.rollback()
    
    finally :
        cursor.close()
        conn.close()
    
    print("CSV 데이터가 rest 테이블에 저장 완료!")
    
# 음식점 조회
def rest_select(sub_id=None) :
    conn = get_conn()
    cursor = conn.cursor()

    if sub_id:
        sql = "SELECT * FROM rest WHERE sub_id=%s"
        cursor.execute(sql, (sub_id,))
    else:
        sql = "SELECT * FROM rest"
        cursor.execute(sql)

    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows 

