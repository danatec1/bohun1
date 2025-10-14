"""
Routes Configuration
Flask 애플리케이션의 라우팅 설정
"""

from flask import Blueprint
from ..controllers.main_controller import MainController
from ..controllers.hospital_controller import HospitalController
from ..controllers.auth_controller import AuthController

# 블루프린트 생성
main_bp = Blueprint('main', __name__)
api_bp = Blueprint('api', __name__, url_prefix='/api')

# 컨트롤러 인스턴스 생성
main_controller = MainController()
hospital_controller = HospitalController()
auth_controller = AuthController()

# 테스트 라우트
@main_bp.route('/test')
def test():
    return '<h1>Flask 서버가 정상적으로 작동합니다!</h1><p><a href="/">메인 페이지로</a></p>'

# 메인 페이지 라우트
@main_bp.route('/')
def index():
    try:
        return main_controller.index()
    except Exception as e:
        return f'<h1>오류 발생</h1><p>{str(e)}</p><p><a href="/test">테스트 페이지</a></p>'

# 병원 관련 라우트
@main_bp.route('/hospitals')
def hospitals():
    return hospital_controller.index()

# 지도 페이지 라우트
@main_bp.route('/map')
def map_view():
    return main_controller.map_view()

# Folium 지도 페이지 라우트
@main_bp.route('/folium-map')
def folium_map():
    return main_controller.folium_map()

# 병원 CRUD 페이지
@main_bp.route('/admin')
@main_bp.route('/hospital_crud')
def hospital_crud():
    return main_controller.hospital_crud()

# API 라우트
@api_bp.route('/hospitals', methods=['GET'])
def api_hospitals_list():
    return hospital_controller.api_list()

# CRUD API 라우트
@api_bp.route('/hospitals/crud', methods=['GET'])
def api_hospitals_crud_list():
    """CRUD용 병원 목록 조회 (검색/필터 지원)"""
    return hospital_controller.get_hospitals_for_crud()

@api_bp.route('/hospitals', methods=['POST'])
def api_hospitals_create():
    """CRUD용 병원 생성"""
    return hospital_controller.create_hospital_crud()

@api_bp.route('/hospitals/<int:hospital_id>', methods=['PUT'])
def api_hospitals_update(hospital_id):
    """CRUD용 병원 수정"""
    return hospital_controller.update_hospital_crud(hospital_id)

@api_bp.route('/hospitals/<int:hospital_id>', methods=['DELETE'])
def api_hospitals_delete(hospital_id):
    """CRUD용 병원 삭제"""
    return hospital_controller.delete_hospital_crud(hospital_id)

@api_bp.route('/hospitals/search', methods=['GET'])
def api_hospitals_search():
    return hospital_controller.search()

@api_bp.route('/hospitals/table-structure', methods=['GET'])
def api_hospitals_table_structure():
    return hospital_controller.check_table_structure()

@api_bp.route('/tables', methods=['GET'])
def api_all_tables():
    return hospital_controller.check_all_tables()

@api_bp.route('/map/folium', methods=['GET'])
def api_generate_folium_map():
    return hospital_controller.generate_folium_map()

@api_bp.route('/export/excel', methods=['GET'])
def api_export_excel():
    return hospital_controller.export_to_excel()

@api_bp.route('/statistics/yearly', methods=['GET'])
def api_yearly_statistics():
    return hospital_controller.get_yearly_statistics()

# 생성된 지도 HTML 파일 서빙
@main_bp.route('/<path:filename>')
def serve_generated_file(filename):
    """생성된 지도 HTML 파일 제공"""
    from flask import send_from_directory
    import os
    
    # .html 파일만 허용
    if not filename.endswith('.html'):
        return {'error': '페이지를 찾을 수 없습니다'}, 404
    
    # 프로젝트 루트 디렉토리에서 파일 찾기
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    file_path = os.path.join(root_dir, filename)
    
    if os.path.exists(file_path):
        return send_from_directory(root_dir, filename)
    
    return {'error': '페이지를 찾을 수 없습니다'}, 404

# 인증 관련 라우트
@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    return auth_controller.login()

@main_bp.route('/signup', methods=['POST'])
def signup():
    return auth_controller.signup()

@main_bp.route('/logout')
def logout():
    return auth_controller.logout()

def register_routes(app):
    """애플리케이션에 블루프린트 등록"""
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)