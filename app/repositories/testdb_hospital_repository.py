"""
TestDB MySQL Repository
testdb.위탁병원현황 테이블을 사용하는 병원 리포지토리
"""

import pymysql
import json
from typing import List, Optional
from ..models.hospital import Hospital

class TestDBHospitalRepository:
    def __init__(self, host='121.157.160.22', port=3306, user='root', password='zzaaqq', database='testdb'):
        self.connection_config = {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'database': database,
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor,
            'connect_timeout': 30
        }
        
    def _get_connection(self):
        """MySQL 연결 생성"""
        return pymysql.connect(**self.connection_config)
        
    def find_all(self) -> List[Hospital]:
        """위탁병원현황 테이블에서 모든 병원 조회"""
        hospitals = []
        try:
            with self._get_connection() as connection:
                with connection.cursor() as cursor:
                    # 위탁병원현황 테이블에서 데이터 조회 (공백 없음)
                    cursor.execute('SELECT * FROM `위탁병원현황`')
                    rows = cursor.fetchall()
                    
                    for i, row in enumerate(rows):
                        # 실제 테이블의 컬럼명에 맞게 매핑
                        hospital = Hospital(
                            hospital_id=row.get('연번', i + 1),
                            name=row.get('요양기관명', '알 수 없는 병원'),
                            address=f"{row.get('주소', '')} {row.get('상세주소', '')}".strip(),
                            latitude=self._safe_float(row.get('위도')),
                            longitude=self._safe_float(row.get('경도')),
                            medical_departments=[row.get('종별', '')],
                            bed_count=row.get('병상수'),
                            department_count=row.get('진료과수')
                        )
                        hospitals.append(hospital)
                        
        except Exception as e:
            print(f"데이터베이스 조회 오류: {e}")
            print("테이블 구조를 확인해주세요.")
            
        return hospitals
    
    def _safe_float(self, value):
        """안전한 float 변환"""
        if value is None:
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
    
    def _parse_departments(self, departments_str):
        """진료과목 문자열을 리스트로 변환"""
        if not departments_str:
            return []
        
        if isinstance(departments_str, str):
            # 쉼표, 세미콜론, 슬래시 등으로 구분된 문자열을 처리
            separators = [',', ';', '/', '|']
            for sep in separators:
                if sep in departments_str:
                    return [dept.strip() for dept in departments_str.split(sep) if dept.strip()]
            return [departments_str.strip()]
        
        return []
    
    def get_table_structure(self):
        """테이블 구조 확인용 메서드"""
        try:
            with self._get_connection() as connection:
                with connection.cursor() as cursor:
                    # 테이블 존재 확인
                    cursor.execute("SHOW TABLES LIKE %s", ('위탁병원현황',))
                    table_exists = cursor.fetchone()
                    
                    if not table_exists:
                        return {
                            'table_name': '위탁병원현황',
                            'exists': False,
                            'error': 'Table does not exist'
                        }
                    
                    # 테이블 컬럼 정보 조회
                    cursor.execute('DESCRIBE `위탁병원현황`')
                    columns = cursor.fetchall()
                    
                    # 테이블 데이터 개수 확인
                    cursor.execute('SELECT COUNT(*) as count FROM `위탁병원현황`')
                    count_result = cursor.fetchone()
                    row_count = count_result['count'] if count_result else 0
                    
                    # 샘플 데이터 확인 (최대 3개)
                    cursor.execute('SELECT * FROM `위탁병원현황` LIMIT 3')
                    sample_data = cursor.fetchall()
                    
                    return {
                        'table_name': '위탁병원현황',
                        'exists': True,
                        'columns': columns,
                        'row_count': row_count,
                        'sample_data': sample_data
                    }
        except Exception as e:
            print(f"테이블 구조 조회 오류: {e}")
            return {
                'table_name': '위탁병원현황',
                'columns': [],
                'error': str(e)
            }
    
    def get_all_tables(self):
        """testdb의 모든 테이블 목록 조회"""
        try:
            with self._get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute('SHOW TABLES')
                    tables = cursor.fetchall()
                    
                    table_list = []
                    for table in tables:
                        table_name = list(table.values())[0]  # 첫 번째 값이 테이블명
                        
                        # 각 테이블의 행 수 확인
                        try:
                            cursor.execute(f'SELECT COUNT(*) as count FROM `{table_name}`')
                            count_result = cursor.fetchone()
                            row_count = count_result['count'] if count_result else 0
                        except:
                            row_count = 0
                        
                        table_list.append({
                            'name': table_name,
                            'row_count': row_count
                        })
                    
                    return {
                        'database': 'testdb',
                        'tables': table_list
                    }
        except Exception as e:
            print(f"테이블 목록 조회 오류: {e}")
            return {
                'database': 'testdb',
                'tables': [],
                'error': str(e)
            }

    # 기본적인 CRUD 메서드들 (필요시 구현)
    def find_by_id(self, hospital_id: int) -> Optional[Hospital]:
        """ID로 병원 검색 (구현 필요)"""
        hospitals = self.find_all()
        for hospital in hospitals:
            if hospital.hospital_id == hospital_id:
                return hospital
        return None
    
    def create(self, hospital: Hospital) -> int:
        """병원 정보 생성 (구현 필요)"""
        # testdb는 읽기 전용으로 사용하는 경우가 많으므로 구현하지 않음
        raise NotImplementedError("TestDB는 읽기 전용입니다.")
    
    def update(self, hospital: Hospital) -> bool:
        """병원 정보 수정 (구현 필요)"""
        raise NotImplementedError("TestDB는 읽기 전용입니다.")
    
    def delete(self, hospital_id: int) -> bool:
        """병원 정보 삭제 (구현 필요)"""
        raise NotImplementedError("TestDB는 읽기 전용입니다.")
    
    def get_yearly_statistics(self):
        """위탁병원현황_연도별현황 테이블에서 연도별 통계 조회"""
        try:
            with self._get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT * FROM `위탁병원현황_연도별현황`')
                    rows = cursor.fetchall()
                    return rows
        except Exception as e:
            print(f"연도별 통계 조회 오류: {e}")
            return []
    
    def find_all_for_crud(self, search: str = '', filter_type: str = '') -> List[dict]:
        """CRUD용 병원 목록 조회 (검색 및 필터링 지원)"""
        hospitals = []
        try:
            with self._get_connection() as connection:
                with connection.cursor() as cursor:
                    # 기본 쿼리
                    query = 'SELECT * FROM `위탁병원현황` WHERE 1=1'
                    params = []
                    
                    # 검색어 처리
                    if search:
                        query += ''' AND (
                            `요양기관명` LIKE %s OR
                            `시군구` LIKE %s OR
                            `주소` LIKE %s OR
                            `전화번호` LIKE %s
                        )'''
                        search_pattern = f'%{search}%'
                        params.extend([search_pattern] * 4)
                    
                    # 종별 필터
                    if filter_type:
                        query += ' AND `종별` = %s'
                        params.append(filter_type)
                    
                    query += ' ORDER BY `연번`'
                    
                    cursor.execute(query, params)
                    rows = cursor.fetchall()
                    
                    for row in rows:
                        hospitals.append({
                            '연번': row.get('연번'),
                            '시군구': row.get('시군구', ''),
                            '요양기관명': row.get('요양기관명', ''),
                            '종별': row.get('종별', ''),
                            '병상수': row.get('병상수', 0),
                            '진료과수': row.get('진료과수', 0),
                            '전화번호': row.get('전화번호', ''),
                            '주소': row.get('주소', ''),
                            '상세주소': row.get('상세주소', ''),
                            '경도': float(row.get('경도')) if row.get('경도') else 0,
                            '위도': float(row.get('위도')) if row.get('위도') else 0
                        })
        except Exception as e:
            print(f"CRUD 조회 오류: {e}")
        
        return hospitals
    
    def create_crud(self, data: dict) -> int:
        """CRUD용 병원 생성"""
        try:
            with self._get_connection() as connection:
                with connection.cursor() as cursor:
                    query = '''
                        INSERT INTO `위탁병원현황`
                        (`시군구`, `요양기관명`, `종별`, `병상수`, `진료과수`, 
                         `전화번호`, `주소`, `상세주소`, `경도`, `위도`)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    '''
                    cursor.execute(query, (
                        data.get('시군구'),
                        data.get('요양기관명'),
                        data.get('종별'),
                        data.get('병상수'),
                        data.get('진료과수'),
                        data.get('전화번호'),
                        data.get('주소'),
                        data.get('상세주소', ''),
                        data.get('경도'),
                        data.get('위도')
                    ))
                    connection.commit()
                    return cursor.lastrowid
        except Exception as e:
            print(f"CRUD 생성 오류: {e}")
            raise
    
    def update_crud(self, hospital_id: int, data: dict) -> bool:
        """CRUD용 병원 수정"""
        try:
            with self._get_connection() as connection:
                with connection.cursor() as cursor:
                    query = '''
                        UPDATE `위탁병원현황`
                        SET `시군구` = %s, `요양기관명` = %s, `종별` = %s,
                            `병상수` = %s, `진료과수` = %s, `전화번호` = %s,
                            `주소` = %s, `상세주소` = %s, `경도` = %s, `위도` = %s
                        WHERE `연번` = %s
                    '''
                    cursor.execute(query, (
                        data.get('시군구'),
                        data.get('요양기관명'),
                        data.get('종별'),
                        data.get('병상수'),
                        data.get('진료과수'),
                        data.get('전화번호'),
                        data.get('주소'),
                        data.get('상세주소', ''),
                        data.get('경도'),
                        data.get('위도'),
                        hospital_id
                    ))
                    connection.commit()
                    return cursor.rowcount > 0
        except Exception as e:
            print(f"CRUD 수정 오류: {e}")
            raise
    
    def delete_crud(self, hospital_id: int) -> bool:
        """CRUD용 병원 삭제"""
        try:
            with self._get_connection() as connection:
                with connection.cursor() as cursor:
                    query = 'DELETE FROM `위탁병원현황` WHERE `연번` = %s'
                    cursor.execute(query, (hospital_id,))
                    connection.commit()
                    return cursor.rowcount > 0
        except Exception as e:
            print(f"CRUD 삭제 오류: {e}")
            raise
