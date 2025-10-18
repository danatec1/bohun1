#!/usr/bin/env python3
"""
MySQL 연결 테스트 스크립트
Windows Server에서 MySQL 비밀번호를 확인하고 연결을 테스트합니다.
"""

import pymysql
import os
import getpass

def test_mysql_connection():
    print("=== MySQL 연결 테스트 ===")
    
    # 현재 환경변수 확인
    env_password = os.environ.get('MYSQL_PASSWORD')
    if env_password:
        print(f"환경변수 MYSQL_PASSWORD: 설정됨 (길이: {len(env_password)})")
    else:
        print("환경변수 MYSQL_PASSWORD: 설정되지 않음")
        print("현재 기본값 'zzaaqq'를 사용합니다.")
    
    # 테스트할 비밀번호들
    passwords_to_test = []
    
    if env_password:
        passwords_to_test.append(("환경변수", env_password))
    
    passwords_to_test.extend([
        ("기본값", "zzaaqq"),
        ("이전 기본값", "1234"),
        ("공백", ""),
        ("root", "root")
    ])
    
    # 수동 입력 옵션
    manual_password = input("\n수동으로 비밀번호를 입력하시겠습니까? (y/n): ").lower()
    if manual_password == 'y':
        custom_pw = getpass.getpass("MySQL 비밀번호 입력: ")
        passwords_to_test.insert(0, ("수동입력", custom_pw))
    
    print("\n=== 연결 테스트 시작 ===")
    
    for desc, password in passwords_to_test:
        try:
            print(f"\n[{desc}] 테스트 중...")
            
            connection = pymysql.connect(
                host='localhost',
                user='root',
                password=password,
                database='testdb',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            
            print(f"✅ [{desc}] 연결 성공!")
            
            # 간단한 쿼리 테스트
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) as count FROM 위탁병원현황")
                result = cursor.fetchone()
                print(f"   위탁병원현황 테이블 레코드 수: {result['count']}")
            
            connection.close()
            
            # 성공한 비밀번호로 환경변수 설정 안내
            print(f"\n🎉 성공! 다음 명령어로 환경변수를 설정하세요:")
            print(f"$env:MYSQL_PASSWORD = \"{password}\"")
            return password
            
        except Exception as e:
            print(f"❌ [{desc}] 연결 실패: {e}")
    
    print("\n⚠️  모든 비밀번호 테스트 실패")
    print("MySQL 서버 상태를 확인해주세요:")
    print("1. MySQL 서비스가 실행 중인지 확인")
    print("2. root 계정의 비밀번호 확인")
    print("3. testdb 데이터베이스 존재 여부 확인")
    
    return None

if __name__ == "__main__":
    test_mysql_connection()
