#!/usr/bin/env python3
"""
MySQL 직접 연결 테스트 스크립트
testdb.위탁병원현황 테이블에서 데이터를 직접 가져와서 지도에 표시하는 테스트
"""

from app.repositories.testdb_hospital_repository import TestDBHospitalRepository

def test_mysql_direct_connection():
    """MySQL에서 직접 병원 데이터를 가져오는 테스트"""
    print("=" * 60)
    print("🏥 MySQL 직접 연결 테스트 (testdb.위탁병원현황)")
    print("=" * 60)
    
    try:
        # Repository 인스턴스 생성
        repo = TestDBHospitalRepository()
        print("✅ Repository 생성 완료")
        
        # 테이블 구조 확인
        print("\n📊 테이블 구조 확인:")
        structure = repo.get_table_structure()
        print(f"   테이블명: {structure['table_name']}")
        print(f"   존재여부: {structure['exists']}")
        print(f"   레코드 수: {structure.get('row_count', 0)}개")
        
        # 컬럼 정보 출력
        if structure.get('columns'):
            print("\n📋 컬럼 목록:")
            for col in structure['columns'][:5]:  # 처음 5개만
                print(f"   - {col['Field']}: {col['Type']}")
        
        # 실제 데이터 조회
        print("\n🔍 실제 데이터 조회:")
        hospitals = repo.find_all()
        print(f"✅ MySQL에서 직접 가져온 병원 수: {len(hospitals)}개")
        
        if hospitals:
            # 처음 3개 병원 정보 출력
            print("\n🏥 처음 3개 병원 정보:")
            for i, hospital in enumerate(hospitals[:3]):
                print(f"   {i+1}. {hospital.name}")
                print(f"      주소: {hospital.address}")
                print(f"      좌표: 위도 {hospital.latitude}, 경도 {hospital.longitude}")
                print(f"      종별: {hospital.medical_departments}")
                print()
            
            print("=" * 60)
            print("🗺️  이 데이터가 실시간으로 지도에 표시됩니다!")
            print("   - Folium 지도에서 각 병원이 마커로 표시됨")
            print("   - 마커 클릭시 병원 정보 팝업 표시")
            print("   - MySQL 데이터 변경시 즉시 지도에 반영")
            print("=" * 60)
            return True
            
        else:
            print("❌ 데이터를 가져오지 못했습니다.")
            return False
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return False

if __name__ == "__main__":
    success = test_mysql_direct_connection()
    if success:
        print("\n✅ MySQL 직접 연결 테스트 성공!")
        print("   웹 브라우저에서 http://127.0.0.1:5001/folium-map 에 접속하여")
        print("   '지도 생성' 버튼을 클릭하면 MySQL 데이터가 지도에 표시됩니다.")
    else:
        print("\n❌ MySQL 직접 연결 테스트 실패!")
