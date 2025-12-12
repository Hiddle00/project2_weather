from flask import Blueprint, render_template, request, redirect, session
import dao

#user에 관련된 라우터 함수들 분리
#@app.route("/login") -> @app.route("/user/login")

# @user_bp 데코레이터가 붙은 라우터는 전부 앞에 /user가 붙는다.
recommend_bp = Blueprint("recommend", __name__, url_prefix="/recommend")


#음식 카테고리 추천
#validate > service > dao
@recommend_bp.route("/recommend", methods=["GET"])
def recommend_category() :
    categorys = dao.get_food_category()
    return categorys

#음식점 추천
#validate > service > dao
@recommend_bp.route("/recommend/<category>", methods=["GET"])
def recommend_rest(category) :
    restaurants = ""
    if category == "all" :
        restaurants = dao.get_all_restaurants()
    else :
        restaurants = dao.get_recommend_restaurants(category)
    return restaurants

