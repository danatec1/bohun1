"""
Configuration Settings
애플리케이션 환경별 설정
"""

import os
from pathlib import Path

# 기본 경로 설정
BASE_DIR = Path(__file__).resolve().parent

class Config:
    """기본 설정"""
    
    # 데이터베이스 설정
    DATABASE_PATH = os.environ.get('DATABASE_PATH') or os.path.join(BASE_DIR, 'hospital.db')
    
    # 보안 설정
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # 로깅 설정
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    LOG_FILE = os.environ.get('LOG_FILE') or os.path.join(BASE_DIR, 'logs', 'app.log')
    
    # API 설정
    JSON_AS_ASCII = False  # 한글 지원을 위해
    JSONIFY_PRETTYPRINT_REGULAR = True
    
    # 업로드 설정
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    
class DevelopmentConfig(Config):
    """개발 환경 설정"""
    DEBUG = True
    TESTING = False
    
    # 개발용 데이터베이스
    DATABASE_PATH = os.path.join(BASE_DIR, 'hospital_dev.db')

class ProductionConfig(Config):
    """운영 환경 설정"""
    DEBUG = False
    TESTING = False
    
    # 운영 환경에서는 환경변수에서 가져오도록
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'production-secret-key-change-me'
    DATABASE_PATH = os.environ.get('DATABASE_PATH') or os.path.join(BASE_DIR, 'hospital_prod.db')

class TestingConfig(Config):
    """테스트 환경 설정"""
    DEBUG = True
    TESTING = True
    
    # 테스트용 인메모리 데이터베이스
    DATABASE_PATH = ':memory:'

# 환경별 설정 매핑
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}