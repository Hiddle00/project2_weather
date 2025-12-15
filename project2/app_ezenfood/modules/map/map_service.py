from .map_dao import MapDAO
import requests
from datetime import datetime
import math

class MapService:
    def __init__(self):
        self.dao = MapDAO()

    # ==========================
    # 음식점 조회
    # ==========================
    def get_restaurants(self, lat, lon, food_sort=None, limit=30):
        return self.dao.fetch_restaurants(lat, lon, food_sort, limit)

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
        hh = now.hour
        base_date = now
        if now.minute < 40:
            hh -= 1
            if hh < 0:
                hh = 23
                base_date = base_date.replace(day=base_date.day - 1)

        base_date_str = base_date.strftime("%Y%m%d")
        base_time = f"{hh:02d}00"

        url = (
            f"https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"
            f"?serviceKey={service_key}&numOfRows=100&pageNo=1&dataType=JSON"
            f"&base_date={base_date_str}&base_time={base_time}&nx={nx}&ny={ny}"
        )

        try:
            res = requests.get(url, timeout=5)
            data = res.json()
            items = data.get("response", {}).get("body", {}).get("items", {}).get("item", [])
            weather = {"temp": "-", "rain": 0, "humidity": 0, "pty": 0, "sky": 1}

            for it in items:
                if it["category"] == "T1H": weather["temp"] = float(it["obsrValue"])
                elif it["category"] == "RN1": weather["rain"] = float(it["obsrValue"])
                elif it["category"] == "REH": weather["humidity"] = float(it["obsrValue"])
                elif it["category"] == "SKY": weather["sky"] = int(it["obsrValue"])
                elif it["category"] == "PTY": weather["pty"] = int(it["obsrValue"])
            return weather
        except Exception as e:
            print(f"Weather API error: {e}")
            return {"temp": "-", "rain": 0, "humidity": 0, "pty": 0, "sky": 1}
