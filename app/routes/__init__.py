"""
Routes Configuration
Flask 애플리케이션의 라우팅 설정
"""

from flask import Blueprint, send_from_directory, current_app, render_template
import os
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

# 차트 대시보드 페이지 (차트 3,4,5,6,7)
@main_bp.route('/c')
def chart_dashboard():
    return render_template('c.html')

# 차트 대시보드 페이지 (햄버거 메뉴 버전)
@main_bp.route('/c1')
def chart_dashboard_v2():
    return render_template('c_1.html')

# 차트 HTML 파일 라우트
@main_bp.route('/chart3')
def chart3():
    return send_from_directory(os.path.join(current_app.root_path, '../public'), 'chart3_scatter_matrix.html')

@main_bp.route('/chart4')
def chart4():
    return send_from_directory(os.path.join(current_app.root_path, '../public'), 'chart4_yearly_area.html')

@main_bp.route('/chart5')
def chart5():
    return send_from_directory(os.path.join(current_app.root_path, '../public'), 'chart5_regional_bar.html')

@main_bp.route('/chart6')
def chart6():
    return send_from_directory(os.path.join(current_app.root_path, '../public'), 'chart6_pivot_bar.html')

@main_bp.route('/chart7')
def chart7():
    return send_from_directory(os.path.join(current_app.root_path, '../public'), 'chart7_pie_subplots.html')

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

@api_bp.route('/statistics/yearly-trend', methods=['GET'])
def api_yearly_trend():
    return hospital_controller.get_yearly_total_trend()

# ============================================
# React 차트 앱 라우트 (하이브리드 배포)
# ============================================

@main_bp.route('/charts')
@main_bp.route('/charts/')
def chart_app():
    """React 차트 앱의 index.html 서빙"""
    chart_app_dir = os.path.join(current_app.root_path, 'static', 'chart-app')
    
    # chart-app 폴더가 없으면 안내 페이지 표시
    if not os.path.exists(chart_app_dir):
        return '''
        <html>
        <head><title>차트 앱 설치 필요</title></head>
        <body style="font-family: Arial; padding: 50px; text-align: center;">
            <h1>🚀 React 차트 앱이 아직 설치되지 않았습니다</h1>
            <p>다음 명령어를 실행하여 차트 앱을 빌드하고 배포하세요:</p>
            <pre style="background: #f5f5f5; padding: 20px; border-radius: 5px; text-align: left; display: inline-block;">
cd c:\\bohun1\\Chart
npm run build
Copy-Item -Path "dist\\*" -Destination "..\\app\\static\\chart-app\\" -Recurse -Force
            </pre>
            <p><a href="/">← 메인 페이지로 돌아가기</a></p>
        </body>
        </html>
        ''', 404
    
    return send_from_directory(chart_app_dir, 'index.html')

@main_bp.route('/charts/<path:path>')
def serve_chart_assets(path):
    """React 앱의 정적 파일들 서빙 (assets, data, Plotly HTML 등)"""
    chart_app_dir = os.path.join(current_app.root_path, 'static', 'chart-app')
    
    # 파일이 존재하는지 확인
    file_path = os.path.join(chart_app_dir, path)
    if not os.path.exists(file_path):
        return {'error': f'파일을 찾을 수 없습니다: {path}'}, 404
    
    return send_from_directory(chart_app_dir, path)

# ============================================
# 기존 생성된 HTML 파일 서빙
# ============================================

# 생성된 지도 HTML 파일 서빙
@main_bp.route('/<path:filename>')
def serve_generated_file(filename):
    """생성된 지도 HTML 파일 제공"""
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