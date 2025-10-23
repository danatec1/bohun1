# 🚀 Windows Server 배포 체크리스트

## 📦 배포에 필요한 파일 및 폴더

### 1️⃣ **필수 Python 파일**
```
✅ run.py                          # Flask 서버 실행 파일
✅ requirements.txt                 # Python 패키지 의존성
✅ hospital.db                      # SQLite 데이터베이스 (있는 경우)
```

### 2️⃣ **Flask 애플리케이션 폴더**
```
✅ app/
   ├── __init__.py                 # Flask 앱 초기화
   ├── controllers/                # 컨트롤러
   │   ├── __init__.py
   │   ├── main_controller.py
   │   ├── hospital_controller.py
   │   └── auth_controller.py
   ├── models/                     # 데이터 모델
   │   ├── __init__.py
   │   ├── hospital.py
   │   └── user.py
   ├── repositories/               # 데이터 저장소
   │   ├── __init__.py
   │   ├── hospital_repository.py
   │   └── mysql_hospital_repository.py
   ├── routes/                     # 라우트 (⭐ 차트 라우트 포함)
   │   └── __init__.py
   ├── services/                   # 비즈니스 로직
   │   ├── __init__.py
   │   └── hospital_service.py
   ├── templates/                  # HTML 템플릿
   │   ├── base.html
   │   ├── index.html
   │   ├── hospitals.html
   │   └── c.html                  # ⭐ 차트 대시보드 페이지
   └── utils/
```

### 3️⃣ **정적 파일 (Static Files)**
```
✅ public/
   ├── css/
   │   └── style.css
   ├── js/
   │   ├── main.js
   │   └── hospitals.js
   └── images/
       └── logo.png

✅ public/chart*.html               # ⭐⭐⭐ 차트 HTML 파일들 (가장 중요!)
   ├── chart3_scatter_matrix.html
   ├── chart4_yearly_area.html
   ├── chart5_regional_bar.html
   ├── chart6_pivot_bar.html
   └── chart7_pie_subplots.html
```

### 4️⃣ **설정 파일**
```
✅ config/
   ├── __init__.py
   └── [기타 설정 파일]
```

---

## 🎯 차트 관련 필수 파일 (핵심!)

### ⭐ **반드시 가져가야 할 파일**
```
1. app/templates/c.html              # 차트 대시보드 페이지
2. app/routes/__init__.py            # 차트 라우트 포함 (/c, /chart3-7)
3. public/chart3_scatter_matrix.html # 산점도 행렬 차트
4. public/chart4_yearly_area.html    # 연도별 Area 차트
5. public/chart5_regional_bar.html   # 지역별 막대 차트
6. public/chart6_pivot_bar.html      # Pivot 막대 차트
7. public/chart7_pie_subplots.html   # 파이차트 서브플롯
```

---

## 📋 배포 단계별 가이드

### Step 1: 파일 복사
```powershell
# Windows Server에서 실행
# 전체 프로젝트 폴더를 복사 (예: C:\webapp\bohun1)

# 또는 필수 파일만 복사
xcopy /E /I "C:\bohun1\app" "C:\webapp\bohun1\app"
xcopy /E /I "C:\bohun1\public" "C:\webapp\bohun1\public"
xcopy /E /I "C:\bohun1\config" "C:\webapp\bohun1\config"
copy "C:\bohun1\run.py" "C:\webapp\bohun1\"
copy "C:\bohun1\requirements.txt" "C:\webapp\bohun1\"
```

### Step 2: Python 환경 설정
```powershell
# Python 3.8 이상 설치 확인
python --version

# 가상환경 생성 (선택사항)
python -m venv venv
.\venv\Scripts\Activate

# 패키지 설치
pip install -r requirements.txt
```

### Step 3: MySQL 연결 설정
```python
# config/ 또는 app/__init__.py에서 MySQL 연결 정보 수정
MYSQL_HOST = "your_server_ip"
MYSQL_USER = "root"
MYSQL_PASSWORD = "your_password"
MYSQL_DB = "testdb"
```

### Step 4: 방화벽 설정
```powershell
# 포트 5000 열기 (또는 80/443 사용)
New-NetFirewallRule -DisplayName "Flask App" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow
```

### Step 5: 서버 실행
```powershell
# 개발 서버 (테스트용)
python run.py

# 프로덕션 서버 (Waitress 사용 권장)
pip install waitress
waitress-serve --host=0.0.0.0 --port=5000 app:app
```

