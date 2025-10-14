"""
Application Entry Point
Flask 애플리케이션 실행 파일
"""

from app import create_app
import os

# 환경 설정 (기본값: development)
config_name = os.environ.get('FLASK_ENV') or 'development'

# Flask 애플리케이션 생성
app = create_app(config_name)

if __name__ == '__main__':
    # 개발 서버 실행
    debug = config_name == 'development'
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5001)),
        debug=debug
    )