"""
Hospital Repository
병원 데이터 접근을 담당하는 리포지토리
"""

import sqlite3
import json
from typing import List, Optional
from ..models.hospital import Hospital

class HospitalRepository:
    def __init__(self, db_path: str = 'hospital.db'):
        self.db_path = db_path
        self._init_database()
        
    def _init_database(self):
        """데이터베이스 초기화"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS hospitals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    address TEXT,
                    latitude REAL,
                    longitude REAL,
                    medical_departments TEXT
                )
            ''')
            conn.commit()
            
    def create(self, hospital: Hospital) -> int:
        """병원 정보 생성"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO hospitals (name, address, latitude, longitude, medical_departments)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                hospital.name,
                hospital.address,
                hospital.latitude,
                hospital.longitude,
                json.dumps(hospital.medical_departments, ensure_ascii=False)
            ))
            conn.commit()
            return cursor.lastrowid
            
    def find_by_id(self, hospital_id: int) -> Optional[Hospital]:
        """ID로 병원 검색"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM hospitals WHERE id = ?', (hospital_id,))
            row = cursor.fetchone()
            
            if row:
                return Hospital(
                    hospital_id=row[0],
                    name=row[1],
                    address=row[2],
                    latitude=row[3],
                    longitude=row[4],
                    medical_departments=json.loads(row[5]) if row[5] else []
                )
            return None
            
    def find_all(self) -> List[Hospital]:
        """모든 병원 조회"""
        hospitals = []
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM hospitals')
            rows = cursor.fetchall()
            
            for row in rows:
                hospitals.append(Hospital(
                    hospital_id=row[0],
                    name=row[1],
                    address=row[2],
                    latitude=row[3],
                    longitude=row[4],
                    medical_departments=json.loads(row[5]) if row[5] else []
                ))
                
        return hospitals
        
    def update(self, hospital: Hospital) -> bool:
        """병원 정보 수정"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE hospitals 
                SET name = ?, address = ?, latitude = ?, longitude = ?, medical_departments = ?
                WHERE id = ?
            ''', (
                hospital.name,
                hospital.address,
                hospital.latitude,
                hospital.longitude,
                json.dumps(hospital.medical_departments, ensure_ascii=False),
                hospital.hospital_id
            ))
            conn.commit()
            return cursor.rowcount > 0
            
    def delete(self, hospital_id: int) -> bool:
        """병원 정보 삭제"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM hospitals WHERE id = ?', (hospital_id,))
            conn.commit()
            return cursor.rowcount > 0