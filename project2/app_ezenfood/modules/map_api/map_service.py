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
        try:
            return self.dao.fetch_restaurants(lat, lon, food_sort, limit)
        except Exception as e:
            print(f"[MapService] DB 조회 실패: {e}")
            return []

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

        now = datetime.now()
        if now.minute < 45:
            now -= timedelta(hours=1)
        base_date_str = now.strftime("%Y%m%d")
        base_time = now.strftime("%H") + "00"

        url = "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst"
        params = {
            "serviceKey": service_key,
            "numOfRows": 100,
            "pageNo": 1,
            "dataType": "JSON",
            "base_date": base_date_str,
            "base_time": base_time,
            "nx": nx,
            "ny": ny
        }

        CATEGORY_MAP = {
            "T1H": "temp",
            "RN1": "rain",
            "REH": "humidity",
            "SKY": "sky",
            "PTY": "pty",
            "WSD": "wind_speed",
            "UUU": "wind_u",
            "VVV": "wind_v",
            "VEC": "wind_dir",
            "LGT": "lightning",
            "SNO": "snow"
        }

        def safe_float(v, default=0) -> str | float:
            try:
                return float(v)
            except:
                return default

        # 기본 weather 값
        weather = {
            "temp": "-", "rain": 0, "humidity": 0, "sky": 1, "pty": 0,
            "wind_speed": None, "wind_u": None, "wind_v": None,
            "wind_dir": None, "snow": 0, "lightning": None,
        }

        try:
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            items = data.get("response", {}).get("body", {}).get("items", {}).get("item", [])

            if not items:
                return weather

            # 가장 가까운 시간 데이터 필터
            min_time = min((item['fcstDate'], item['fcstTime']) for item in items)
            items = [item for item in items if (item['fcstDate'], item['fcstTime']) == min_time]

            for it in items:
                cat = it.get("category")
                val = it.get("fcstValue")
                if cat not in CATEGORY_MAP:
                    continue
                key = CATEGORY_MAP[cat]

                if key in ("sky", "pty"):
                    weather[key] = int(val) if str(val).isdigit() else 0
                elif key == "temp":
                    weather["temp"] = safe_float(val, "-")
                else:
                    weather[key] = safe_float(val, 0)

            return weather

        except Exception as e:
            print(f"[Weather API error] {e}")
            return weather
