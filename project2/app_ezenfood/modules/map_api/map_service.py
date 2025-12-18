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
        # ==========================
        # 1. 위경도 → 기상청 격자 좌표 변환
        # ==========================
        coords = self.dfs_xy_conv(lat, lon)
        nx, ny = coords["x"], coords["y"]

        # ==========================
        # 2. 초단기예보 기준 시각 계산
        #    - 매시 30분 발표
        #    - 00~44분 → 이전 시각 사용
        # ==========================
        now = datetime.now()
        if now.minute < 45:
            now -= timedelta(hours=1)

        base_date = now.strftime("%Y%m%d")      # 예: 20251218
        base_time = now.strftime("%H") + "00"   # 예: 1400

        # ==========================
        # 3. 기상청 초단기예보 API
        # ==========================
        url = "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst"
        params = {
            "serviceKey": service_key,
            "numOfRows": 100,
            "pageNo": 1,
            "dataType": "JSON",
            "base_date": base_date,
            "base_time": base_time,
            "nx": nx,
            "ny": ny
        }

        # ==========================
        # 4. 기상청 요소 코드 → 내부 키 매핑
        # ==========================
        CATEGORY_MAP = {
            "T1H": "temp",        # 기온 (℃)
            "RN1": "rain",        # 1시간 강수량 (mm)
            "REH": "humidity",    # 습도 (%)
            "SKY": "sky",         # 하늘상태 (1,3,4)
            "PTY": "pty",         # 강수형태 (0~7)
            "WSD": "wind_speed",  # 풍속 (m/s)
            "UUU": "wind_u",      # 동서바람 (+동 / -서)
            "VVV": "wind_v",      # 남북바람 (+북 / -남)
            "VEC": "wind_dir",    # 풍향 (각도)
            "LGT": "lightning",   # 낙뢰
            "SNO": "snow"         # 적설량
        }

        # ==========================
        # 5. 숫자 변환 유틸
        # ==========================
        def to_float(v):
            try:
                return float(v)
            except:
                return None

        # ==========================
        # 6. 반환용 기본 weather 구조
        #    ※ 값이 없는 요소는 None 유지
        # ==========================
        weather = {
            "temp": None,
            "rain": 0,
            "humidity": None,
            "sky": None,
            "pty": None,
            "wind_speed": None,
            "wind_u": None,
            "wind_v": None,
            "wind_dir": None,
            "snow": 0,
            "lightning": None
        }

        try:
            # ==========================
            # 7. API 호출
            # ==========================
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()

            items = (
                data.get("response", {})
                    .get("body", {})
                    .get("items", {})
                    .get("item", [])
            )

            # 데이터 없으면 기본값 반환
            if not items:
                return weather

            # ==========================
            # 8. 예보 시각(fcstDate, fcstTime) 목록 정렬
            # ==========================
            times = sorted(set(
                (i["fcstDate"], i["fcstTime"]) for i in items
            ))

            # ==========================
            # 9. 현재 기준 이후 가장 가까운 예보 시각 선택
            # ==========================
            now_key = (base_date, base_time)
            target_time = None

            for t in times:
                if t >= now_key:
                    target_time = t
                    break

            # 이후 시각이 없으면 마지막 시각 사용
            if target_time is None:
                target_time = times[-1]

            # ==========================
            # 10. 선택된 시각 데이터만 필터링
            # ==========================
            target_items = [
                i for i in items
                if (i["fcstDate"], i["fcstTime"]) == target_time
            ]

            # ==========================
            # 11. 요소별 값 채우기
            # ==========================
            for it in target_items:
                cat = it.get("category")
                val = it.get("fcstValue")

                if cat not in CATEGORY_MAP:
                    continue

                key = CATEGORY_MAP[cat]

                # 하늘상태 / 강수형태는 정수
                if key in ("sky", "pty"):
                    if str(val).isdigit():
                        weather[key] = int(val)

                # 그 외 수치형 데이터
                else:
                    v = to_float(val)
                    if v is not None:
                        weather[key] = v

            return weather

        except Exception as e:
            print(f"[Weather API error] {e}")
            return weather

