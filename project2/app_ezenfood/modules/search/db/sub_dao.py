from project2.app_ezenfood.modules.search.db.get_conn import get_conn
import json
from get_query import get_query
from sentence_transformers import SentenceTransformer

class SubDAO:
    # staticmethod : 클래스에서 객체는 필요없고 기능만 필요할 때
    # 자바의 static이랑 똑같음
    @staticmethod
    def sub_insert(data_list):
        conn = get_conn()
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO sub_category 
                (sub_name, sub_sentence, sub_sentemb, sub_keyword, sub_keyemb)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.executemany(query, data_list)
            conn.commit()
        except Exception as e:
            print("DB Insert Error:", e)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def sub_select(query="돼지고기") :
        try : 
            conn = get_conn()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM sub")
            rows = cursor.fetchall()
        except Exception as e :
            print("DB Insert Error:", e)
            conn.rollback()
        finally :
            cursor.close()
            conn.close()
        model = SentenceTransformer("snunlp/KR-SBERT-V40K-klueNLI-augSTS")
        sort_list = get_query(query, rows, model)
        return sort_list  # 리스트 그대로 반환
