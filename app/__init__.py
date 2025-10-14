"""
Flask Application Factory
Flask 애플리케이션을 생성하고 설정하는 팩토리 함수
"""

from flask import Flask
from .routes import register_routes
import os
from datetime import timedelta

def create_app(config_name='development'):
    """Flask 애플리케이션 생성 및 설정"""
    
    # Flask 애플리케이션 인스턴스 생성
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='../public',
                static_url_path='/static')
    
    # 설정 로드
    app.config.from_object(f'config.{config_name.title()}Config')
    
    # 비밀 키 설정 (세션, CSRF 등을 위해)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # 세션 설정
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    
    # 라우트 등록
    register_routes(app)
    
    # 에러 핸들러 등록
    register_error_handlers(app)
    
    # 컨텍스트 프로세서 등록
    register_context_processors(app)
    
    return app

def register_error_handlers(app):
    """에러 핸들러 등록"""
    
    @app.errorhandler(404)
    def not_found(error):
        return {'error': '페이지를 찾을 수 없습니다'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'error': '서버 내부 오류가 발생했습니다'}, 500

def register_context_processors(app):
    """템플릿 컨텍스트 프로세서 등록"""
    
    @app.context_processor
    def utility_processor():
        """템플릿에서 사용할 유틸리티 함수들"""
        return {
            'enumerate': enumerate,
            'len': len,
            'str': str,
            'int': int
        }