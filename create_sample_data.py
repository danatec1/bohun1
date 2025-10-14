"""
샘플 데이터 생성 스크립트
"""

from app.services.hospital_service import HospitalService

def create_sample_data():
    service = HospitalService()
    
    # 샘플 병원 데이터
    sample_hospitals = [
        {
            'name': '서울대학교병원',
            'address': '서울특별시 종로구 대학로 101',
            'latitude': 37.5800,
            'longitude': 127.0017,
            'medical_departments': ['내과', '외과', '정형외과', '신경과']
        },
        {
            'name': '삼성서울병원',
            'address': '서울특별시 강남구 일원로 81',
            'latitude': 37.4881,
            'longitude': 127.0857,
            'medical_departments': ['심장내과', '신경외과', '암센터']
        },
        {
            'name': '아산병원',
            'address': '서울특별시 송파구 올림픽로43길 88',
            'latitude': 37.5260,
            'longitude': 127.1106,
            'medical_departments': ['내과', '외과', '소아과', '산부인과']
        }
    ]
    
    try:
        for hospital_data in sample_hospitals:
            hospital_id = service.create_hospital(hospital_data)
            print(f"생성된 병원: {hospital_data['name']} (ID: {hospital_id})")
        
        print("샘플 데이터 생성 완료!")
        
    except Exception as e:
        print(f"샘플 데이터 생성 실패: {e}")

if __name__ == '__main__':
    create_sample_data()