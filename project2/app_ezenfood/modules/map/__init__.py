# map/__init__.py
from .map_router import map_bp

def init_app(app):
    """
    Flask 앱에 map 모듈 블루프린트 등록
    """
    app.register_blueprint(map_bp, url_prefix="/api/map")
