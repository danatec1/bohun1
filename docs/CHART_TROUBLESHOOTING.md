# 📊 차트 표시 문제 해결 가이드

## 배포 환경에서 차트가 안 보일 때 체크리스트

### 1️⃣ 브라우저 개발자 도구 확인 (최우선)

```
F12 → Console 탭 → 에러 메시지 확인
F12 → Network 탭 → API 요청 상태 확인
```

#### 주요 에러 유형

| 에러 | 원인 | 해결 방법 |
|------|------|-----------|
| `404 /api/statistics/yearly` | API 라우트 미등록 | routes/__init__.py 확인 |
| `500 Internal Server Error` | 서버 로직 오류 | 서버 로그 확인 |
| `Chart is not defined` | Chart.js CDN 로드 실패 | CDN 접근 확인 |
| `Failed to fetch` | 네트워크 연결 실패 | 방화벽/포트 확인 |
| `Access-Control-Allow-Origin` | CORS 오류 | Flask-CORS 설정 |

---

### 2️⃣ Chart.js CDN 접근 확인

#### 테스트 명령어 (PowerShell)
```powershell
# CDN 접근 테스트
Invoke-WebRequest -Uri "https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js" -UseBasicParsing
```

#### 해결 방법 1: 로컬 파일로 변경

**1단계: Chart.js 다운로드**
```powershell
# public/js/ 디렉토리로 이동
cd c:\bohun1\public\js

# Chart.js 다운로드
Invoke-WebRequest -Uri "https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js" -OutFile "chart.min.js"
```

**2단계: hospitals.html 수정**
```html
<!-- CDN 방식 (기존) -->
<!-- <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script> -->

<!-- 로컬 파일 방식 (변경) -->
<script src="/static/js/chart.min.js"></script>
```

#### 해결 방법 2: npm 패키지 설치
```bash
npm install chart.js
# 또는
pip install flask-assets
```

---

### 3️⃣ API 엔드포인트 확인

#### 브라우저에서 직접 테스트
```
http://localhost:5001/api/statistics/yearly
http://서버IP:5001/api/statistics/yearly
```

**정상 응답 예시:**
```json
{
  "success": true,
  "data": [
    {
      "광역지자체": "서울특별시",
      "2022년12월": 150,
      "2023년12월": 155,
      "2024년12월": 160
    },
    ...
  ]
}
```

**오류 응답 예시:**
```json
{
  "success": false,
  "error": "Table '위탁병원현황_연도별현황' doesn't exist"
}
```

#### PowerShell에서 테스트
```powershell
# API 호출 테스트
Invoke-RestMethod -Uri "http://localhost:5001/api/statistics/yearly" -Method GET | ConvertTo-Json -Depth 10
```

---

### 4️⃣ MySQL 데이터베이스 확인

#### 테이블 존재 여부 확인
```sql
-- MySQL에 접속
mysql -u root -p

USE testdb;

-- 테이블 확인
SHOW TABLES LIKE '위탁병원현황_연도별현황';

-- 데이터 확인
SELECT * FROM 위탁병원현황_연도별현황 LIMIT 5;

-- 데이터 개수 확인
SELECT COUNT(*) FROM 위탁병원현황_연도별현황;
```

#### 테이블이 없는 경우
```sql
-- 테이블 생성 (예시)
CREATE TABLE 위탁병원현황_연도별현황 (
    광역지자체 VARCHAR(20),
    `2022년12월` INT,
    `2023년12월` INT,
    `2024년12월` INT
);

-- 샘플 데이터 삽입
INSERT INTO 위탁병원현황_연도별현황 VALUES
('서울특별시', 150, 155, 160),
('부산광역시', 80, 82, 85),
('대구광역시', 60, 62, 65);
```

---

### 5️⃣ MySQL 연결 설정 확인

#### hospital_controller.py 확인
```python
# app/controllers/hospital_controller.py
self.db_config = {
    'host': 'localhost',      # ✅ 확인
    'user': 'root',            # ✅ 확인
    'password': 'Admin1',      # ✅ 확인
    'database': 'testdb',      # ✅ 확인
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}
```

