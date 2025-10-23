# 하이브리드 배포 가이드 (방법 2)
## React 빌드 + Flask 서빙

## 🎯 개념

```
[React 앱 빌드] → [정적 파일 생성] → [Flask가 서빙] → [python run.py로 실행]
```

**핵심**: 
- React 앱을 한 번 빌드하면 순수 HTML/CSS/JS 파일로 변환됨
- Flask는 이 정적 파일들을 서빙만 하면 됨
- Node.js 서버(localhost:4000) 불필요!

## 📝 단계별 실행

### Step 1: React 앱 빌드
```powershell
# Chart 폴더로 이동
cd c:\bohun1\Chart

# 프로덕션 빌드 실행
npm run build
```

**빌드 결과**:
```
c:\bohun1\Chart\dist\
├── index.html              # React 앱의 진입점
├── assets\
│   ├── index-*.js         # 번들된 JavaScript
│   └── index-*.css        # 번들된 CSS
├── data\                   # 복사된 데이터 파일
│   ├── images\
│   │   ├── 1.JPG
│   │   └── 2.JPG
│   └── chart_sync_info.json
└── *.html                  # Plotly 차트 파일들
```

### Step 2: 빌드 파일을 Flask static에 복사
```powershell
# Flask static 폴더에 chart-app 디렉토리 생성
New-Item -ItemType Directory -Path "c:\bohun1\app\static\chart-app" -Force

# 빌드된 모든 파일 복사
Copy-Item -Path "c:\bohun1\Chart\dist\*" -Destination "c:\bohun1\app\static\chart-app\" -Recurse -Force
```

**복사 후 구조**:
```
c:\bohun1\app\static\chart-app\
├── index.html
├── assets\
│   ├── index-abc123.js
│   └── index-def456.css
├── data\
│   ├── images\
│   └── chart_sync_info.json
└── chart3_scatter_matrix.html
    chart4_yearly_area.html
    ...
```

### Step 3: Flask 라우트 추가

**파일**: `c:\bohun1\app\routes\__init__.py`

```python
from flask import send_from_directory, current_app
import os

# 기존 코드...

# React 차트 앱 라우트 추가
@main_bp.route('/charts')
@main_bp.route('/charts/')
def chart_app():
    """React 차트 앱의 index.html 서빙"""
    return send_from_directory(
        os.path.join(current_app.root_path, 'static', 'chart-app'),
        'index.html'
    )

# React 앱의 정적 파일 서빙 (assets, data 등)
@main_bp.route('/charts/<path:path>')
def serve_chart_assets(path):
    """React 앱의 정적 파일들 서빙"""
    return send_from_directory(
        os.path.join(current_app.root_path, 'static', 'chart-app'),
        path
    )
```

### Step 4: Flask 서버 실행
```powershell
# bohun1 폴더로 이동
cd c:\bohun1

# Flask 서버 실행
python run.py
```

**출력 예시**:
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:80
 * Running on http://192.168.x.x:80
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
```

### Step 5: 브라우저에서 확인
```
http://localhost/charts
또는
http://localhost:80/charts
```

## ✅ 동작 원리

### 1. **사용자가 `/charts` 접속**
```
브라우저 → http://localhost/charts
```

### 2. **Flask가 index.html 반환**
```python
# app/routes/__init__.py
@main_bp.route('/charts')
def chart_app():
    return send_from_directory('static/chart-app', 'index.html')
```

### 3. **브라우저가 index.html 로드**
```html
<!-- index.html -->
<!DOCTYPE html>
<html>
  <head>
    <script type="module" src="/charts/assets/index-abc123.js"></script>
    <link rel="stylesheet" href="/charts/assets/index-def456.css">
  </head>
  <body>
    <div id="root"></div>
  </body>
</html>
```

### 4. **브라우저가 추가 리소스 요청**
```
GET /charts/assets/index-abc123.js
GET /charts/assets/index-def456.css
GET /charts/data/chart_sync_info.json
GET /charts/chart3_scatter_matrix.html
```

### 5. **Flask가 정적 파일 서빙**
```python
@main_bp.route('/charts/<path:path>')
def serve_chart_assets(path):
    # path = 'assets/index-abc123.js'
    # path = 'data/chart_sync_info.json'
    # path = 'chart3_scatter_matrix.html'
    return send_from_directory('static/chart-app', path)
```

## 🔧 Vite 설정 수정 필요

React 앱이 `/charts` 경로에서 서빙되므로 Vite 설정 수정이 필요합니다.

**파일**: `c:\bohun1\Chart\vite.config.ts`

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from "path"

export default defineConfig({
  plugins: [react()],
  base: '/charts/',  // 👈 이 줄 추가 (기본값은 '/')
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    port: 4000
  }
})
```

**중요**: `base: '/charts/'` 설정 후 다시 빌드해야 합니다!

```powershell
cd c:\bohun1\Chart
npm run build
Copy-Item -Path "dist\*" -Destination "c:\bohun1\app\static\chart-app\" -Recurse -Force
```

## 📊 전체 흐름도

