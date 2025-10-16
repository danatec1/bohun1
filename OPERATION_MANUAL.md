# 🏥 위탁병원 관리 시스템 운영 매뉴얼

## 📋 목차
1. [웹 서비스 시작 순서](#웹-서비스-시작-순서)
2. [시스템 개요](#시스템-개요)
3. [일상 운영](#일상-운영)
4. [사용자 관리](#사용자-관리)
5. [병원 데이터 관리](#병원-데이터-관리)
6. [지도 기능 활용](#지도-기능-활용)
7. [백업 및 복구](#백업-및-복구)
8. [문제 해결](#문제-해결)

---

## 🚀 웹 서비스 시작 순서

### 📝 시작 전 체크리스트
- [ ] Python 3.8 이상 설치 확인
- [ ] MySQL 8.0 설치 및 실행 중
- [ ] 데이터베이스 `testdb` 생성 완료
- [ ] 필요한 테이블 생성 완료
- [ ] 가상환경 준비 완료

---

### 🔢 단계별 시작 순서

#### **STEP 1: 프로젝트 디렉토리로 이동**
```powershell
# Windows PowerShell
cd C:\bohun1

# 또는 Linux/Mac
cd /opt/bohun1
```

---

#### **STEP 2: MySQL 서비스 확인 및 시작**

##### Windows
```powershell
# MySQL 서비스 상태 확인
Get-Service MySQL*

# 출력 예시:
# Status   Name               DisplayName
# ------   ----               -----------
# Running  MySQL80            MySQL80

# MySQL이 중지되어 있다면 시작
Start-Service MySQL80

# 다시 확인
Get-Service MySQL80
```

##### Linux/Mac
```bash
# MySQL 상태 확인
sudo systemctl status mysql

# MySQL 시작 (중지되어 있다면)
sudo systemctl start mysql

# MySQL 자동 시작 설정
sudo systemctl enable mysql
```

---

#### **STEP 3: 가상환경 활성화**

##### Windows PowerShell
```powershell
# 가상환경 활성화
.\venv\Scripts\Activate.ps1

# 활성화 성공 시 프롬프트에 (venv) 표시됨
# (venv) PS C:\bohun1>

# ⚠️ 실행 정책 오류 발생 시:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# 그 후 다시 활성화 시도
```

##### Windows CMD
```cmd
venv\Scripts\activate.bat
```

##### Linux/Mac
```bash
source venv/bin/activate
```

**✅ 활성화 확인**:
```bash
# Python 경로 확인 (가상환경 경로여야 함)
which python  # Linux/Mac
where python  # Windows

# 패키지 확인
pip list
```

---

#### **STEP 4: 데이터베이스 연결 확인**

```bash
# MySQL 접속 테스트
mysql -u root -pAdmin1 testdb -e "SELECT COUNT(*) FROM 위탁병원현황;"

# 성공 시 출력:
# +----------+
# | COUNT(*) |
# +----------+
# |       XX |
# +----------+
```

**연결 실패 시**:
```bash
# MySQL 비밀번호 확인
mysql -u root -p
# 비밀번호 입력 후 접속 확인

# testdb 데이터베이스 존재 확인
SHOW DATABASES;
```

---

#### **STEP 5: Flask 애플리케이션 실행**

```bash
# 애플리케이션 실행
python run.py
```

**✅ 정상 실행 시 출력**:
```
✅ users 테이블 확인/생성 완료
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5001
 * Running on http://192.168.x.x:5001
Press CTRL+C to quit
 * Restarting with stat
✅ users 테이블 확인/생성 완료
 * Debugger is active!
 * Debugger PIN: xxx-xxx-xxx
```

**주요 확인 사항**:
- ✅ "users 테이블 확인/생성 완료" 메시지
- ✅ "Running on http://127.0.0.1:5001" 메시지
- ✅ 디버거 활성화 메시지

---

#### **STEP 6: 웹 브라우저로 접속**

##### 로컬 컴퓨터에서 접속:
```
http://127.0.0.1:5001
또는
http://localhost:5001
```

##### 같은 네트워크의 다른 컴퓨터에서 접속:
```
http://[서버컴퓨터IP]:5001
예: http://192.168.1.100:5001
```

**서버 IP 확인 방법**:
```powershell
# Windows
ipconfig

# Linux/Mac
ifconfig
ip addr show
```

---

#### **STEP 7: 로그인 페이지 확인**

1. 브라우저에서 자동으로 **로그인 페이지**로 이동
2. 처음 사용이라면 **"회원가입"** 탭 클릭
3. 계정 생성:
   - **사용자명**: admin (또는 원하는 이름)
   - **이메일**: admin@example.com
   - **비밀번호**: admin123 (최소 6자)
   - **비밀번호 확인**: admin123
4. **"가입하기"** 버튼 클릭
5. 자동으로 로그인 탭으로 이동
6. 방금 만든 계정으로 로그인

---

#### **STEP 8: 메인 대시보드 확인**

로그인 성공 시:
1. **메인 대시보드**로 이동
2. 4개의 주요 기능 카드 표시:
   - 🏥 위탁병원 관리
   - 🗺️ 위탁병원 지도
   - 🔍 위탁병원 검색
   - 📋 위탁병원 현황

---

#### **STEP 9: 기능 테스트**

##### 병원 관리 (CRUD)
```
http://127.0.0.1:5001/hospital_crud
```
- ✅ 병원 목록 조회
- ✅ 검색 기능 (병원명, 주소, 전화번호)
- ✅ 종별 필터 (종합병원, 병원, 의원, 요양병원)
- ✅ 새 병원 추가
- ✅ 병원 정보 수정
- ✅ 병원 삭제

##### Folium 지도
```
http://127.0.0.1:5001/folium-map
```
- ✅ 지도 생성 버튼 클릭
- ✅ 병원 마커 표시 확인
- ✅ 종별 필터링 (우측 상단 체크박스)
- ✅ 마커 클릭 시 팝업 정보 확인
- ✅ 배경 지도 변경 (OpenStreetMap, VWorld 등)

---

### 🛑 서비스 종료 순서

#### **STEP 1: Flask 서버 종료**
```bash
# 터미널에서 Ctrl + C 키 입력
# 출력: KeyboardInterrupt
```

#### **STEP 2: 가상환경 비활성화**
```bash
deactivate

# 프롬프트에서 (venv) 표시 사라짐
```

#### **STEP 3: MySQL 종료 (선택사항)**
```powershell
# Windows - 서버 종료 시에만
Stop-Service MySQL80

# Linux/Mac - 서버 종료 시에만
sudo systemctl stop mysql
```

---

### 🔄 서비스 재시작

```bash
# 1. 가상환경 활성화
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Linux/Mac

# 2. 애플리케이션 실행
python run.py
```

---

### ⚡ 빠른 시작 (한 번에)

#### Windows PowerShell 스크립트
```powershell
# start_server.ps1 파일 생성
cd C:\bohun1
Start-Service MySQL80
.\venv\Scripts\Activate.ps1
python run.py
```

실행:
```powershell
.\start_server.ps1
```

#### Linux/Mac Bash 스크립트
```bash
# start_server.sh 파일 생성
#!/bin/bash
cd /opt/bohun1
sudo systemctl start mysql
source venv/bin/activate
python run.py
```

실행:
```bash
chmod +x start_server.sh
./start_server.sh
```

---

### 🔍 문제 발생 시 체크리스트

#### ❌ "ModuleNotFoundError: No module named 'flask'"
```bash
# 가상환경이 활성화되었는지 확인
# 프롬프트에 (venv) 표시 확인

# 패키지 재설치
pip install -r requirements.txt
```

#### ❌ "Can't connect to MySQL server"
```bash
# MySQL 서비스 실행 확인
Get-Service MySQL*  # Windows
sudo systemctl status mysql  # Linux

# MySQL 시작
Start-Service MySQL80  # Windows
sudo systemctl start mysql  # Linux
```

#### ❌ "Port 5001 already in use"
```powershell
# Windows: 포트 사용 중인 프로세스 확인
netstat -ano | findstr :5001

# PID 확인 후 종료
taskkill /PID [PID번호] /F

# Linux/Mac
lsof -i :5001
kill -9 [PID]
```

#### ❌ "Access denied for user 'root'@'localhost'"
```bash
# 비밀번호 확인
# 기본값: Admin1

# 비밀번호가 다르다면 코드 수정:
# app/repositories/testdb_hospital_repository.py
# app/repositories/hospital_crud_repository.py
# app/repositories/user_repository.py
```

---

## 📖 시스템 개요

### 시스템 구성
```
위탁병원 관리 시스템
├── 프론트엔드: HTML5, CSS3, JavaScript
├── 백엔드: Flask (Python)
├── 데이터베이스: MySQL 8.0
└── 지도 라이브러리: Folium
```

### 주요 기능
1. **인증 시스템**: 로그인/회원가입/로그아웃
2. **병원 CRUD**: 생성, 조회, 수정, 삭제
3. **검색/필터**: 병원명, 주소, 전화번호, 종별
4. **지도 시각화**: Folium 기반 인터랙티브 지도
5. **종별 필터링**: 종합병원, 병원, 의원, 요양병원

### 시스템 URL
- **메인 페이지**: http://127.0.0.1:5001/
- **로그인**: http://127.0.0.1:5001/login
- **병원 관리**: http://127.0.0.1:5001/hospital_crud
- **지도 보기**: http://127.0.0.1:5001/folium-map
- **로그아웃**: http://127.0.0.1:5001/logout

---

## 👥 사용자 관리

### 1. 신규 사용자 등록

**웹 인터페이스 이용**:
1. http://127.0.0.1:5001/login 접속
2. "회원가입" 탭 클릭
3. 정보 입력:
   - 사용자명 (영문, 숫자 조합)
   - 이메일
   - 비밀번호 (최소 6자)
   - 비밀번호 확인
4. "가입하기" 버튼 클릭

**MySQL에서 직접 생성** (관리자용):
```sql
USE testdb;

-- 비밀번호 해시 생성 (Python에서)
-- python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('password123'))"

INSERT INTO users (username, email, password_hash)
VALUES (
    'newuser',
    'newuser@example.com',
    'pbkdf2:sha256:260000$...'  -- 위에서 생성한 해시값
);
```

### 2. 사용자 목록 조회

```sql
USE testdb;

SELECT user_id, username, email, created_at
FROM users
ORDER BY created_at DESC;
```

### 3. 비밀번호 재설정

```python
# Python 인터프리터에서 실행
from werkzeug.security import generate_password_hash

# 새 비밀번호 해시 생성
new_hash = generate_password_hash('newpassword123')
print(new_hash)
```

```sql
-- MySQL에서 업데이트
UPDATE users 
SET password_hash = 'pbkdf2:sha256:260000$...'  -- 위에서 생성한 해시
WHERE username = 'targetuser';
```

---

## 🏥 병원 데이터 관리

### 1. 병원 추가 (웹 인터페이스)

1. http://127.0.0.1:5001/hospital_crud 접속
2. **"+ 새 병원 추가"** 버튼 클릭
3. 필수 정보 입력:
   - 시군구
   - 요양기관명
   - 종별 (종합병원/병원/의원/요양병원)
   - 병상수
   - 진료과수
   - 전화번호
   - 주소
   - 경도/위도
4. **"저장"** 클릭

### 2. 병원 검색

**웹 인터페이스**:
- 검색창에 입력: 병원명, 주소, 전화번호 중 일부
- 종별 드롭다운으로 필터링

**예시**:
- "서울" 입력 → 서울 지역 병원 검색
- "02-2072" 입력 → 전화번호로 검색
- "종합병원" 선택 → 종합병원만 표시

---

## 🗺️ 지도 기능 활용

### 1. 지도 생성

1. http://127.0.0.1:5001/folium-map 접속
2. **"지도 생성"** 버튼 클릭
3. 생성된 지도 자동 표시

### 2. 지도 기능

#### 종별 필터링
- 우측 상단 체크박스로 ON/OFF
- 🔴 종합병원 (빨강)
- 🔵 병원 (파랑)
- 🟢 의원 (초록)
- 🟠 요양병원 (주황)

#### 배경 지도 변경
- 우측 상단 레이어 컨트롤
- OpenStreetMap (기본, 영문)
- VWorld 기본지도 (한글)
- VWorld 위성지도
- VWorld 하이브리드
- CartoDB Positron (밝은 테마)
- CartoDB Dark (어두운 테마)

#### 마커 정보
- 마커 클릭 시 팝업 표시:
  - 🏥 병원명
  - 📍 주소
  - 🏥 규모 (병상수, 진료과수)
  - 🌍 좌표 (위도, 경도)

---

## 💾 백업 및 복구

### 데이터베이스 백업

```bash
# Windows
mysqldump -u root -pAdmin1 testdb > C:\backup\testdb_backup_20250115.sql

# Linux/Mac
mysqldump -u root -pAdmin1 testdb > /backup/testdb_backup_20250115.sql
```

### 데이터베이스 복구

```bash
# MySQL 접속
mysql -u root -pAdmin1

# 기존 데이터베이스 삭제 (주의!)
DROP DATABASE IF EXISTS testdb;

# 데이터베이스 재생성
CREATE DATABASE testdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 종료
EXIT;

# 백업 파일에서 복구
mysql -u root -pAdmin1 testdb < C:\backup\testdb_backup_20250115.sql
```

---

## ❓ 문제 해결

### Q: 서버가 시작되지 않아요
**A**: 
1. 가상환경 활성화 확인
2. MySQL 서비스 실행 확인
3. 포트 5001 사용 중인지 확인

### Q: 로그인이 안 돼요
**A**:
1. 비밀번호 확인 (최소 6자)
2. 계정 존재 확인
3. 브라우저 쿠키 허용 설정

### Q: 지도가 생성되지 않아요
**A**:
1. 병원 데이터에 위도/경도 확인
2. Folium 패키지 설치 확인
3. 브라우저 F12로 오류 확인

---

## 📝 일일 운영 체크리스트

**시작 시**:
- [ ] MySQL 서비스 실행
- [ ] 가상환경 활성화
- [ ] Flask 서버 실행
- [ ] 웹 브라우저 접속 확인

**종료 시**:
- [ ] Flask 서버 종료 (Ctrl+C)
- [ ] 가상환경 비활성화
- [ ] 데이터 백업 (필요시)

---

**📌 이 매뉴얼을 인쇄하여 운영자 책상에 비치하세요!**
