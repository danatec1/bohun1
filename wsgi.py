"""
WSGI Entry Point
운영 환경에서 사용할 WSGI 파일
"""

from app import create_app
import os

# 운영 환경 설정
os.environ['FLASK_ENV'] = 'production'

# Flask 애플리케이션 생성
app = create_app('production')

if __name__ == '__main__':
    app.run()
