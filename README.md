날씨 기반 음식 추천 플랫폼
전주 지역 날씨 데이터를 분석하여 날씨에 맞는 음식을 추천하고, 카카오맵으로 주변 음식점을 보여주는 웹 서비스입니다.
기술 스택

Backend: Flask
Frontend: HTML5, CSS3, JavaScript, Bootstrap
Database: MySQL
API: 기상청 API, 카카오맵 API
Tools: Git, VS Code

주요 기능

사용자 위치 기반 현재 날씨 조회
3년치 날씨 데이터 군집화를 통한 음식 추천
추천 음식에 맞는 전주 음식점 리스트 제공
카카오맵을 통한 음식점 위치 표시

실행 방법

저장소 클론
git clone [저장소 주소]
cd project2
라이브러리 설치
pip install -r app_ezenfood/requirements.txt
실행
python -m app_ezenfood.app

프로젝트 루트 폴더(project2)에서 실행해야 합니다.
담당 역할
역할 | 담당자
데이터 수집 및 전처리 | 최연흠
군집화 로직 구현 | 이승준
임베딩 작업 | 유재욱
