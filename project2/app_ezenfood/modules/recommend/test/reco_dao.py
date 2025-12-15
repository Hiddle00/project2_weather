import pandas as pd

class RecommendDAO:

    def __init__(self, conn_factory):
        self.conn_factory = conn_factory

    # 추천에 필요한 음식점 조회
    def fetch_rest_list(self, sub_id: int) -> pd.DataFrame :
        conn = self.conn_factory()
        try :
            cursor = conn.cursor()
            query = """
                select
                    r.rest_id,
                    r.rest_name,
                    r.rest_x,
                    r.rest_y,
                    r.review_count
                from rest r
                where r.sub_id=%s
            """
            # where r.rest_display  = 'Y'
            cursor.execute(query, (sub_id,))
            rows = cursor.fetchall()
            df = pd.DataFrame(rows)
            return df #pd.read_sql(query, conn, params=[sub_id])
        finally :
            conn.close()

    # 리뷰 감정 데이터 조회
    def fetch_reviews(self) -> pd.DataFrame :
        conn = self.conn_factory()
        try :
            cursor = conn.cursor()
            query = """
                select
                    rest_id,
                    review_emotion
                from review
                where review_emotion is not null
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            df = pd.DataFrame(rows)
            return df #pd.read_sql(query, conn)
        finally :
            conn.close()