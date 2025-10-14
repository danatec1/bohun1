"""
Hospital CRUD Repository
testdb.위탁병원현황 테이블에 직접 연결하는 CRUD 리포지토리
"""

import pymysql
from typing import List, Dict, Any, Optional

class HospitalCrudRepository:
    def __init__(self):
        self.connection_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'Admin1',
            'database': 'testdb',
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor
        }
    
    def _get_connection(self):
        """MySQL 연결 생성"""
        return pymysql.connect(**self.connection_config)
    
    def find_all_for_crud(self, search: str = '', filter_type: str = '') -> List[Dict[str, Any]]:
        """CRUD용 병원 목록 조회 (검색 및 필터링)"""
        hospitals = []
        
        with self._get_connection() as connection:
            with connection.cursor() as cursor:
                # 기본 쿼리
                query = 'SELECT * FROM 위탁병원현황 WHERE 1=1'
                params = []
                
                # 종별 필터링
                if filter_type:
                    query += ' AND 종별 = %s'
                    params.append(filter_type)
                
                # 검색어 필터링 (요양기관명, 주소, 상세주소, 전화번호)
                if search:
                    query += ' AND (요양기관명 LIKE %s OR 주소 LIKE %s OR 상세주소 LIKE %s OR 전화번호 LIKE %s)'
                    search_param = f'%{search}%'
                    params.extend([search_param, search_param, search_param, search_param])
                
                query += ' ORDER BY 연번'
                
                cursor.execute(query, params)
                rows = cursor.fetchall()
                
                for row in rows:
                    hospitals.append({
                        '연번': row['연번'],
                        '시군구': row['시군구'],
                        '요양기관명': row['요양기관명'],
                        '종별': row['종별'],
                        '병상수': row['병상수'],
                        '진료과수': row['진료과수'],
                        '전화번호': row['전화번호'],
                        '주소': row['주소'],
                        '상세주소': row['상세주소'] or '',
                        '경도': float(row['경도']) if row['경도'] else 0,
                        '위도': float(row['위도']) if row['위도'] else 0
                    })
        
        return hospitals
    
    def find_by_id(self, hospital_id: int) -> Optional[Dict[str, Any]]:
        """ID로 병원 조회"""
        with self._get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM 위탁병원현황 WHERE 연번 = %s', (hospital_id,))
                row = cursor.fetchone()
                
                if row:
                    return {
                        '연번': row['연번'],
                        '시군구': row['시군구'],
                        '요양기관명': row['요양기관명'],
                        '종별': row['종별'],
                        '병상수': row['병상수'],
                        '진료과수': row['진료과수'],
                        '전화번호': row['전화번호'],
                        '주소': row['주소'],
                        '상세주소': row['상세주소'] or '',
                        '경도': float(row['경도']) if row['경도'] else 0,
                        '위도': float(row['위도']) if row['위도'] else 0
                    }
                return None
    
    def create_crud(self, data: Dict[str, Any]) -> int:
        """병원 생성"""
        with self._get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO 위탁병원현황 
                    (시군구, 요양기관명, 종별, 병상수, 진료과수, 전화번호, 주소, 상세주소, 경도, 위도)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', (
                    data.get('시군구'),
                    data.get('요양기관명'),
                    data.get('종별'),
                    data.get('병상수'),
                    data.get('진료과수'),
                    data.get('전화번호'),
                    data.get('주소'),
                    data.get('상세주소'),
                    data.get('경도'),
                    data.get('위도')
                ))
                connection.commit()
                return cursor.lastrowid
    
    def update_crud(self, hospital_id: int, data: Dict[str, Any]) -> bool:
        """병원 수정"""
        with self._get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute('''
                    UPDATE 위탁병원현황 
                    SET 시군구 = %s, 요양기관명 = %s, 종별 = %s, 병상수 = %s, 
                        진료과수 = %s, 전화번호 = %s, 주소 = %s, 상세주소 = %s, 
                        경도 = %s, 위도 = %s
                    WHERE 연번 = %s
                ''', (
                    data.get('시군구'),
                    data.get('요양기관명'),
                    data.get('종별'),
                    data.get('병상수'),
                    data.get('진료과수'),
                    data.get('전화번호'),
                    data.get('주소'),
                    data.get('상세주소'),
                    data.get('경도'),
                    data.get('위도'),
                    hospital_id
                ))
                connection.commit()
                return cursor.rowcount > 0
    
    def delete_crud(self, hospital_id: int) -> bool:
        """병원 삭제"""
        with self._get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute('DELETE FROM 위탁병원현황 WHERE 연번 = %s', (hospital_id,))
                connection.commit()
                return cursor.rowcount > 0
