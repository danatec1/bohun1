"""
Test Configuration
테스트 파일 예시
"""

import pytest
import sys
import os

# 프로젝트 루트를 sys.path에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app
from app.services.hospital_service import HospitalService

@pytest.fixture
def app():
    """테스트용 Flask 앱"""
    app = create_app('testing')
    return app

@pytest.fixture
def client(app):
    """테스트 클라이언트"""
    return app.test_client()

@pytest.fixture
def service():
    """병원 서비스 인스턴스"""
    return HospitalService()

def test_main_page(client):
    """메인 페이지 테스트"""
    response = client.get('/')
    assert response.status_code == 200

def test_hospitals_page(client):
    """병원 목록 페이지 테스트"""
    response = client.get('/hospitals')
    assert response.status_code == 200

def test_api_hospitals_list(client):
    """병원 API 목록 테스트"""
    response = client.get('/api/hospitals')
    assert response.status_code == 200
    
def test_hospital_service_create(service):
    """병원 서비스 생성 테스트"""
    hospital_data = {
        'name': '테스트 병원',
        'address': '서울시 강남구',
        'latitude': 37.5665,
        'longitude': 126.9780,
        'medical_departments': ['내과', '외과']
    }
    
    hospital_id = service.create_hospital(hospital_data)
    assert hospital_id is not None
    assert isinstance(hospital_id, int)
    
    # 생성된 병원 조회
    hospital = service.get_hospital(hospital_id)
    assert hospital is not None
    assert hospital['name'] == '테스트 병원'