from flask import Flask, request
from flask_cors import CORS
from homecontroller import HomeController

app = Flask(__name__)
CORS(app)

home_controller = HomeController()

# 메인 페이지
@app.route('/')
def index():
    return home_controller.index()

# 날씨 기반 음식 추천
@app.route('/api/recommend', methods=['GET'])
def recommend():
    return home_controller.get_recommendation(request.args)

# 음식점 조회
@app.route('/api/restaurants', methods=['GET'])
def restaurants():
    return home_controller.get_restaurants(request.args)

if __name__ == '__main__':
    print("서버 가동 준비 완료!")
    app.run(host='0.0.0.0', port=5000, debug=True)
