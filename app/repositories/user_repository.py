"""
User Repository
사용자 데이터베이스 작업을 처리하는 리포지토리
"""

import pymysql
import os
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Optional
from ..models.user import User


class UserRepository:
    def __init__(self, host='localhost', user='root',
                 password=None, database='testdb'):
        # 환경변수에서 MySQL 비밀번호 가져오기 (기본값: zzaaqq)
        if password is None:
            password = os.environ.get('MYSQL_PASSWORD', 'zzaaqq')
        self.connection_config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database,
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor
        }
        self._create_table_if_not_exists()

    def _get_connection(self):
        """MySQL 연결 생성"""
        return pymysql.connect(**self.connection_config)

    def _create_table_if_not_exists(self):
        """users 테이블이 없으면 생성"""
        try:
            with self._get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS users (
                            user_id INT AUTO_INCREMENT PRIMARY KEY,
                            username VARCHAR(50) UNIQUE NOT NULL,
                            email VARCHAR(100) UNIQUE NOT NULL,
                            password_hash VARCHAR(255) NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                    """)
                    connection.commit()
                    print("✅ users 테이블 확인/생성 완료")
        except Exception as e:
            print(f"❌ users 테이블 생성 오류: {e}")

    def create_user(self, username: str, email: str,
                    password: str) -> Optional[int]:
        """새 사용자 생성"""
        try:
            password_hash = generate_password_hash(password)
            with self._get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO users (username, email, password_hash)
                        VALUES (%s, %s, %s)
                    """, (username, email, password_hash))
                    connection.commit()
                    return cursor.lastrowid
        except pymysql.err.IntegrityError as e:
            print(f"중복된 사용자명 또는 이메일: {e}")
            return None
        except Exception as e:
            print(f"사용자 생성 오류: {e}")
            return None

    def find_by_username(self, username: str) -> Optional[User]:
        """사용자명으로 사용자 조회"""
        try:
            with self._get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT * FROM users WHERE username = %s
                    """, (username,))
                    row = cursor.fetchone()
                    if row:
                        return User(
                            user_id=row['user_id'],
                            username=row['username'],
                            email=row['email'],
                            password_hash=row['password_hash'],
                            created_at=row['created_at']
                        )
                    return None
        except Exception as e:
            print(f"사용자 조회 오류: {e}")
            return None

    def find_by_id(self, user_id: int) -> Optional[User]:
        """ID로 사용자 조회"""
        try:
            with self._get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT * FROM users WHERE user_id = %s
                    """, (user_id,))
                    row = cursor.fetchone()
                    if row:
                        return User(
                            user_id=row['user_id'],
                            username=row['username'],
                            email=row['email'],
                            password_hash=row['password_hash'],
                            created_at=row['created_at']
                        )
                    return None
        except Exception as e:
            print(f"사용자 조회 오류: {e}")
            return None

    def verify_password(self, user: User, password: str) -> bool:
        """비밀번호 검증"""
        return check_password_hash(user.password_hash, password)

    def get_all_users(self):
        """모든 사용자 조회 (관리자용)"""
        try:
            with self._get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT user_id, username, email, created_at
                        FROM users ORDER BY created_at DESC
                    """)
                    return cursor.fetchall()
        except Exception as e:
            print(f"사용자 목록 조회 오류: {e}")
            return []
