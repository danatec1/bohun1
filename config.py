"""
Configuration Settings
애플리케이션 환경별 설정
"""

import os

class Config:
    """기본 설정"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False
    
    # MySQL 설정
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'Admin1')
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'testdb')
    
class DevelopmentConfig(Config):
    """개발 환경 설정"""
    DEBUG = True
    
class ProductionConfig(Config):
    """운영 환경 설정"""
    DEBUG = False
    # 운영 환경에서는 반드시 환경 변수로 설정할 것
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # 보안 강화
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
class TestingConfig(Config):
    """테스트 환경 설정"""
    TESTING = True
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
