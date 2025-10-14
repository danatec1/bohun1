"""
Hospital Model
병원 정보를 관리하는 데이터 모델
"""

class Hospital:
    def __init__(self, hospital_id=None, name=None, address=None, 
                 latitude=None, longitude=None, medical_departments=None,
                 bed_count=None, department_count=None):
        self.hospital_id = hospital_id
        self.name = name
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.medical_departments = medical_departments or []
        self.bed_count = bed_count
        self.department_count = department_count
    
    @property
    def hospital_type(self):
        """종별 반환 (medical_departments의 첫 번째 항목)"""
        if self.medical_departments and len(self.medical_departments) > 0:
            return self.medical_departments[0]
        return '기타'
        
    def to_dict(self):
        """객체를 딕셔너리로 변환"""
        return {
            'hospital_id': self.hospital_id,
            'name': self.name,
            'address': self.address,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'medical_departments': self.medical_departments,
            'hospital_type': self.hospital_type
        }
        
    @classmethod
    def from_dict(cls, data):
        """딕셔너리에서 객체 생성"""
        return cls(
            hospital_id=data.get('hospital_id'),
            name=data.get('name'),
            address=data.get('address'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            medical_departments=data.get('medical_departments', [])
        )