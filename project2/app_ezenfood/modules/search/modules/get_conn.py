import pymysql

def get_conn() :
    return pymysql.connect(
        host="192.168.60.179",
        user="유재욱",
        password="ezen",
        database="ezeneats",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )
