# 🔧 위탁병원 관리 시스템 환경설정 가이드

## 📋 목차
1. [데이터베이스 연결 설정](#데이터베이스-연결-설정)
2. [Flask 애플리케이션 설정](#flask-애플리케이션-설정)
3. [포트 및 호스트 설정](#포트-및-호스트-설정)
4. [보안 설정](#보안-설정)
5. [성능 최적화](#성능-최적화)
6. [로깅 설정](#로깅-설정)
7. [환경별 설정](#환경별-설정)

---

## 🗄️ 데이터베이스 연결 설정

### 1. MySQL 연결 정보 변경

시스템에서 MySQL 연결을 사용하는 파일들:

#### `app/repositories/testdb_hospital_repository.py`
```python
class TestDBHospitalRepository:
    def __init__(self):
        self.connection_config = {
            'host': 'localhost',        # MySQL 서버 주소
            'user': 'root',             # MySQL 사용자명
            'password': 'Admin1',       # MySQL 비밀번호
            'database': 'testdb',       # 데이터베이스 이름
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor
        }
```

#### `app/repositories/hospital_crud_repository.py`
```python
class HospitalCrudRepository:
    def __init__(self):
        self.connection_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'Admin1',
            'database': 'testdb',
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor
        }
```

#### `app/repositories/user_repository.py`
```python
class UserRepository:
    def __init__(self):
        self.connection_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'Admin1',
            'database': 'testdb',
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor
        }
```

### 2. 환경변수 사용 (권장)

보안을 위해 환경변수로 관리하는 방법:

#### `.env` 파일 생성
```bash
# 프로젝트 루트에 .env 파일 생성
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=Admin1
DB_NAME=testdb
DB_CHARSET=utf8mb4
```

#### 코드 수정
```python
import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일 로드

class TestDBHospitalRepository:
    def __init__(self):
        self.connection_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', 3306)),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'database': os.getenv('DB_NAME', 'testdb'),
            'charset': os.getenv('DB_CHARSET', 'utf8mb4'),
            'cursorclass': pymysql.cursors.DictCursor
        }
```

#### 패키지 설치
```bash
pip install python-dotenv
```

### 3. 원격 MySQL 서버 연결

```python
self.connection_config = {
    'host': '192.168.1.100',    # 원격 서버 IP
    'port': 3306,
    'user': 'bohun_user',
    'password': 'SecurePassword123!',
    'database': 'testdb',
    'charset': 'utf8mb4',
    'connect_timeout': 10,      # 연결 타임아웃 (초)
    'cursorclass': pymysql.cursors.DictCursor
}
```

#### MySQL 원격 접속 허용 설정
```sql
-- MySQL에서 원격 사용자 생성
CREATE USER 'bohun_user'@'%' IDENTIFIED BY 'SecurePassword123!';
GRANT ALL PRIVILEGES ON testdb.* TO 'bohun_user'@'%';
FLUSH PRIVILEGES;
```

```ini
# my.ini (Windows) 또는 my.cnf (Linux) 수정
[mysqld]
bind-address = 0.0.0.0  # 모든 IP에서 접속 허용
```

---

## ⚙️ Flask 애플리케이션 설정

### 1. 기본 설정 (`app/__init__.py`)

```python
from flask import Flask
from datetime import timedelta
import os

def create_app():
    app = Flask(__name__, 
                static_folder='../public',
                static_url_path='/static')
    
    # 기본 설정
    app.config['DEBUG'] = True  # 프로덕션에서는 False
    app.config['TESTING'] = False
    
    # 세션 설정
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_SECURE'] = False  # HTTPS에서는 True
    
    # 파일 업로드 설정
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
    
    # JSON 설정
    app.config['JSON_AS_ASCII'] = False  # 한글 깨짐 방지
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    
    return app
```

### 2. 환경별 설정 파일

#### `config/development.py`
```python
class DevelopmentConfig:
    DEBUG = True
    TESTING = False
    SECRET_KEY = 'dev-secret-key-change-in-production'
    
    # MySQL 설정
    DB_HOST = 'localhost'
    DB_USER = 'root'
    DB_PASSWORD = 'Admin1'
    DB_NAME = 'testdb'
    
    # 세션 설정
    PERMANENT_SESSION_LIFETIME = 86400 * 7  # 7일
    SESSION_COOKIE_SECURE = False
```

#### `config/production.py`
```python
import secrets

class ProductionConfig:
    DEBUG = False
    TESTING = False
    SECRET_KEY = secrets.token_hex(32)  # 랜덤 생성
    
    # MySQL 설정 (환경변수에서)
    DB_HOST = os.environ.get('DB_HOST')
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_NAME = os.environ.get('DB_NAME')
    
    # 보안 강화
    SESSION_COOKIE_SECURE = True  # HTTPS 필수
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Strict'
    PERMANENT_SESSION_LIFETIME = 7200  # 2시간
```

#### 설정 로드
```python
from config.development import DevelopmentConfig
from config.production import ProductionConfig

def create_app(config_name='development'):
    app = Flask(__name__)
    
    if config_name == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)
    
    return app
```

---

## 🌐 포트 및 호스트 설정

### 1. 기본 설정 변경 (`run.py`)

```python
from app import create_app

app = create_app()

if __name__ == '__main__':
    # 개발 환경
    app.run(
        host='0.0.0.0',      # 모든 네트워크 인터페이스
        port=5001,           # 포트 번호
        debug=True,          # 디버그 모드
        threaded=True        # 멀티스레드 활성화
    )
```

### 2. 환경변수로 설정

```python
import os

if __name__ == '__main__':
    app.run(
        host=os.environ.get('FLASK_HOST', '0.0.0.0'),
        port=int(os.environ.get('FLASK_PORT', 5001)),
        debug=os.environ.get('FLASK_DEBUG', 'True') == 'True'
    )
```

#### `.env` 파일
```bash
FLASK_HOST=0.0.0.0
FLASK_PORT=5001
FLASK_DEBUG=True
```

### 3. 포트 변경 시 주의사항

포트를 변경한 경우 다음 파일들도 업데이트:
- README.md
- 문서의 모든 URL 예시
- 방화벽 규칙

---

## 🔒 보안 설정

### 1. SECRET_KEY 생성

```python
# Python 인터프리터에서 실행
import secrets
print(secrets.token_hex(32))
# 출력: a5d8f7e9c3b2a1f0e4d8c7b6a5f4e3d2c1b0a9f8e7d6c5b4a3f2e1d0c9b8a7f6
```

`app/__init__.py`에 적용:
```python
app.config['SECRET_KEY'] = 'a5d8f7e9c3b2a1f0e4d8c7b6a5f4e3d2c1b0a9f8e7d6c5b4a3f2e1d0c9b8a7f6'
```

### 2. HTTPS 설정 (SSL/TLS)

#### 자체 서명 인증서 (개발용)
```bash
# 인증서 생성
openssl req -x509 -newkey rsa:4096 -nodes \
    -out cert.pem -keyout key.pem -days 365
```

```python
# run.py
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5001,
        ssl_context=('cert.pem', 'key.pem')  # HTTPS
    )
```

#### Let's Encrypt (프로덕션)
Nginx/Apache 리버스 프록시 사용 권장

### 3. CORS 설정 (필요시)

```bash
pip install flask-cors
```

```python
from flask_cors import CORS

app = create_app()
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://yourdomain.com"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type"]
    }
})
```

### 4. 비밀번호 정책

`app/repositories/user_repository.py`:
```python
def create_user(self, username, email, password):
    # 비밀번호 강도 검증
    if len(password) < 8:
        raise ValueError("비밀번호는 최소 8자 이상이어야 합니다")
    
    if not any(c.isupper() for c in password):
        raise ValueError("비밀번호에 대문자가 포함되어야 합니다")
    
    if not any(c.isdigit() for c in password):
        raise ValueError("비밀번호에 숫자가 포함되어야 합니다")
    
    # 해시 생성 (강화된 해시)
    password_hash = generate_password_hash(
        password, 
        method='pbkdf2:sha256',
        salt_length=16
    )
```

---

## ⚡ 성능 최적화

### 1. MySQL 연결 풀링

```bash
pip install DBUtils
```

```python
from DBUtils.PooledDB import PooledDB
import pymysql

class HospitalRepository:
    _pool = None
    
    @classmethod
    def get_pool(cls):
        if cls._pool is None:
            cls._pool = PooledDB(
                creator=pymysql,
                maxconnections=10,      # 최대 연결 수
                mincached=2,            # 최소 캐시 연결
                maxcached=5,            # 최대 캐시 연결
                blocking=True,          # 연결 대기
                host='localhost',
                user='root',
                password='Admin1',
                database='testdb',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        return cls._pool
    
    def _get_connection(self):
        return self.get_pool().connection()
```

### 2. MySQL 쿼리 최적화

#### 인덱스 추가
```sql
-- 자주 검색하는 컬럼에 인덱스 생성
CREATE INDEX idx_hospital_name ON 위탁병원현황(요양기관명);
CREATE INDEX idx_hospital_type ON 위탁병원현황(종별);
CREATE INDEX idx_hospital_location ON 위탁병원현황(시군구);

-- 복합 인덱스
CREATE INDEX idx_location_type ON 위탁병원현황(시군구, 종별);

-- 인덱스 확인
SHOW INDEX FROM 위탁병원현황;
```

#### 쿼리 실행 계획 확인
```sql
EXPLAIN SELECT * FROM 위탁병원현황 WHERE 종별 = '종합병원';
```

### 3. Flask 캐싱

```bash
pip install Flask-Caching
```

```python
from flask_caching import Cache

app = create_app()
cache = Cache(app, config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300  # 5분
})

@app.route('/api/hospitals')
@cache.cached(timeout=60)  # 1분 캐시
def get_hospitals():
    # 병원 데이터 조회
    return jsonify(hospitals)
```

### 4. Gzip 압축

```bash
pip install Flask-Compress
```

```python
from flask_compress import Compress

app = create_app()
Compress(app)
```

---

## 📝 로깅 설정

### 1. 기본 로깅

```python
import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(app):
    # 로그 디렉토리 생성
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    # 파일 핸들러
    file_handler = RotatingFileHandler(
        'logs/bohun1.log',
        maxBytes=10240000,  # 10MB
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Bohun Hospital System startup')

# app/__init__.py
app = create_app()
setup_logging(app)
```

### 2. 로그 레벨 설정

```python
# 개발 환경
app.logger.setLevel(logging.DEBUG)

# 프로덕션 환경
app.logger.setLevel(logging.WARNING)
```

### 3. 사용 예제

```python
@app.route('/api/hospitals')
def get_hospitals():
    try:
        app.logger.info('Fetching hospitals from database')
        hospitals = repository.find_all()
        app.logger.info(f'Found {len(hospitals)} hospitals')
        return jsonify(hospitals)
    except Exception as e:
        app.logger.error(f'Error fetching hospitals: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500
```

---

## 🌍 환경별 설정

### 1. 개발 환경 (Development)

```python
# run.py
from app import create_app

app = create_app('development')

if __name__ == '__main__':
    app.run(
        host='127.0.0.1',  # 로컬만
        port=5001,
        debug=True,
        use_reloader=True  # 코드 변경 시 자동 재시작
    )
```

### 2. 테스트 환경 (Testing)

```python
# config/testing.py
class TestingConfig:
    TESTING = True
    DEBUG = False
    
    # 테스트용 데이터베이스
    DB_NAME = 'testdb_test'
    
    # 세션 설정
    WTF_CSRF_ENABLED = False
```

### 3. 프로덕션 환경 (Production)

#### Gunicorn 사용
```bash
pip install gunicorn
```

```bash
# gunicorn으로 실행
gunicorn \
    --bind 0.0.0.0:5001 \
    --workers 4 \
    --threads 2 \
    --timeout 60 \
    --access-logfile logs/access.log \
    --error-logfile logs/error.log \
    run:app
```

#### systemd 서비스 설정
```ini
# /etc/systemd/system/bohun1.service
[Unit]
Description=Bohun Hospital Management System
After=network.target mysql.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/opt/bohun1
Environment="PATH=/opt/bohun1/venv/bin"
Environment="FLASK_ENV=production"
ExecStart=/opt/bohun1/venv/bin/gunicorn \
    --bind 0.0.0.0:5001 \
    --workers 4 \
    run:app
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## 📊 모니터링 설정

### 1. 헬스체크 엔드포인트

```python
@app.route('/health')
def health_check():
    try:
        # 데이터베이스 연결 테스트
        with connection_pool.connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT 1')
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 503
```

### 2. 메트릭 수집

```bash
pip install prometheus-flask-exporter
```

```python
from prometheus_flask_exporter import PrometheusMetrics

app = create_app()
metrics = PrometheusMetrics(app)
```

---

## 🔧 문제 해결

### 연결 문제

```python
# 연결 타임아웃 설정
self.connection_config = {
    'host': 'localhost',
    'connect_timeout': 10,
    'read_timeout': 30,
    'write_timeout': 30
}
```

### 인코딩 문제

```python
# MySQL 연결 시 인코딩 명시
self.connection_config = {
    'charset': 'utf8mb4',
    'init_command': "SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci"
}
```

### 세션 문제

```python
# 세션 저장소 변경 (Redis 사용)
from flask_session import Session

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')
Session(app)
```

---

## 📚 참고 자료

- Flask 설정 문서: https://flask.palletsprojects.com/en/2.3.x/config/
- MySQL 연결 풀: https://pypi.org/project/DBUtils/
- Gunicorn 설정: https://docs.gunicorn.org/en/stable/settings.html

---

**✅ 체크리스트**

설정 완료 후 확인:
- [ ] 데이터베이스 연결 정상 작동
- [ ] SECRET_KEY 강력한 값으로 설정
- [ ] 프로덕션에서 DEBUG=False
- [ ] HTTPS 설정 (프로덕션)
- [ ] 로그 파일 생성 확인
- [ ] 성능 테스트 완료
- [ ] 백업 자동화 설정
- [ ] 모니터링 시스템 구축

**이 설정 가이드와 함께 시스템을 안전하고 효율적으로 운영하세요!** 🚀
