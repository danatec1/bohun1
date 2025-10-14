#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySQL testdb 연결 및 테이블 구조 확인 스크립트
"""

import pymysql
import json

def check_mysql_connection():
    """MySQL 연결 테스트"""
    connection_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'Admin1',
        'database': 'testdb',
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor
    }
    
    try:
        print("MySQL 연결 시도...")
        connection = pymysql.connect(**connection_config)
        print("✅ MySQL 연결 성공!")
        
        with connection.cursor() as cursor:
            # 데이터베이스 목록 확인
            print("\n📋 데이터베이스 목록:")
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
            for db in databases:
                print(f"  - {list(db.values())[0]}")
            
            # testdb 선택
            cursor.execute("USE testdb")
            
            # 테이블 목록 확인
            print("\n📋 testdb의 테이블 목록:")
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            if not tables:
                print("  테이블이 없습니다.")
                return
            
            for table in tables:
                table_name = list(table.values())[0]
                print(f"  - {table_name}")
                
                # 각 테이블의 구조 확인
                try:
                    cursor.execute(f"DESCRIBE `{table_name}`")
                    columns = cursor.fetchall()
                    print(f"    컬럼 수: {len(columns)}")
                    
                    # 데이터 개수 확인
                    cursor.execute(f"SELECT COUNT(*) as count FROM `{table_name}`")
                    count_result = cursor.fetchone()
                    row_count = count_result['count'] if count_result else 0
                    print(f"    데이터 행 수: {row_count}")
                    
                    # 컬럼 정보 출력
                    if columns:
                        print(f"    컬럼:")
                        for col in columns:
                            print(f"      - {col['Field']} ({col['Type']})")
                    
                    # 샘플 데이터 확인 (최대 2개)
                    if row_count > 0:
                        cursor.execute(f"SELECT * FROM `{table_name}` LIMIT 2")
                        sample_data = cursor.fetchall()
                        print(f"    샘플 데이터:")
                        for i, row in enumerate(sample_data, 1):
                            print(f"      행 {i}: {dict(row)}")
                    
                    print()
                    
                except Exception as e:
                    print(f"    ❌ 테이블 '{table_name}' 조회 실패: {e}")
        
        connection.close()
        print("✅ MySQL 연결 종료")
        
    except Exception as e:
        print(f"❌ MySQL 연결 실패: {e}")

if __name__ == "__main__":
    check_mysql_connection()
