# 🏥 위탁병원 관리 시스템 설치 가이드

## 📋 목차
1. [시스템 요구사항](#시스템-요구사항)
2. [사전 준비사항](#사전-준비사항)
3. [설치 절차](#설치-절차)
4. [데이터베이스 설정](#데이터베이스-설정)
5. [애플리케이션 설정](#애플리케이션-설정)
6. [실행 및 테스트](#실행-및-테스트)
7. [문제 해결](#문제-해결)

---

## 🖥️ 시스템 요구사항

### 하드웨어 요구사항
- **CPU**: 2코어 이상
- **RAM**: 4GB 이상 (권장: 8GB)
- **HDD**: 10GB 이상의 여유 공간
- **네트워크**: 인터넷 연결 (패키지 설치용)

### 소프트웨어 요구사항
- **운영체제**: 
  - Windows 10/11 (64bit)
  - Windows Server 2016 이상
  - Linux (Ubuntu 20.04 LTS 이상)
  - macOS 10.15 이상

- **필수 소프트웨어**:
  - Python 3.8 이상 (권장: Python 3.12)
  - MySQL 8.0 이상
  - Git (선택사항)

---

## 📦 사전 준비사항

### 1. Python 설치

#### Windows
```powershell
# Python 공식 웹사이트에서 다운로드
# https://www.python.org/downloads/

# 설치 시 "Add Python to PATH" 체크 필수!

# 설치 확인
python --version
pip --version
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
python3 --version
pip3 --version
```

### 2. MySQL 설치

#### Windows
```powershell
# MySQL 공식 웹사이트에서 MySQL Installer 다운로드
# https://dev.mysql.com/downloads/installer/

# MySQL Installer 실행 후:
# 1. "Developer Default" 선택
# 2. root 비밀번호 설정 (예: Admin1)
# 3. MySQL Server 포트: 3306 (기본값)

# 설치 확인
mysql --version
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
sudo systemctl enable mysql

# MySQL 보안 설정
sudo mysql_secure_installation

# 설치 확인
mysql --version
```

---

## 🚀 설치 절차

### 1. 프로젝트 파일 다운로드

#### 방법 A: Git 사용 (권장)
```bash
# 프로젝트 클론
git clone <repository-url>
cd bohun1
```

#### 방법 B: ZIP 파일 다운로드
1. 프로젝트 ZIP 파일 다운로드
2. 원하는 위치에 압축 해제 (예: `C:\bohun1` 또는 `/opt/bohun1`)
3. 해당 디렉토리로 이동

### 2. 가상환경 생성 및 활성화

#### Windows (PowerShell)
```powershell
# 프로젝트 디렉토리로 이동
cd C:\bohun1

# 가상환경 생성
python -m venv venv

# 가상환경 활성화
.\venv\Scripts\Activate.ps1

# PowerShell 실행 정책 오류 시:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Windows (CMD)
```cmd
cd C:\bohun1
python -m venv venv
venv\Scripts\activate.bat
```

#### Linux/macOS
```bash
cd /opt/bohun1
python3 -m venv venv
source venv/bin/activate
```

### 3. Python 패키지 설치

```bash
# requirements.txt의 모든 패키지 설치
pip install -r requirements.txt

# 설치 확인
pip list
```

**주요 패키지 목록**:
- Flask 2.3.3 (웹 프레임워크)
- PyMySQL 1.1.0 (MySQL 연결)
- folium 0.14.0 (지도 생성)
- werkzeug (보안 및 암호화)

---

## 🗄️ 데이터베이스 설정

### 1. MySQL 접속 및 데이터베이스 생성

```bash
# MySQL 접속 (root 계정)
mysql -u root -p
# 비밀번호 입력: Admin1 (또는 설정한 비밀번호)
```

### 2. 데이터베이스 및 테이블 생성

```sql
-- 데이터베이스 생성
CREATE DATABASE IF NOT EXISTS testdb 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- 데이터베이스 선택
USE testdb;

-- 위탁병원현황 테이블 생성
CREATE TABLE IF NOT EXISTS `위탁병원현황` (
    `연번` INT AUTO_INCREMENT PRIMARY KEY COMMENT '고유 ID',
    `시군구` VARCHAR(8) NOT NULL COMMENT '시군구',
    `요양기관명` VARCHAR(32) NOT NULL COMMENT '병원명',
    `종별` VARCHAR(4) NOT NULL COMMENT '병원 종별 (종합병원, 병원, 의원, 요양병원)',
    `병상수` INT DEFAULT 0 COMMENT '병상 수',
    `진료과수` INT DEFAULT 0 COMMENT '진료과 수',
    `전화번호` VARCHAR(16) COMMENT '전화번호',
    `주소` VARCHAR(64) NOT NULL COMMENT '주소',
    `상세주소` VARCHAR(64) COMMENT '상세주소',
    `경도` DOUBLE COMMENT '경도 (longitude)',
    `위도` DOUBLE COMMENT '위도 (latitude)',
    INDEX idx_sigungu (`시군구`),
    INDEX idx_type (`종별`),
    INDEX idx_name (`요양기관명`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- users 테이블 생성 (로그인/회원가입용)
CREATE TABLE IF NOT EXISTS `users` (
    `user_id` INT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(50) NOT NULL UNIQUE,
    `email` VARCHAR(100) NOT NULL UNIQUE,
    `password_hash` VARCHAR(255) NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_username (`username`),
    INDEX idx_email (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 권한 확인
SHOW GRANTS FOR 'root'@'localhost';

-- MySQL 종료
EXIT;
```

### 3. 샘플 데이터 입력 (선택사항)

```bash
# 프로젝트 디렉토리에서 실행
python create_sample_data.py
```

**또는 직접 SQL로 입력**:
```sql
USE testdb;

INSERT INTO `위탁병원현황` 
(`시군구`, `요양기관명`, `종별`, `병상수`, `진료과수`, `전화번호`, `주소`, `상세주소`, `경도`, `위도`) 
VALUES
('서울', '서울대학교병원', '종합병원', 1779, 40, '02-2072-2114', '서울특별시 종로구 대학로 101', '', 127.002158, 37.579617),
('서울', '강남세브란스병원', '종합병원', 1000, 35, '02-2019-3000', '서울특별시 강남구 언주로 211', '', 127.053350, 37.517305),
('부산', '부산대학교병원', '종합병원', 900, 30, '051-240-7000', '부산광역시 서구 구덕로 179', '', 129.019208, 35.104270);
```

---

## ⚙️ 애플리케이션 설정

### 1. 환경설정 파일 생성

프로젝트 루트에 `.env` 파일 생성 (선택사항):

```bash
# .env 파일 내용
# Flask 설정
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-change-this-in-production

# MySQL 연결 정보
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=Admin1
DB_NAME=testdb

# 서버 설정
FLASK_HOST=0.0.0.0
FLASK_PORT=5001
```

### 2. 데이터베이스 연결 정보 확인

다음 파일들의 MySQL 연결 정보가 올바른지 확인:

#### `app/repositories/testdb_hospital_repository.py`
```python
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
self.connection_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Admin1',
    'database': 'testdb',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}
```

**⚠️ 중요**: 프로덕션 환경에서는 반드시 비밀번호를 변경하세요!

### 3. 방화벽 설정 (필요시)

#### Windows
```powershell
# Windows Defender 방화벽에서 포트 5001 허용
New-NetFirewallRule -DisplayName "Flask App" -Direction Inbound -LocalPort 5001 -Protocol TCP -Action Allow
```

#### Linux
```bash
# UFW 방화벽 설정
sudo ufw allow 5001/tcp
sudo ufw reload
```

---

## 🎯 실행 및 테스트

### 1. 애플리케이션 실행

```bash
# 가상환경이 활성화된 상태에서
python run.py
```

**실행 성공 시 출력**:
```
✅ users 테이블 확인/생성 완료
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5001
 * Running on http://192.168.x.x:5001
```

### 2. 웹 브라우저로 접속

- **로컬 접속**: http://127.0.0.1:5001
- **네트워크 접속**: http://[서버IP]:5001

### 3. 초기 로그인

1. 브라우저에서 자동으로 로그인 페이지로 이동
2. **회원가입** 탭 클릭
3. 계정 생성:
   - 사용자명: admin
   - 이메일: admin@example.com
   - 비밀번호: admin123 (최소 6자)
4. 로그인 후 메인 대시보드 접속

### 4. 기능 테스트

#### ✅ 메인 대시보드
- http://127.0.0.1:5001/
- 시스템 개요 및 통계 확인

#### ✅ 병원 관리 (CRUD)
- http://127.0.0.1:5001/hospital_crud
- 병원 추가, 수정, 삭제, 검색 테스트

#### ✅ Folium 지도
- http://127.0.0.1:5001/folium-map
- 병원 위치 지도 확인
- 종별 필터링 테스트

#### ✅ 로그아웃
- http://127.0.0.1:5001/logout

---

## 🔧 프로덕션 배포

### 1. Gunicorn 사용 (Linux/macOS)

```bash
# Gunicorn 설치
pip install gunicorn

# Gunicorn으로 실행
gunicorn -w 4 -b 0.0.0.0:5001 run:app
```

### 2. Nginx 리버스 프록시 설정 (선택사항)

```nginx
# /etc/nginx/sites-available/bohun1
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias /opt/bohun1/public;
    }
}
```

```bash
# Nginx 설정 활성화
sudo ln -s /etc/nginx/sites-available/bohun1 /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 3. systemd 서비스 등록 (Linux)

```bash
# /etc/systemd/system/bohun1.service
[Unit]
Description=Bohun Hospital Management System
After=network.target mysql.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/bohun1
Environment="PATH=/opt/bohun1/venv/bin"
ExecStart=/opt/bohun1/venv/bin/gunicorn -w 4 -b 127.0.0.1:5001 run:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# 서비스 등록 및 실행
sudo systemctl daemon-reload
sudo systemctl start bohun1
sudo systemctl enable bohun1
sudo systemctl status bohun1
```

---

## 🛠️ 문제 해결

### 1. Python 관련 문제

#### ❌ "python: command not found"
```bash
# Windows: PATH 환경변수에 Python 추가
# 제어판 > 시스템 > 고급 시스템 설정 > 환경 변수

# Linux: python3로 실행
python3 run.py
```

#### ❌ "No module named 'flask'"
```bash
# 가상환경이 활성화되어 있는지 확인
# 패키지 재설치
pip install -r requirements.txt
```

### 2. MySQL 연결 문제

#### ❌ "Access denied for user 'root'@'localhost'"
```sql
-- MySQL에서 비밀번호 재설정
ALTER USER 'root'@'localhost' IDENTIFIED BY 'Admin1';
FLUSH PRIVILEGES;
```

#### ❌ "Can't connect to MySQL server"
```bash
# MySQL 서비스 상태 확인 (Windows)
Get-Service MySQL*

# MySQL 서비스 시작
Start-Service MySQL80

# Linux
sudo systemctl status mysql
sudo systemctl start mysql
```

#### ❌ "Unknown database 'testdb'"
```sql
-- MySQL에 접속하여 데이터베이스 생성
CREATE DATABASE testdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. 포트 충돌 문제

#### ❌ "Address already in use"
```powershell
# Windows: 포트 5001 사용 중인 프로세스 확인
netstat -ano | findstr :5001
# PID 확인 후 종료
taskkill /PID [PID번호] /F

# Linux
lsof -i :5001
kill -9 [PID]
```

**또는 `run.py`에서 포트 변경**:
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)  # 5001 → 5002
```

### 4. 인코딩 문제

#### ❌ 한글이 깨져서 표시됨
```sql
-- MySQL 테이블 인코딩 확인
SHOW CREATE TABLE 위탁병원현황;

-- 인코딩 변경
ALTER TABLE 위탁병원현황 CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. 권한 문제 (Linux)

```bash
# 디렉토리 소유권 변경
sudo chown -R $USER:$USER /opt/bohun1

# 실행 권한 부여
chmod +x run.py
```

---

## 📞 지원 및 문의

### 로그 확인
- 애플리케이션 로그: 터미널 출력 확인
- MySQL 로그 (Linux): `/var/log/mysql/error.log`
- MySQL 로그 (Windows): `C:\ProgramData\MySQL\MySQL Server 8.0\Data\*.err`

### 시스템 정보 확인
```bash
# Python 버전
python --version

# 설치된 패키지
pip list

# MySQL 버전
mysql --version

# 데이터베이스 연결 테스트
mysql -u root -p testdb -e "SELECT COUNT(*) FROM 위탁병원현황;"
```

---

## 📝 체크리스트

설치 완료 후 아래 항목들을 확인하세요:

- [ ] Python 3.8 이상 설치 완료
- [ ] MySQL 8.0 이상 설치 및 실행 중
- [ ] 가상환경 생성 및 활성화
- [ ] requirements.txt 패키지 설치 완료
- [ ] testdb 데이터베이스 생성
- [ ] 위탁병원현황 테이블 생성
- [ ] users 테이블 생성
- [ ] MySQL 연결 정보 설정 확인
- [ ] 애플리케이션 실행 성공 (http://127.0.0.1:5001)
- [ ] 회원가입/로그인 테스트 완료
- [ ] 병원 CRUD 기능 테스트 완료
- [ ] Folium 지도 기능 테스트 완료

**축하합니다! 🎉 위탁병원 관리 시스템 설치가 완료되었습니다.**

---

## 📚 추가 자료

- Python 공식 문서: https://docs.python.org/ko/3/
- Flask 공식 문서: https://flask.palletsprojects.com/
- MySQL 공식 문서: https://dev.mysql.com/doc/
- Folium 공식 문서: https://python-visualization.github.io/folium/

