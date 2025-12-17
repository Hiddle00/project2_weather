from .map_dao import MapDAO
import requests
from datetime import datetime, timedelta
import math

class MapService:
    def __init__(self):
        self.dao = MapDAO()

    # ==========================
    # 음식점 조회
    # ==========================
    def get_restaurants(self, lat, lon, food_sort=None, limit=30):
        """
        MapDAO.fetch_restaurants 호출
        lat/lon 기준 근처 음식점 반환
        DB 조회 실패 시 콘솔에 에러 로그
        """
        try:
            return self.dao.fetch_restaurants(lat, lon, food_sort, limit)
        except Exception as e:
            print(f"[MapService] DB 조회 실패: {e}")
            return []  # 실패 시 빈 리스트 반환


    # ==========================
    # 기상청 좌표 변환
    # ==========================
    def dfs_xy_conv(self, lat, lon):
        RE, GRID = 6371.00877, 5.0
        SLAT1, SLAT2 = 30.0, 60.0
        OLON, OLAT = 126.0, 38.0
        XO, YO = 43, 136
        DEGRAD = math.pi / 180.0

        re = RE / GRID
        slat1 = SLAT1 * DEGRAD
        slat2 = SLAT2 * DEGRAD
        olon = OLON * DEGRAD
        olat = OLAT * DEGRAD

        sn = math.log(math.cos(slat1) / math.cos(slat2)) / \
             math.log(math.tan(math.pi * 0.25 + slat2 * 0.5) / math.tan(math.pi * 0.25 + slat1 * 0.5))
        sf = math.pow(math.tan(math.pi * 0.25 + slat1 * 0.5), sn) * math.cos(slat1) / sn
        ro = re * sf / math.pow(math.tan(math.pi * 0.25 + olat * 0.5), sn)
        ra = re * sf / math.pow(math.tan(math.pi * 0.25 + lat * DEGRAD * 0.5), sn)
        theta = lon * DEGRAD - olon
        if theta > math.pi: theta -= 2.0 * math.pi
        if theta < -math.pi: theta += 2.0 * math.pi
        theta *= sn
        x = math.floor(ra * math.sin(theta) + XO + 0.5)
        y = math.floor(ro - ra * math.cos(theta) + YO + 0.5)
        return {"x": x, "y": y}

    # ==========================
    # 기상청 날씨 데이터 가져오기
    # ==========================
    def get_weather(self, lat, lon, service_key):
        coords = self.dfs_xy_conv(lat, lon)
        nx, ny = coords["x"], coords["y"]

        """
            기상청 예보 API는 매 정시(00분)에 데이터가 생성되지만,
            실제로 API에서 조회 가능해지는 건 약 40분 이후 
            그래서 현재 시간이 40분 미만이면 시(hour)에서 1을 빼준다

            timedelta : 시간의 차이를 나타내는 클래스
            timedelta(days=1)      1일
            timedelta(hours=1)     1시간
            timedelta(minutes=30)  30분
            timedelta(seconds=10)  10초...
        """
        now = datetime.now()
        if now.minute < 40:
            now -= timedelta(hours=1)
        base_date_str = now.strftime("%Y%m%d")
        base_time = now.strftime("%H") + "00"
        
        #초단기예보로 조회하게 변경
        url = "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst"
        params = {
            "serviceKey": service_key,
            "numOfRows": 100,
            "pageNo": 2,
            "dataType": "JSON",
            "base_date": base_date_str,
            "base_time": base_time,
            "nx": nx,
            "ny": ny
        }
        """응답형태
        {
        "response": {
            "header": {
            "resultCode": "00",
            "resultMsg": "NORMAL_SERVICE"
            },
            "body": {
            "dataType": "JSON",
            "items": {
                "item": [
                {
                    "baseDate": "20251216",
                    "baseTime": "2130",
                    "category": "LGT",
                    "fcstDate": "20251216",
                    "fcstTime": "2200",
                    "fcstValue": "0",
                    "nx": 63,
                    "ny": 89
                },
                {"category": "PTY",}
                {
                    "category": "RN1",
                    "fcstValue": "강수없음",
                },
                {
                    "category": "SKY",
                    "fcstValue": "4",
                },
                {"category": "T1H",},
                {"category": "REH",},
                {"category": "UUU",},
                {"category": "VVV",},
                {"category": "VEC",},
                {"category": "WSD",}
                ]
            },
            "pageNo": 2,
            "numOfRows": 100,
            "totalCount": 60
            }
        }}
        """
                    # 카테고리 매핑 테이블
        
        # 카테고리 매핑 테이블
        CATEGORY_MAP = {
            "T1H" : "temp",
            "RN1" : "rain",
            "REH" : "humidity",
            "SKY" : "sky",
            "PTY" : "pty",
            "WSD" : "wind_speed",
            "UUU" : "wind_u",
            "VVV" : "wind_v",
            "VEC" : "wind_dir",
            "LGT" : "lightning",
            "SNO" : "snow"
        }
        # ->(화살표) : return값의 타입 힌트
        def safe_float(v, default=0) -> str | float :
            try:
                return float(v)
            except:
                return default

        try:
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()

            items = data.get("response", {}).get("body", {}).get("items", {}).get("item", [])
            #print("items : ", items)
            # ************************
            # 초단기예보로 변경하면 6시간 분량의 응답이 와서 제일 가까운 응답만 걸러냄
            min_time = min(
                (item['fcstDate'], item['fcstTime']) for item in items
            )
            items = [
                item for item in items
                if (item['fcstDate'], item['fcstTime']) == min_time
            ]
            #print("items : ", items)  짧은거
            
            # 기본 weather 컨테이너
            weather = {
                "temp" : "-",
                "rain" : 0,
                "humidity" : 0,
                "sky" : 1,
                "pty" : 0,
                "wind_speed" : None,
                "wind_u" : None,
                "wind_v" : None,
                "wind_dir" : None,
                "snow" : 0,
                "lightning" : None,
            }
            
            for it in items:
                cat = it.get("category")
                val = it.get("fcstValue") # 초단기예보 변수명으로 변경
                #val = it.get("obsrValue") 단기실황?에서 사용하는 응답값 변수명
                if cat not in CATEGORY_MAP:
                    continue

                key = CATEGORY_MAP[cat]

                # 타입 정규화
                if key in ("sky", "pty") :
                    weather[key] = int(val) if str(val).isdigit() else 0
                elif key == "temp" :
                    weather["temp"] = safe_float(val, "-")
                else :
                    weather[key] = safe_float(val, 0)

            return weather

        except Exception as e:
            print(f"Weather API error: {e}")
            return {"temp": "-", "rain": 0, "humidity": 0, "pty": 0, "sky": 1}