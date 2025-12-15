from flask import Flask, request
from flask_cors import CORS
from app_ezenfood import CSV_DIR
from map import init_app as map_init
map_init(app)


app = Flask(__name__)
CORS(app)

app.config["CSV_DIR"] = CSV_DIR

# 메인 페이지
@app.route('/')
def index():
    # 바로 map.html 렌더링
    return render_template('map.html', kakao_key=KAKAO_MAP_KEY)

# 날씨 기반 음식 추천       이거 없애고 recommend쪽으로 가져와야함
@app.route('/api/recommend', methods=['GET'])
def recommend():
    return home_controller.get_recommendation(request.args)

# 음식점 조회               이거 없애고 recommend쪽으로 가져와야함
@app.route('/api/restaurants', methods=['GET'])
def restaurants():
    return home_controller.get_restaurants(request.args)

if __name__ == '__main__':
    print("서버 가동 준비 완료!")
    app.run(host='0.0.0.0', port=5000, debug=True)
