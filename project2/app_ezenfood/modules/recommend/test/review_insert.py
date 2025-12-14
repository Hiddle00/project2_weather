from sqlalchemy import create_engine

user = "root"
password = "ezen"
localhost = "localhost"
db_name = "ezeneats"

engine = create_engine(
    f"mysql+pymysql://{user}:{password}@{localhost}:3306/{db_name}"
)
print(engine)

df_rest.to_sql(
    name='review',      # 테이블 이름
    con=engine,         # DB 연결
    if_exists='append', # append / replace / fail
    index=False
)
"""
append      기존 테이블에 데이터 추가
replace     테이블 삭제 후 다시 생성
fail        테이블 있으면 에러

INSERT INTO rest
(rest_id, sub_id, rest_name, rest_x, rest_y, ...)
VALUES
(17387852, 3, '진안숯불구이', 127.123, 35.456, ...),
...

sub_id 필수
"""