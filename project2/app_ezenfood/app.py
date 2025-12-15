from flask import Flask, request, render_template
from flask_cors import CORS
from .modules.map_api import init_app as map_init
from pathlib import Path
from dotenv import load_dotenv
import os
# 뭣만 하면 CSV_DIR 오류 만 하루종일 뜨길래 오류 덜뜨게 수정 완료 모듈구동법 수정함

BASE_DIR = Path(__file__).resolve().parent
CSV_DIR = BASE_DIR / "csv"


    
app = Flask(__name__)
CORS(app)

# 맵 init 호출
map_init(app)

app.config["CSV_DIR"] = CSV_DIR

# .env 파일 읽기
load_dotenv()
KAKAO_MAP_KEY = os.getenv("KAKAO_MAP_KEY")
# 메인 페이지   (이거 홈컨트롤 관리 말고 바로 app.py에서 렌더링 하게 수정함요)
@app.route('/')
def index():
    return render_template('map.html', kakao_key=KAKAO_MAP_KEY)

# 날씨 기반 음식 추천       이거 없애고 recommend쪽으로 가져와야함
# @app.route('/api/recommend', methods=['GET'])
# def recommend():
#     return home_controller.get_recommendation(request.args)

# 음식점 조회               이거 없애고 recommend쪽으로 가져와야함
# @app.route('/api/restaurants', methods=['GET'])
# def restaurants():
#     return home_controller.get_restaurants(request.args)

if __name__ == '__main__':
    print("서버 가동 준비 완료!")
    app.run(host='0.0.0.0', port=5000, debug=True)