---

## 🔧 프로덕션 배포 옵션

### Option 1: Waitress (권장)
```python
# run_production.py
from waitress import serve
from app import create_app

app = create_app()
serve(app, host='0.0.0.0', port=5000, threads=4)
```

### Option 2: IIS (Internet Information Services)
1. **wfastcgi** 설치
   ```powershell
   pip install wfastcgi
   wfastcgi-enable
   ```

2. **IIS에 Python 핸들러 추가**
   - IIS Manager 열기
   - Handler Mappings → Add Module Mapping
   - FastCGI 설정

3. **web.config 생성**
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <configuration>
     <system.webServer>
       <handlers>
         <add name="Python FastCGI" 
              path="*" 
              verb="*" 
              modules="FastCgiModule" 
              scriptProcessor="C:\Python\python.exe|C:\Python\Scripts\wfastcgi.py" 
              resourceType="Unspecified" />
       </handlers>
     </system.webServer>
   </configuration>
   ```

### Option 3: Windows 서비스로 등록 (자동 시작)
```powershell
# NSSM (Non-Sucking Service Manager) 사용
# https://nssm.cc/ 에서 다운로드

nssm install FlaskChartApp "C:\Python\python.exe" "C:\webapp\bohun1\run.py"
nssm start FlaskChartApp
```

---

## ⚠️ 주의사항

### 1. **포트 변경**
```python
# run.py에서 포트 80 사용 시 관리자 권한 필요
# 또는 5000번 포트 사용 + IIS/Nginx 리버스 프록시 설정
```

### 2. **보안**
```python
# 프로덕션에서는 DEBUG 모드 끄기
app.config['DEBUG'] = False

# SECRET_KEY 설정
app.config['SECRET_KEY'] = 'your-secret-key-here'
```

### 3. **데이터베이스**
```python
# MySQL 연결 풀 설정
# SQLite 대신 MySQL 사용 권장 (동시 접속 처리)
```

---

## 📂 최소 배포 구조 (차트만 필요한 경우)

```
C:\webapp\bohun1\
├── run.py
├── requirements.txt
├── app\
│   ├── __init__.py
│   ├── routes\
│   │   └── __init__.py        # /c, /chart3-7 라우트
│   └── templates\
│       └── c.html              # 차트 대시보드
└── public\
    ├── chart3_scatter_matrix.html
    ├── chart4_yearly_area.html
    ├── chart5_regional_bar.html
    ├── chart6_pivot_bar.html
    └── chart7_pie_subplots.html
```

---

## ✅ 배포 후 확인 사항

1. ✅ 서버 실행: `python run.py`
2. ✅ 차트 페이지 접속: `http://server-ip:5000/c`
3. ✅ 개별 차트 접속:
   - `http://server-ip:5000/chart3`
   - `http://server-ip:5000/chart4`
   - `http://server-ip:5000/chart5`
   - `http://server-ip:5000/chart6`
   - `http://server-ip:5000/chart7`
4. ✅ 차트 인터랙션 테스트 (확대/축소/호버)

---

## 🎯 빠른 배포 명령어 요약

```powershell
# 1. 필수 파일 복사
robocopy "C:\bohun1\app" "C:\webapp\bohun1\app" /E
robocopy "C:\bohun1\public" "C:\webapp\bohun1\public" /E
copy "C:\bohun1\run.py" "C:\webapp\bohun1\"
copy "C:\bohun1\requirements.txt" "C:\webapp\bohun1\"

# 2. 패키지 설치
cd C:\webapp\bohun1
pip install -r requirements.txt

# 3. 서버 실행
python run.py
```

---

## 📞 트러블슈팅

### 차트가 404 에러
- `public/chart*.html` 파일이 제대로 복사되었는지 확인
- `app/routes/__init__.py`에 `/chart3-7` 라우트가 있는지 확인

### 데이터베이스 연결 오류
- MySQL 서버가 실행 중인지 확인
- 방화벽에서 MySQL 포트(3306) 열려있는지 확인
- 연결 정보 (host, user, password, db) 확인

### 포트 80 사용 불가
- 관리자 권한으로 실행하거나
- 5000번 포트 사용 + IIS 리버스 프록시 설정

---

**배포 성공하시길 바랍니다! 🚀**
