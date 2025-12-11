from get_conn import get_conn
import json

class SubDAO:
    # staticmethod : 클래스에서 객체는 필요없고 기능만 필요할 때
    # 자바의 static이랑 똑같음
    @staticmethod
    def insert_many(data_list):
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
