# 프로덕션 서버 실행 스크립트
# Waitress WSGI 서버 사용

from waitress import serve
from app import create_app
import os

app = create_app()
app.config['DEBUG'] = False

port = int(os.environ.get('PORT', 5000))
print(' 프로덕션 서버 시작: http://0.0.0.0:' + str(port) + '/c')
serve(app, host='0.0.0.0', port=port, threads=8)