#### 연결 테스트
```python
# Python 콘솔에서 테스트
import pymysql

try:
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='Admin1',
        database='testdb'
    )
    print("✅ MySQL 연결 성공")
    connection.close()
except Exception as e:
    print(f"❌ MySQL 연결 실패: {e}")
```

---

### 6️⃣ 방화벽 및 포트 확인

#### Windows 방화벽 규칙 확인
```powershell
# 포트 5001 규칙 확인
Get-NetFirewallRule -DisplayName "*5001*" | Select-Object DisplayName, Enabled, Direction

# 포트 5211 규칙 확인 (두 번째 서버 사용 시)
Get-NetFirewallRule -DisplayName "*5211*" | Select-Object DisplayName, Enabled, Direction
```

#### 포트 사용 중 확인
```powershell
# 포트 5001 리스닝 확인
netstat -ano | findstr :5001

# 포트 5211 리스닝 확인
netstat -ano | findstr :5211
```

---

### 7️⃣ 서버 로그 확인

#### Flask 개발 서버 로그
```powershell
# run.py 실행 시 콘솔 출력 확인
python run.py
```

**정상 로그 예시:**
```
 * Running on http://0.0.0.0:5001
 * Debugger is active!
127.0.0.1 - - [16/Oct/2025 10:30:15] "GET /api/statistics/yearly HTTP/1.1" 200 -
```

**오류 로그 예시:**
```
127.0.0.1 - - [16/Oct/2025 10:30:15] "GET /api/statistics/yearly HTTP/1.1" 500 -
Traceback (most recent call last):
  File "hospital_controller.py", line 243
    pymysql.err.OperationalError: (1045, "Access denied for user 'root'@'localhost'")
```

#### 운영 서버 로그 (Waitress)
```powershell
# run_production.py 실행 시 로그
python run_production.py
```

---

### 8️⃣ HTTPS/CORS 문제 (클라우드 배포 시)

#### Mixed Content 오류
```
Blocked loading mixed active content "http://..."
```

**해결 방법:**
```html
<!-- 프로토콜 상대 URL 사용 -->
<script src="//cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
```

#### CORS 오류
```python
# app/__init__.py에 추가
from flask_cors import CORS

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # CORS 설정 (필요 시)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    return app
```

---

### 9️⃣ 캐시 문제

#### 브라우저 캐시 삭제
```
Ctrl + Shift + Delete → 캐시된 이미지 및 파일 삭제
또는
Ctrl + F5 (하드 새로고침)
```

#### 서버 캐시 무효화
```python
# app/__init__.py
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # 개발 환경
```

---

### 🔟 환경변수 확인 (운영 환경)

```powershell
# 환경변수 확인
$env:FLASK_ENV
$env:PORT
$env:MYSQL_PASSWORD

# 환경변수 설정
$env:FLASK_ENV = "production"
$env:PORT = "5001"
```

---

## 🛠️ 빠른 디버깅 스크립트

### check_chart_api.ps1
```powershell
# 차트 API 종합 진단 스크립트
param(
    [string]$ServerUrl = "http://localhost:5001"
)

Write-Host "=== 차트 API 진단 시작 ===" -ForegroundColor Cyan

# 1. 서버 응답 확인
Write-Host "`n[1] 서버 응답 확인..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$ServerUrl" -TimeoutSec 5 -UseBasicParsing
    Write-Host "✅ 서버 응답 정상 (Status: $($response.StatusCode))" -ForegroundColor Green
} catch {
    Write-Host "❌ 서버 응답 없음: $_" -ForegroundColor Red
    exit 1
}

