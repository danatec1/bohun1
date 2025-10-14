# 🚀 보훈 병원 시스템 배포 가이드

**버전**: 1.0 | **작성일**: 2025-10-10

---

## 📋 목차

1. [로컬 네트워크 배포](#1-로컬-네트워크-배포)
2. [Windows Server 배포](#2-windows-server-배포)
3. [클라우드 배포](#3-클라우드-배포)
4. [Docker 배포](#4-docker-배포)
5. [보안 설정](#5-보안-설정)

---

## 1️⃣ 로컬 네트워크 배포 (가장 간단)

### 현재 상태
✅ 이미 `host='0.0.0.0'`으로 설정되어 있어 로컬 네트워크에서 접근 가능

### 배포 절차

#### 1. 방화벽 포트 열기
```powershell
# PowerShell을 관리자 권한으로 실행
New-NetFirewallRule -DisplayName "Flask App Port 5001" -Direction Inbound -LocalPort 5001 -Protocol TCP -Action Allow
```

#### 2. 서버 실행
```powershell
cd c:\bohun1
python run.py
```

#### 3. IP 주소 확인
```powershell
ipconfig
```
출력에서 **IPv4 주소** 확인 (예: `192.168.1.100`)

#### 4. 접속
- **같은 컴퓨터**: http://127.0.0.1:5001
- **같은 네트워크**: http://192.168.1.100:5001 (실제 IP로 변경)

### 주의사항
- ⚠️ 디버그 모드 활성화 상태
- ⚠️ 공용 인터넷 접근 불가
- ⚠️ 컴퓨터 종료 시 서버 중지

---

## 2️⃣ Windows Server 배포 (권장)

### A. Waitress WSGI 서버 사용 (권장)

#### 1. Waitress 설치
```powershell
pip install waitress
```

#### 2. 운영 서버 스크립트 생성

파일: `run_production.py`
```python
from waitress import serve
from app import create_app
import os

# 운영 환경 설정
os.environ['FLASK_ENV'] = 'production'
app = create_app('production')

if __name__ == '__main__':
    print('🚀 보훈 병원 시스템 시작 중...')
    print('📍 서버 주소: http://0.0.0.0:5001')
    print('⚠️  종료하려면 Ctrl+C를 누르세요')
    
    serve(app, host='0.0.0.0', port=5001, threads=4)
```

#### 3. 실행
```powershell
python run_production.py
```

### B. Windows 서비스로 등록 (자동 시작)

#### 1. NSSM 설치
```powershell
# Chocolatey가 설치되어 있다면
choco install nssm

# 또는 https://nssm.cc/download 에서 다운로드
```

#### 2. 서비스 등록
```powershell
# NSSM을 관리자 권한으로 실행
nssm install BohunHospitalSystem "C:\Python312\python.exe" "c:\bohun1\run_production.py"

# 서비스 시작
nssm start BohunHospitalSystem

# 서비스 상태 확인
nssm status BohunHospitalSystem
```

#### 3. 서비스 관리
```powershell
# 중지
nssm stop BohunHospitalSystem

# 재시작
nssm restart BohunHospitalSystem

# 제거
nssm remove BohunHospitalSystem confirm
```

---

## 3️⃣ 클라우드 배포

### A. Azure App Service

#### 1. Azure CLI 설치 및 로그인
```powershell
# Azure CLI 설치
winget install Microsoft.AzureCLI

# 로그인
az login
```

#### 2. 웹앱 생성
```powershell
# 리소스 그룹 생성
az group create --name bohun-hospital-rg --location koreacentral

# App Service Plan 생성
az appservice plan create --name bohun-plan --resource-group bohun-hospital-rg --sku B1 --is-linux

# 웹앱 생성
az webapp create --resource-group bohun-hospital-rg --plan bohun-plan --name bohun-hospital-app --runtime "PYTHON|3.12"
```

#### 3. 배포
```powershell
# Git 배포
az webapp deployment source config-local-git --name bohun-hospital-app --resource-group bohun-hospital-rg

# 또는 ZIP 배포
az webapp deployment source config-zip --resource-group bohun-hospital-rg --name bohun-hospital-app --src app.zip
```

### B. AWS EC2

#### 1. EC2 인스턴스 생성
- Windows Server 2022 선택
- t3.medium 이상 권장

#### 2. 인스턴스 설정
```powershell
# Python 설치
# MySQL 설치
# 코드 복사

cd C:\bohun1
pip install -r requirements.txt
python run_production.py
```

### C. Heroku (간편)

#### 1. Heroku CLI 설치
```powershell
# https://devcenter.heroku.com/articles/heroku-cli
```

#### 2. 배포 파일 생성

**Procfile** (파일명 정확히)
```
web: waitress-serve --port=$PORT wsgi:app
```

**runtime.txt**
```
python-3.12.0
```

#### 3. 배포
```powershell
heroku login
heroku create bohun-hospital
git push heroku main
```

---

## 4️⃣ Docker 배포

### Dockerfile 생성

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# 시스템 패키지 업데이트
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Python 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install waitress

# 애플리케이션 코드 복사
COPY . .

# 포트 노출
EXPOSE 5001

# 환경 변수 설정
ENV FLASK_ENV=production

# 서버 실행
CMD ["waitress-serve", "--host=0.0.0.0", "--port=5001", "wsgi:app"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5001:5001"
    environment:
      - FLASK_ENV=production
      - MYSQL_HOST=mysql
      - MYSQL_USER=root
      - MYSQL_PASSWORD=Admin1
      - MYSQL_DATABASE=testdb
    depends_on:
      - mysql
    
  mysql:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=Admin1
      - MYSQL_DATABASE=testdb
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

### 실행
```powershell
# Docker Desktop 설치 필요
docker-compose up -d
```

---

## 5️⃣ 보안 설정

### A. 환경 변수 설정

#### Windows
```powershell
# 영구 환경 변수 설정
[Environment]::SetEnvironmentVariable("SECRET_KEY", "your-secret-key-here", "Machine")
[Environment]::SetEnvironmentVariable("MYSQL_PASSWORD", "your-password", "Machine")
[Environment]::SetEnvironmentVariable("FLASK_ENV", "production", "Machine")
```

#### .env 파일 사용
```ini
# .env 파일 생성
SECRET_KEY=your-random-secret-key-here
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=Admin1
MYSQL_DATABASE=testdb
FLASK_ENV=production
```

```powershell
# python-dotenv 설치
pip install python-dotenv
```

### B. HTTPS 설정

#### 1. Let's Encrypt 인증서 (무료)
```powershell
# Certbot 설치
choco install certbot
```

#### 2. Nginx 리버스 프록시
```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### C. 데이터베이스 보안

```python
# testdb_hospital_repository.py에서 환경 변수 사용
import os

class TestDBHospitalRepository:
    def __init__(self):
        self.connection_config = {
            'host': os.environ.get('MYSQL_HOST', 'localhost'),
            'user': os.environ.get('MYSQL_USER', 'root'),
            'password': os.environ.get('MYSQL_PASSWORD'),  # 기본값 제거
            'database': os.environ.get('MYSQL_DATABASE', 'testdb'),
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor
        }
```

---

## 📊 배포 방법 비교

| 방법 | 난이도 | 비용 | 확장성 | 추천 대상 |
|------|--------|------|--------|-----------|
| **로컬 네트워크** | ⭐ | 무료 | ❌ | 개발/테스트 |
| **Waitress + NSSM** | ⭐⭐ | 무료 | ⭐ | 소규모 내부 서비스 |
| **Azure App Service** | ⭐⭐⭐ | 유료 | ⭐⭐⭐ | 엔터프라이즈 |
| **AWS EC2** | ⭐⭐⭐ | 유료 | ⭐⭐⭐ | 유연한 제어 필요 |
| **Heroku** | ⭐⭐ | 무료/유료 | ⭐⭐ | 빠른 프로토타입 |
| **Docker** | ⭐⭐⭐⭐ | 무료 | ⭐⭐⭐⭐ | 컨테이너 환경 |

---

## ✅ 배포 전 체크리스트

### 코드
- [ ] `DEBUG = False` 설정
- [ ] `SECRET_KEY` 환경 변수 설정
- [ ] 데이터베이스 비밀번호 환경 변수화
- [ ] 에러 로깅 설정
- [ ] HTTPS 설정 (운영 환경)

### 인프라
- [ ] 방화벽 포트 오픈
- [ ] MySQL 서버 실행
- [ ] 백업 설정
- [ ] 모니터링 설정

### 테스트
- [ ] 모든 페이지 접속 확인
- [ ] 지도 생성 테스트
- [ ] Excel 내보내기 테스트
- [ ] 다른 컴퓨터에서 접속 테스트

---

## 🆘 문제 해결

### 포트가 이미 사용 중
```powershell
# 포트 사용 프로세스 확인
netstat -ano | findstr :5001

# 프로세스 종료
taskkill /PID [프로세스ID] /F
```

### MySQL 연결 실패
```powershell
# MySQL 서비스 확인
Get-Service -Name "MySQL*"

# MySQL 재시작
Restart-Service -Name "MySQL80"
```

### 방화벽 문제
```powershell
# 방화벽 규칙 확인
Get-NetFirewallRule -DisplayName "Flask*"

# 규칙 제거 후 재생성
Remove-NetFirewallRule -DisplayName "Flask App Port 5001"
New-NetFirewallRule -DisplayName "Flask App Port 5001" -Direction Inbound -LocalPort 5001 -Protocol TCP -Action Allow
```

---

## 📞 추가 지원

- **로컬 네트워크**: 지금 바로 사용 가능 ✅
- **Windows 서버**: Waitress + NSSM 권장
- **클라우드**: Azure App Service 권장 (한국 리전 지원)
- **간단 배포**: Heroku 권장

상세 문서: `OPERATION_MANUAL.md` 참조
