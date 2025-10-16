"""
Hospital Controller
병원 관련 HTTP 요청을 처리하는 컨트롤러
"""

from flask import request, jsonify, render_template, redirect, url_for, flash
from ..services.hospital_service import HospitalService
from ..repositories.testdb_hospital_repository import TestDBHospitalRepository
from ..repositories.hospital_crud_repository import HospitalCrudRepository
from ..services.folium_map_service import FoliumMapService
import os
import pymysql

class HospitalController:
    def __init__(self):
        # TestDB 리포지토리를 사용하여 서비스 초기화
        testdb_repository = TestDBHospitalRepository()
        self.service = HospitalService(testdb_repository)
        # CRUD 전용 리포지토리
        self.crud_repository = HospitalCrudRepository()
        # MySQL 연결 설정
        import os
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': os.environ.get('MYSQL_PASSWORD', '1234'),  # 환경변수 또는 기본값
            'database': 'testdb',
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor
        }
        
    def index(self):
        """병원 목록 페이지"""
        try:
            hospitals = self.service.get_all_hospitals()
            return render_template('hospitals.html', hospitals=hospitals)
        except Exception as e:
            flash(f'병원 목록을 불러오는데 실패했습니다: {str(e)}', 'error')
            return render_template('hospitals.html', hospitals=[])
            
    def show(self, hospital_id):
        """병원 상세 정보"""
        try:
            hospital = self.service.get_hospital(hospital_id)
            if not hospital:
                return jsonify({'error': '병원을 찾을 수 없습니다'}), 404
            return jsonify(hospital)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
            
    def get_hospitals_for_crud(self):
        """CRUD용 병원 목록 조회 (검색 및 필터링 지원)"""
        try:
            search = request.args.get('search', '').strip()
            filter_type = request.args.get('filter_type', '').strip()
            
            hospitals = self.crud_repository.find_all_for_crud(search, filter_type)
            return jsonify(hospitals)
        except Exception as e:
            print(f"CRUD 조회 오류: {e}")
            return jsonify({'error': str(e)}), 500
    
    def create_hospital_crud(self):
        """CRUD용 병원 생성"""
        try:
            data = request.get_json()
            hospital_id = self.crud_repository.create_crud(data)
            return jsonify({'success': True, 'id': hospital_id}), 201
        except Exception as e:
            print(f"CRUD 생성 오류: {e}")
            return jsonify({'error': str(e)}), 500
    
    def update_hospital_crud(self, hospital_id):
        """CRUD용 병원 수정"""
        try:
            data = request.get_json()
            success = self.crud_repository.update_crud(hospital_id, data)
            if success:
                return jsonify({'success': True})
            return jsonify({'error': '병원을 찾을 수 없습니다'}), 404
        except Exception as e:
            print(f"CRUD 수정 오류: {e}")
            return jsonify({'error': str(e)}), 500
    
    def delete_hospital_crud(self, hospital_id):
        """CRUD용 병원 삭제"""
        try:
            success = self.crud_repository.delete_crud(hospital_id)
            if success:
                return jsonify({'success': True})
            return jsonify({'error': '병원을 찾을 수 없습니다'}), 404
        except Exception as e:
            print(f"CRUD 삭제 오류: {e}")
            return jsonify({'error': str(e)}), 500
    
    def create(self):
        """새 병원 생성"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': '요청 데이터가 없습니다'}), 400
                
            # 필수 필드 검증
            required_fields = ['name']
            for field in required_fields:
                if not data.get(field):
                    return jsonify({'error': f'{field}는 필수 필드입니다'}), 400
                    
            hospital_id = self.service.create_hospital(data)
            return jsonify({'id': hospital_id, 'message': '병원이 성공적으로 생성되었습니다'}), 201
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
            
    def update(self, hospital_id):
        """병원 정보 수정"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': '요청 데이터가 없습니다'}), 400
                
            success = self.service.update_hospital(hospital_id, data)
            if not success:
                return jsonify({'error': '병원을 찾을 수 없거나 수정에 실패했습니다'}), 404
                
            return jsonify({'message': '병원 정보가 성공적으로 수정되었습니다'})
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
            
    def delete(self, hospital_id):
        """병원 삭제"""
        try:
            success = self.service.delete_hospital(hospital_id)
            if not success:
                return jsonify({'error': '병원을 찾을 수 없거나 삭제에 실패했습니다'}), 404
                
            return jsonify({'message': '병원이 성공적으로 삭제되었습니다'})
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
            
    def search(self):
        """병원 검색"""
        try:
            query = request.args.get('q', '')
            lat = request.args.get('lat', type=float)
            lng = request.args.get('lng', type=float)
            radius = request.args.get('radius', 1.0, type=float)
            
            if lat and lng:
                # 위치 기반 검색
                hospitals = self.service.get_hospitals_by_location(lat, lng, radius)
            elif query:
                # 이름 기반 검색
                hospitals = self.service.search_hospitals_by_name(query)
            else:
                # 모든 병원
                hospitals = self.service.get_all_hospitals()
                
            return jsonify(hospitals)
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
            
    def api_list(self):
        """API용 병원 목록"""
        try:
            hospitals = self.service.get_all_hospitals()
            return jsonify(hospitals)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def check_table_structure(self):
        """테이블 구조 확인용 엔드포인트"""
        try:
            # TestDB 리포지토리에서 테이블 구조 확인
            testdb_repository = TestDBHospitalRepository()
            result = testdb_repository.get_table_structure()
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': f'테이블 구조 확인 실패: {str(e)}'}), 500
        
    def check_all_tables(self):
        """모든 테이블 목록 확인용 엔드포인트"""
        try:
            testdb_repository = TestDBHospitalRepository()
            result = testdb_repository.get_all_tables()
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': f'테이블 목록 확인 실패: {str(e)}'}), 500
    
    def generate_folium_map(self):
        """Folium을 사용한 지도 생성"""
        try:
            map_service = FoliumMapService()
            filepath = map_service.create_hospital_map()
            filename = os.path.basename(filepath)
            
            # 병원 수 계산
            hospitals = self.service.get_all_hospitals()
            hospital_count = len(hospitals)
            
            # 파일을 URL 경로로 변환 (파일명만 사용)
            map_url = f'/{filename}'
            
            return jsonify({
                'success': True,
                'message': '지도가 성공적으로 생성되었습니다.',
                'filepath': filepath,
                'filename': filename,
                'map_url': map_url,
                'hospital_count': hospital_count
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'지도 생성 실패: {str(e)}'
            }), 500
    
    def export_to_excel(self):
        """병원 데이터를 Excel로 내보내기"""
        try:
            map_service = FoliumMapService()
            filepath = map_service.export_to_excel()
            
            return jsonify({
                'success': True,
                'message': 'Excel 파일이 성공적으로 생성되었습니다.',
                'filepath': filepath,
                'filename': os.path.basename(filepath)
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Excel 내보내기 실패: {str(e)}'
            }), 500
    
    def get_yearly_statistics(self):
        """연도별 통계 데이터 조회 (위탁병원현황_연도별현황)"""
        try:
            connection = pymysql.connect(**self.db_config)
            with connection.cursor() as cursor:
                sql = """
                SELECT 광역지자체, `2022년12월`, `2023년12월`, `2024년12월`
                FROM 위탁병원현황_연도별현황
                ORDER BY `2024년12월` DESC
                """
                cursor.execute(sql)
                results = cursor.fetchall()
                
            connection.close()
            return jsonify({'success': True, 'data': results})
        except Exception as e:
            print(f"연도별 통계 조회 오류: {e}")
            return jsonify({'success': False, 'error': str(e)}), 500