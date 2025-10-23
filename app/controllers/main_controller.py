"""
Main Controller
메인 페이지 관련 HTTP 요청을 처리하는 컨트롤러
"""

from flask import render_template
from ..services.hospital_service import HospitalService

class MainController:
    def __init__(self):
        self.hospital_service = HospitalService()
        
    def index(self):
        """메인 페이지 - 누구나 접근 가능"""
        try:
            # 통계 데이터 수집
            hospitals = self.hospital_service.get_all_hospitals()
            
            # 지역별 통계 (시도 기준)
            provinces = set()
            departments = set()
            
            for hospital in hospitals:
                # 주소에서 시도 추출 (간단한 방법)
                if hospital.get('address'):
                    address_parts = hospital['address'].split()
                    if address_parts:
                        province = address_parts[0]
                        # 특별시, 광역시, 도 등이 포함된 경우만 추가
                        if any(suffix in province for suffix in ['시', '도', '특별시', '광역시']):
                            provinces.add(province)
                
                # 진료과목 수집
                if hospital.get('medical_departments'):
                    departments.update(hospital['medical_departments'])
            
            context = {
                'total_hospitals': len(hospitals),
                'total_provinces': len(provinces),
                'total_departments': len(departments)
            }
            
            return render_template('index.html', **context)
            
        except Exception as e:
            # 에러 발생시 기본값으로 렌더링
            context = {
                'total_hospitals': 0,
                'total_provinces': 0,
                'total_departments': 0
            }
            return render_template('index.html', **context)
    
    def map_view(self):
        """지도 전용 페이지"""
        try:
            hospitals = self.hospital_service.get_all_hospitals()
            return render_template('map.html', hospitals=hospitals)
        except Exception as e:
            print(f"지도 페이지 오류: {e}")
            return render_template('map.html', hospitals=[])
    
    def folium_map(self):
        """Folium 지도 페이지"""
        return render_template('folium_map.html')
    
    def hospital_crud(self):
        """병원 CRUD 관리 페이지"""
        return render_template('hospital_crud.html')
