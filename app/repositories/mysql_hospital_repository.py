"""
MySQL Database Repository
MySQL 데이터베이스를 사용하는 병원 리포지토리
"""

import pymysql
import json
from typing import List, Optional
from ..models.hospital import Hospital

class MySQLHospitalRepository:
    def __init__(self, host='localhost', user='root', password='Admin1', database='bohun_hospital'):
        self.connection_config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database,
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor
        }
        self._init_database()
        
    def _get_connection(self):
        """MySQL 연결 생성"""
        return pymysql.connect(**self.connection_config)
        
    def _init_database(self):
        """데이터베이스 및 테이블 초기화"""
        try:
            # 데이터베이스가 없으면 생성
            temp_config = self.connection_config.copy()
            del temp_config['database']
            
            with pymysql.connect(**temp_config) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.connection_config['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                    connection.commit()
            
            # 테이블 생성
            with self._get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute('''
                        CREATE TABLE IF NOT EXISTS hospitals (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            name VARCHAR(255) NOT NULL,
                            address TEXT,
                            latitude DECIMAL(10, 8),
                            longitude DECIMAL(11, 8),
                            medical_departments JSON,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                    ''')
                    connection.commit()
                    
        except Exception as e:
            print(f"데이터베이스 초기화 오류: {e}")
            
    def create(self, hospital: Hospital) -> int:
        """병원 정보 생성"""
        with self._get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO hospitals (name, address, latitude, longitude, medical_departments)
                    VALUES (%s, %s, %s, %s, %s)
                ''', (
                    hospital.name,
                    hospital.address,
                    hospital.latitude,
                    hospital.longitude,
                    json.dumps(hospital.medical_departments, ensure_ascii=False)
                ))
                connection.commit()
                return cursor.lastrowid
                
    def find_by_id(self, hospital_id: int) -> Optional[Hospital]:
        """ID로 병원 검색"""
        with self._get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM hospitals WHERE id = %s', (hospital_id,))
                row = cursor.fetchone()
                
                if row:
                    return Hospital(
                        hospital_id=row['id'],
                        name=row['name'],
                        address=row['address'],
                        latitude=float(row['latitude']) if row['latitude'] else None,
                        longitude=float(row['longitude']) if row['longitude'] else None,
                        medical_departments=json.loads(row['medical_departments']) if row['medical_departments'] else []
                    )
                return None
                
    def find_all(self) -> List[Hospital]:
        """모든 병원 조회"""
        hospitals = []
        with self._get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM hospitals ORDER BY name')
                rows = cursor.fetchall()
                
                for row in rows:
                    hospitals.append(Hospital(
                        hospital_id=row['id'],
                        name=row['name'],
                        address=row['address'],
                        latitude=float(row['latitude']) if row['latitude'] else None,
                        longitude=float(row['longitude']) if row['longitude'] else None,
                        medical_departments=json.loads(row['medical_departments']) if row['medical_departments'] else []
                    ))
                    
        return hospitals
        
    def update(self, hospital: Hospital) -> bool:
        """병원 정보 수정"""
        with self._get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute('''
                    UPDATE hospitals 
                    SET name = %s, address = %s, latitude = %s, longitude = %s, medical_departments = %s
                    WHERE id = %s
                ''', (
                    hospital.name,
                    hospital.address,
                    hospital.latitude,
                    hospital.longitude,
                    json.dumps(hospital.medical_departments, ensure_ascii=False),
                    hospital.hospital_id
                ))
                connection.commit()
                return cursor.rowcount > 0
                
    def delete(self, hospital_id: int) -> bool:
        """병원 정보 삭제"""
        with self._get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute('DELETE FROM hospitals WHERE id = %s', (hospital_id,))
                connection.commit()
                return cursor.rowcount > 0