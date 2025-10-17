"""
Production Server Runner
Waitress WSGI 서버를 사용한 운영 환경 실행 파일
"""

from waitress import serve
from app import create_app
import os

# 운영 환경 설정
os.environ['FLASK_ENV'] = 'production'

# Flask 애플리케이션 생성
app = create_app('production')

if __name__ == '__main__':
    print('=' * 60)
    print('🚀 보훈 병원 관리 시스템 - 운영 서버 시작')
    print('=' * 60)
    print(f'📍 서버 주소: http://0.0.0.0:5001')
    print(f'🌐 로컬 접속: http://127.0.0.1:5001')
    print(f'🔒 환경: Production')
    print(f'⚙️  스레드: 4')
    print('=' * 60)
    print('⚠️  서버를 종료하려면 Ctrl+C를 누르세요')
    print('=' * 60)
    
    # Waitress 서버 실행
    # threads=4: 4개의 스레드로 동시 요청 처리
    # host='0.0.0.0': 모든 네트워크 인터페이스에서 접속 허용
    # PORT 환경변수 지원 추가 (기본값 5211)
    port = int(os.environ.get('PORT', 5211))

    serve(
        app,
        host='0.0.0.0',
        port=port,
        threads=4,
        url_scheme='http'
    )