```
개발 단계:
┌─────────────────┐
│ Chart/src/*.tsx │ ← React 소스 코드 수정
└────────┬────────┘
         │ npm run build
         ↓
┌─────────────────┐
│  Chart/dist/*   │ ← 빌드된 정적 파일
└────────┬────────┘
         │ Copy-Item
         ↓
┌──────────────────────┐
│ app/static/chart-app │ ← Flask가 서빙할 파일
└──────────┬───────────┘
           │
           ↓
배포/실행 단계:
┌──────────────┐
│ python run.py│ ← Flask 서버 시작
└──────┬───────┘
       │ http://localhost/charts
       ↓
┌─────────────┐
│   브라우저   │ ← React 앱 실행 (클라이언트 사이드)
└─────────────┘
```

## 🎯 장점

1. ✅ **단일 서버**: `python run.py` 하나만 실행
2. ✅ **포트 하나**: 80 포트만 사용 (4000 불필요)
3. ✅ **React 기능 유지**: 모든 인터랙티브 기능 보존
4. ✅ **통합 라우팅**: 
   - `http://localhost/` → Flask 메인 페이지
   - `http://localhost/hospitals` → 병원 CRUD
   - `http://localhost/charts` → React 차트 앱
5. ✅ **배포 간편**: Flask 앱만 배포하면 됨

## ⚠️ 주의사항

### 1. **빌드 후 복사 필요**
React 코드를 수정할 때마다:
```powershell
cd c:\bohun1\Chart
npm run build
Copy-Item -Path "dist\*" -Destination "c:\bohun1\app\static\chart-app\" -Recurse -Force
```

### 2. **개발 vs 프로덕션**
- **개발 중**: `npm run dev` (localhost:4000, HMR 활성화)
- **배포/테스트**: 빌드 후 Flask 서빙

### 3. **캐싱 문제**
브라우저 캐시로 인해 업데이트가 안 보일 수 있음:
- Ctrl + F5 (하드 새로고침)
- 또는 개발자 도구에서 캐시 비활성화

### 4. **API 경로**
React 앱에서 Flask API 호출 시 경로 주의:
```typescript
// 절대 경로 사용 (권장)
fetch('/api/hospitals')

// 상대 경로는 /charts 기준이므로 주의
fetch('api/hospitals')  // ❌ /charts/api/hospitals 호출됨
```

## 🔄 자동화 스크립트

빌드와 복사를 자동화하는 스크립트:

**파일**: `c:\bohun1\deploy_charts.ps1`

```powershell
# React 차트 앱 빌드 및 배포 자동화 스크립트

Write-Host "🚀 React 차트 앱 빌드 시작..." -ForegroundColor Cyan

# Chart 폴더로 이동
Set-Location "c:\bohun1\Chart"

# 빌드 실행
Write-Host "📦 npm run build 실행 중..." -ForegroundColor Yellow
npm run build

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ 빌드 성공!" -ForegroundColor Green
    
    # 대상 폴더 생성 (존재하지 않으면)
    $destPath = "c:\bohun1\app\static\chart-app"
    if (!(Test-Path $destPath)) {
        New-Item -ItemType Directory -Path $destPath -Force
        Write-Host "📁 폴더 생성: $destPath" -ForegroundColor Yellow
    }
    
    # 파일 복사
    Write-Host "📋 파일 복사 중..." -ForegroundColor Yellow
    Copy-Item -Path "dist\*" -Destination $destPath -Recurse -Force
    
    Write-Host "✅ 배포 완료!" -ForegroundColor Green
    Write-Host ""
    Write-Host "이제 Flask 서버를 실행하세요:" -ForegroundColor Cyan
    Write-Host "  cd c:\bohun1" -ForegroundColor White
    Write-Host "  python run.py" -ForegroundColor White
    Write-Host ""
    Write-Host "브라우저에서 확인:" -ForegroundColor Cyan
    Write-Host "  http://localhost/charts" -ForegroundColor White
    
} else {
    Write-Host "❌ 빌드 실패!" -ForegroundColor Red
    exit 1
}

# 원래 폴더로 돌아가기
Set-Location "c:\bohun1"
```

**사용법**:
```powershell
# PowerShell에서 실행
.\deploy_charts.ps1
```

## 🔥 빠른 시작 (Quick Start)

```powershell
# 1. 빌드 및 배포
cd c:\bohun1\Chart
npm run build
Copy-Item -Path "dist\*" -Destination "..\app\static\chart-app\" -Recurse -Force

# 2. Flask 실행
cd c:\bohun1
python run.py

# 3. 브라우저 접속
# http://localhost/charts
```

## 💡 팁

### VSCode Tasks로 자동화
`.vscode/tasks.json` 추가:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Deploy Charts",
      "type": "shell",
      "command": "cd Chart && npm run build && Copy-Item -Path 'dist\\*' -Destination '..\\app\\static\\chart-app\\' -Recurse -Force",
      "problemMatcher": [],
      "group": {
        "kind": "build",
        "isDefault": true
      }
    }
  ]
}
```

Ctrl+Shift+B로 빠르게 배포!

## 📝 체크리스트

빌드 및 배포 전:
- [ ] `Chart/vite.config.ts`에 `base: '/charts/'` 설정
- [ ] React 코드 수정 완료
- [ ] `npm run build` 실행
- [ ] `app/static/chart-app/` 폴더 확인
- [ ] `app/routes/__init__.py`에 라우트 추가
- [ ] `python run.py` 실행
- [ ] 브라우저에서 `/charts` 확인
