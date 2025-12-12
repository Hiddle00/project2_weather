import pymysql

class RecommendDao :
    def __init__(self) :
        self.conn = pymysql.connect(
            host="192.168.60.179",
            user="최연흠",
            password="ezen",
            database="ezeneats",
            cursorclass=pymysql.cursors.DictCursor
        )
        #쿼리실행 객체
        self.cursor = self.conn.cursor()

    def get_conn() :
        return pymysql.connect(
            host="192.168.60.179",
            user="최연흠",
            password="ezen",
            database="ezeneats",
            charset="utf8mb4"
        )

    def notes(self) :
        sql = "select * from notes"
        self.cursor.execute(sql)
        notes = self.cursor.fetchall()  #결과 : [{}, {}]  /  없음 : []
        self.close()
        return notes

    def insert() :
        sql = "insert into review (rest_id, review_)"
    
    
    #연결종료 함수
    def close_conn(self) :
        self.cursor.close()
        self.conn.close()
