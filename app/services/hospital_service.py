"""
Hospital Service
병원 관련 비즈니스 로직을 처리하는 서비스
"""

from typing import List, Optional, Dict, Any
from ..models.hospital import Hospital
from ..repositories.hospital_repository import HospitalRepository

class HospitalService:
    def __init__(self, repository: HospitalRepository = None):
        self.repository = repository or HospitalRepository()
        
    def create_hospital(self, hospital_data: Dict[str, Any]) -> int:
        """새 병원 등록"""
        hospital = Hospital.from_dict(hospital_data)
        return self.repository.create(hospital)
        
    def get_hospital(self, hospital_id: int) -> Optional[Dict[str, Any]]:
        """병원 정보 조회"""
        hospital = self.repository.find_by_id(hospital_id)
        return hospital.to_dict() if hospital else None
        
    def get_all_hospitals(self) -> List[Dict[str, Any]]:
        """모든 병원 목록 조회"""
        hospitals = self.repository.find_all()
        return [hospital.to_dict() for hospital in hospitals]
        
    def update_hospital(self, hospital_id: int, hospital_data: Dict[str, Any]) -> bool:
        """병원 정보 수정"""
        hospital_data['hospital_id'] = hospital_id
        hospital = Hospital.from_dict(hospital_data)
        return self.repository.update(hospital)
        
    def delete_hospital(self, hospital_id: int) -> bool:
        """병원 정보 삭제"""
        return self.repository.delete(hospital_id)
        
    def search_hospitals_by_name(self, name: str) -> List[Dict[str, Any]]:
        """병원명으로 검색"""
        all_hospitals = self.get_all_hospitals()
        return [h for h in all_hospitals if name.lower() in h['name'].lower()]
        
    def get_hospitals_by_location(self, lat: float, lng: float, radius: float = 1.0) -> List[Dict[str, Any]]:
        """위치 기준으로 병원 검색 (반경 내)"""
        import math
        
        def calculate_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
            """두 지점 간 거리 계산 (km)"""
            R = 6371  # 지구 반지름 (km)
            
            lat1_rad = math.radians(lat1)
            lng1_rad = math.radians(lng1)
            lat2_rad = math.radians(lat2)
            lng2_rad = math.radians(lng2)
            
            dlat = lat2_rad - lat1_rad
            dlng = lng2_rad - lng1_rad
            
            a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng/2)**2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            
            return R * c
        
        all_hospitals = self.get_all_hospitals()
        nearby_hospitals = []
        
        for hospital in all_hospitals:
            if hospital['latitude'] and hospital['longitude']:
                distance = calculate_distance(
                    lat, lng, 
                    hospital['latitude'], hospital['longitude']
                )
                if distance <= radius:
                    hospital['distance'] = round(distance, 2)
                    nearby_hospitals.append(hospital)
                    
        # 거리순으로 정렬
        nearby_hospitals.sort(key=lambda x: x.get('distance', float('inf')))
        return nearby_hospitals
    
    def get_hospitals_for_crud(self, search: str = '', filter_type: str = '') -> List[Dict[str, Any]]:
        """CRUD용 병원 목록 조회 (검색 및 필터링)"""
        return self.repository.find_all_for_crud(search, filter_type)
    
    def create_hospital_crud(self, data: Dict[str, Any]) -> int:
        """CRUD용 병원 생성"""
        return self.repository.create_crud(data)
    
    def update_hospital_crud(self, hospital_id: int, data: Dict[str, Any]) -> bool:
        """CRUD용 병원 수정"""
        return self.repository.update_crud(hospital_id, data)
    
    def delete_hospital_crud(self, hospital_id: int) -> bool:
        """CRUD용 병원 삭제"""
        return self.repository.delete_crud(hospital_id)