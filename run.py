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
    
    # 소켓 재사용 옵션 설정 (TIME_WAIT 문제 해결)
    import socket
    if hasattr(socket, 'SO_REUSEADDR'):
        app.config['SOCK_OPT_SO_REUSEADDR'] = 1
    
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),  # 포트 80 → 5000으로 변경
        debug=debug,
        use_reloader=True,
        threaded=True
    )
