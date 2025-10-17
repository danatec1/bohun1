# 🌐 IIS에서 Flask 애플리케이션 배포 가이드 (Windows Server)

## 📋 목차
1. [문제 상황 이해](#문제-상황-이해)
2. [IIS와 Flask 충돌 해결](#iis와-flask-충돌-해결)
3. [배포 방법 선택](#배포-방법-선택)
4. [IIS + Flask 통합 배포](#iis--flask-통합-배포)
5. [독립 실행 (권장)](#독립-실행-권장)

---

## 🔍 문제 상황 이해

### IIS wwwroot에서 `python run.py` 실행 시 발생하는 문제

```
IIS wwwroot/danatec1 폴더
    ↓
VS Code에서 python run.py 실행
    ↓
❌ 에러 발생
```

**일반적인 에러:**
- ❌ `액세스 권한에 의해 숨겨진 소켓...`
- ❌ `Permission denied`
- ❌ `포트가 이미 사용 중`
- ❌ `Address already in use`

---

## 🎯 IIS와 Flask 충돌 해결

### 충돌 원인

| 항목 | IIS | Flask 개발 서버 |
|------|-----|-----------------|
| 기본 포트 | 80, 443 | 5001 |
| 실행 방식 | Windows 서비스 | Python 프로세스 |
| 목적 | 운영 환경 웹서버 | 개발/테스트 |
| 충돌 | wwwroot 폴더 권한 | 포트 충돌 가능 |

### 📊 진단 스크립트 실행

```powershell
# PowerShell에서 실행
cd c:\bohun1
.\diagnose_iis_flask.ps1
```

이 스크립트는 자동으로:
- ✅ IIS 상태 확인
- ✅ 등록된 사이트 확인
- ✅ 포트 사용 현황 확인
- ✅ Python 프로세스 확인
- ✅ 권장 해결책 제시

---

## 🔧 배포 방법 선택

### 방법 1: IIS + Flask 통합 (복잡, 운영 환경)
- ✅ IIS의 강력한 기능 활용
- ✅ 자동 시작/재시작
- ❌ 설정 복잡

### 방법 2: Waitress 독립 실행 (권장, 간단)
- ✅ 설정 간단
- ✅ IIS와 별도 실행
- ✅ 포트만 다르게 설정
- ❌ IIS 기능 미활용

### 방법 3: 개발 서버 (개발/테스트만)
- ✅ 가장 간단
- ❌ 운영 환경 부적합
- ❌ 성능 제한

---

## 🌐 IIS + Flask 통합 배포

### 전제조건
```powershell
# IIS 설치 확인
Get-WindowsFeature -Name Web-Server

# Python 설치 확인
python --version

# wfastcgi 설치
pip install wfastcgi
wfastcgi-enable
```

### Step 1: web.config 생성

**`C:\inetpub\wwwroot\danatec1\web.config`**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
  <system.webServer>
    <handlers>
      <add name="PythonHandler" 
           path="*" 
           verb="*" 
           modules="FastCgiModule" 
           scriptProcessor="C:\Python312\python.exe|C:\Python312\Lib\site-packages\wfastcgi.py" 
           resourceType="Unspecified" 
           requireAccess="Script" />
    </handlers>
    
    <rewrite>
      <rules>
        <rule name="Flask" stopProcessing="true">
          <match url=".*" />
          <conditions>
            <add input="{REQUEST_FILENAME}" matchType="IsFile" negate="true" />
          </conditions>
          <action type="Rewrite" url="/" />
        </rule>
      </rules>
    </rewrite>
  </system.webServer>
  
  <appSettings>
    <add key="WSGI_HANDLER" value="run.app" />
    <add key="PYTHONPATH" value="C:\inetpub\wwwroot\danatec1" />
    <add key="WSGI_LOG" value="C:\inetpub\wwwroot\danatec1\logs\wfastcgi.log" />
  </appSettings>
</configuration>
```

**⚠️ 주의:** `C:\Python312\python.exe` 경로를 실제 Python 경로로 변경하세요.

### Step 2: IIS 사이트 설정

```powershell
# PowerShell (관리자 권한)

# 1. 사이트 생성 또는 확인
New-WebSite -Name "danatec1" `
    -PhysicalPath "C:\inetpub\wwwroot\danatec1" `
    -Port 80 `
    -Force

# 2. 애플리케이션 풀 설정
Set-ItemProperty "IIS:\AppPools\danatec1" -Name "enable32BitAppOnWin64" -Value $false
Set-ItemProperty "IIS:\AppPools\danatec1" -Name "managedRuntimeVersion" -Value ""

# 3. FastCGI 설정
# IIS Manager에서 수동 설정 필요
```

### Step 3: 권한 설정

```powershell
# IIS_IUSRS에 읽기/실행 권한 부여
icacls "C:\inetpub\wwwroot\danatec1" /grant "IIS_IUSRS:(OI)(CI)RX" /T

# 로그 폴더 쓰기 권한
New-Item -ItemType Directory -Path "C:\inetpub\wwwroot\danatec1\logs" -Force
icacls "C:\inetpub\wwwroot\danatec1\logs" /grant "IIS_IUSRS:(OI)(CI)M" /T
```

---

## ⚡ 독립 실행 (권장)

**IIS와 별도로 Flask를 실행하는 방법**

### 장점
- ✅ IIS 설정 불필요
- ✅ 설정 간단
- ✅ 디버깅 용이
- ✅ IIS는 정적 파일만 제공 (선택)

### Step 1: 프로젝트 위치 확인

```powershell
# 권장: IIS wwwroot 밖에 프로젝트 배치
# 예: C:\apps\bohun1 또는 C:\bohun1

# 현재 위치가 wwwroot 안이라면
cd C:\inetpub\wwwroot\danatec1

# 파일 확인
dir
```

### Step 2: 포트 충돌 확인 및 해결

```powershell
# 포트 5001 사용 여부 확인
.\kill_port.ps1 -Port 5001

# 또는 수동 확인
netstat -ano | findstr :5001
```

### Step 3: 서버 실행

#### 방법 A: 개발 서버 (개발/테스트)
```powershell
# 환경변수 설정 (MySQL 비밀번호)
$env:MYSQL_PASSWORD = "실제비밀번호"

# 서버 실행
python run.py
```

#### 방법 B: Waitress 운영 서버 (권장)
```powershell
# 환경변수 설정
$env:MYSQL_PASSWORD = "실제비밀번호"
$env:PORT = "5001"

# 운영 서버 실행
python run_production.py
```

### Step 4: 접속 테스트

```
로컬: http://localhost:5001
외부: http://서버IP:5001
```

### Step 5: Windows 서비스로 등록 (자동 시작)

```powershell
# NSSM 설치 (관리자 권한)
choco install nssm

# 서비스 등록
nssm install BohunHospital "C:\Python312\python.exe" "C:\bohun1\run_production.py"

# 환경변수 설정
nssm set BohunHospital AppEnvironmentExtra MYSQL_PASSWORD=실제비밀번호

# 작업 디렉토리 설정
nssm set BohunHospital AppDirectory "C:\bohun1"

# 서비스 시작
nssm start BohunHospital

# 서비스 상태 확인
nssm status BohunHospital
```

---

## 🔄 IIS를 리버스 프록시로 사용

**Flask는 5001 포트에서 실행, IIS는 80 포트에서 프록시**

### Step 1: URL Rewrite 모듈 설치
```
https://www.iis.net/downloads/microsoft/url-rewrite
```

### Step 2: Application Request Routing 설치
```
https://www.iis.net/downloads/microsoft/application-request-routing
```

### Step 3: web.config 설정

**`C:\inetpub\wwwroot\danatec1\web.config`**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
  <system.webServer>
    <rewrite>
      <rules>
        <rule name="ReverseProxyToFlask" stopProcessing="true">
          <match url="(.*)" />
          <action type="Rewrite" url="http://localhost:5001/{R:1}" />
        </rule>
      </rules>
    </rewrite>
  </system.webServer>
</configuration>
```

### Step 4: Flask 서버 실행

```powershell
# 백그라운드에서 Flask 실행
python run_production.py
```

### Step 5: 접속

```
http://서버IP → IIS (80) → Flask (5001)
```

---

## 🆘 문제 해결

### 1. "액세스 권한" 에러

**원인:** wwwroot 폴더 권한 문제

**해결:**
```powershell
# 관리자 권한으로 PowerShell 실행
cd C:\inetpub\wwwroot\danatec1
python run.py
```

또는 프로젝트를 wwwroot 밖으로 이동:
```powershell
# C:\bohun1로 이동
Copy-Item -Path "C:\inetpub\wwwroot\danatec1\*" -Destination "C:\bohun1" -Recurse
cd C:\bohun1
python run.py
```

### 2. "포트 사용 중" 에러

```powershell
# 포트 강제 해제
.\kill_port.ps1 -Port 5001

# 또는 다른 포트 사용
$env:PORT = "5002"
python run.py
```

### 3. IIS 사이트가 작동하지 않음

```powershell
# IIS 재시작
iisreset

# 사이트 재시작
Restart-WebAppPool -Name "danatec1"
```

### 4. Python 경로 오류

```powershell
# Python 경로 확인
where python
python --version

# web.config의 Python 경로 수정 필요
```

---

## ✅ 최종 권장 구성

### 개발/테스트 환경
```
VS Code + python run.py
포트: 5001
위치: C:\bohun1
```

### 운영 환경 (간단)
```
python run_production.py (Waitress)
포트: 5001
Windows 서비스로 등록
위치: C:\bohun1
```

### 운영 환경 (고급)
```
IIS (포트 80) → 리버스 프록시 → Flask (포트 5001)
위치: C:\bohun1
Windows 서비스로 Flask 등록
```

---

## 📞 에러 메시지별 해결책

| 에러 메시지 | 원인 | 해결 |
|------------|------|------|
| 액세스 권한 | wwwroot 권한 | 관리자 권한 또는 폴더 이동 |
| 포트 사용 중 | 5001 충돌 | `.\kill_port.ps1 -Port 5001` |
| Permission denied | 폴더 권한 | `icacls` 명령으로 권한 부여 |
| MySQL 연결 실패 | 비밀번호 | 환경변수 설정 확인 |
| 404 Not Found | 라우팅 | web.config 확인 |

---

## 🚀 빠른 시작 (권장 방법)

```powershell
# 1단계: 진단 실행
cd C:\bohun1
.\diagnose_iis_flask.ps1

# 2단계: 포트 확인
.\kill_port.ps1 -Port 5001

# 3단계: 환경변수 설정
$env:MYSQL_PASSWORD = "실제비밀번호"

# 4단계: 서버 실행
python run_production.py

# 5단계: 브라우저 테스트
# http://localhost:5001
```

---

## 📝 체크리스트

배포 전 확인사항:

- [ ] IIS 상태 확인 (`.\diagnose_iis_flask.ps1`)
- [ ] 포트 5001 사용 가능 확인
- [ ] MySQL 서비스 실행 중
- [ ] MYSQL_PASSWORD 환경변수 설정
- [ ] 방화벽 포트 5001 오픈
- [ ] 프로젝트 위치 적절 (wwwroot 권장 안 함)
- [ ] Python 버전 확인 (3.12 이상)
- [ ] requirements.txt 패키지 설치 완료

---

**구체적인 에러 메시지를 알려주시면 정확한 해결책을 제공하겠습니다!** 🎯