# 2. 차트 API 확인
Write-Host "`n[2] 차트 API 확인..." -ForegroundColor Yellow
try {
    $apiResponse = Invoke-RestMethod -Uri "$ServerUrl/api/statistics/yearly" -Method GET
    if ($apiResponse.success) {
        Write-Host "✅ API 응답 정상 (데이터 개수: $($apiResponse.data.Count))" -ForegroundColor Green
        Write-Host "샘플 데이터:" -ForegroundColor Gray
        $apiResponse.data | Select-Object -First 3 | Format-Table
    } else {
        Write-Host "❌ API 오류: $($apiResponse.error)" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ API 호출 실패: $_" -ForegroundColor Red
}

# 3. Chart.js CDN 확인
Write-Host "`n[3] Chart.js CDN 확인..." -ForegroundColor Yellow
try {
    $cdnResponse = Invoke-WebRequest -Uri "https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js" -TimeoutSec 5 -UseBasicParsing
    Write-Host "✅ Chart.js CDN 접근 가능 (크기: $($cdnResponse.RawContentLength) bytes)" -ForegroundColor Green
} catch {
    Write-Host "❌ Chart.js CDN 접근 불가: $_" -ForegroundColor Red
    Write-Host "해결 방법: 로컬 파일로 변경 필요" -ForegroundColor Yellow
}

# 4. MySQL 포트 확인
Write-Host "`n[4] MySQL 포트 확인..." -ForegroundColor Yellow
$mysqlPort = Get-NetTCPConnection -LocalPort 3306 -ErrorAction SilentlyContinue
if ($mysqlPort) {
    Write-Host "✅ MySQL 서비스 실행 중 (포트 3306)" -ForegroundColor Green
} else {
    Write-Host "❌ MySQL 서비스 미실행" -ForegroundColor Red
}

# 5. 애플리케이션 포트 확인
Write-Host "`n[5] 애플리케이션 포트 확인..." -ForegroundColor Yellow
$appPorts = @(5001, 5211)
foreach ($port in $appPorts) {
    $portCheck = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
    if ($portCheck) {
        Write-Host "✅ 포트 $port 리스닝 중" -ForegroundColor Green
    } else {
        Write-Host "⚠️  포트 $port 사용 안 함" -ForegroundColor Yellow
    }
}

Write-Host "`n=== 진단 완료 ===" -ForegroundColor Cyan
```

**사용 방법:**
```powershell
# 저장 후 실행
.\check_chart_api.ps1

# 또는 다른 서버 테스트
.\check_chart_api.ps1 -ServerUrl "http://192.168.1.100:5001"
```

---

## 📱 모바일/다른 기기에서 안 보일 때

### 1. 네트워크 확인
```powershell
# 서버 IP 확인
ipconfig

# 방화벽 규칙 확인
Get-NetFirewallRule -DisplayName "*Flask*" | Select-Object DisplayName, Enabled
```

### 2. CORS 헤더 추가
```python
# app/controllers/hospital_controller.py
def get_yearly_statistics(self):
    try:
        # ... 기존 코드 ...
        response = jsonify({'success': True, 'data': results})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        # ... 에러 처리 ...
```

---

## ✅ 최종 체크리스트

배포 전 확인사항:

- [ ] MySQL 서버 실행 중
- [ ] `위탁병원현황_연도별현황` 테이블 존재
- [ ] 테이블에 데이터 있음 (17개 시도)
- [ ] `/api/statistics/yearly` API 응답 정상
- [ ] Chart.js CDN 또는 로컬 파일 로드 가능
- [ ] 방화벽 포트 5001 (또는 5211) 오픈
- [ ] 브라우저 콘솔에 에러 없음
- [ ] Network 탭에서 API 200 응답 확인
- [ ] `hospitals.html` 페이지 정상 로드
- [ ] 서버 로그에 에러 없음

---

## 🆘 긴급 해결 방법

차트가 계속 안 보인다면:

### 1. 임시 테스트 페이지 생성
```html
<!-- test_chart.html -->
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
</head>
<body>
    <canvas id="testChart" width="400" height="400"></canvas>
    <script>
        new Chart(document.getElementById('testChart'), {
            type: 'pie',
            data: {
                labels: ['A', 'B', 'C'],
                datasets: [{
                    data: [10, 20, 30],
                    backgroundColor: ['red', 'blue', 'green']
                }]
            }
        });
    </script>
</body>
</html>
```

이 페이지가 표시되면 → Chart.js는 정상, API 문제
이 페이지도 안 보이면 → Chart.js CDN 문제

### 2. API 직접 확인
브라우저 주소창에 입력:
```
http://localhost:5001/api/statistics/yearly
```

JSON 데이터가 보이면 → API 정상, 프론트엔드 문제
에러가 보이면 → 백엔드 문제

---

## 📞 추가 지원

문제가 계속되면:
1. 브라우저 콘솔 전체 스크린샷
2. 서버 로그 전체 복사
3. `check_chart_api.ps1` 실행 결과
위 3가지를 확인해주세요.
