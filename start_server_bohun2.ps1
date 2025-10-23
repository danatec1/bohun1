# ========================================
#  Windows Server bohun2 폴더 빠른 시작
# ========================================
# 위치: C:\inetpub\wwwroot\bohun2
# 사용법: 이 스크립트를 복사하여 실행

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  🚀 bohun2 Flask 서버 시작" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. 관리자 권한 확인
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "⚠️  관리자 권한 권장 (wwwroot 폴더)" -ForegroundColor Yellow
    Write-Host "    PowerShell 우클릭 → 관리자 권한으로 실행" -ForegroundColor Gray
    Write-Host ""
    $continue = Read-Host "계속 진행하시겠습니까? (Y/N)"
    if ($continue -ne 'Y' -and $continue -ne 'y') {
        Write-Host "❌ 종료" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "✅ 관리자 권한 확인" -ForegroundColor Green
}

# 2. 현재 위치 확인
Write-Host ""
Write-Host "[1] 현재 위치 확인..." -ForegroundColor Yellow
$currentPath = Get-Location
Write-Host "    현재 위치: $currentPath" -ForegroundColor White

if ($currentPath -ne "C:\inetpub\wwwroot\bohun2") {
    Write-Host "    → bohun2로 이동 중..." -ForegroundColor Gray
    cd C:\inetpub\wwwroot\bohun2
    Write-Host "    ✅ C:\inetpub\wwwroot\bohun2" -ForegroundColor Green
} else {
    Write-Host "    ✅ 이미 bohun2 폴더에 있음" -ForegroundColor Green
}

# 3. 프로젝트 파일 확인
Write-Host ""
Write-Host "[2] 프로젝트 파일 확인..." -ForegroundColor Yellow
$files = @("run_production.py", "run.py", "requirements.txt", "app")

foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "    ✅ $file" -ForegroundColor Green
    } else {
        Write-Host "    ❌ $file 없음" -ForegroundColor Red
    }
}

if (-not (Test-Path "run_production.py")) {
    Write-Host ""
    Write-Host "⚠️  run_production.py 파일이 없습니다!" -ForegroundColor Yellow
    Write-Host "    해결책: C:\bohun1에서 파일 복사" -ForegroundColor Gray
    Write-Host "    Copy-Item -Path 'C:\bohun1\*' -Destination 'C:\inetpub\wwwroot\bohun2' -Recurse -Force" -ForegroundColor Gray
    exit 1
}

# 4. Python 버전 확인
Write-Host ""
Write-Host "[3] Python 버전 확인..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "    ✅ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "    ❌ Python이 설치되지 않았거나 PATH에 없습니다" -ForegroundColor Red
    exit 1
}

# 5. 기존 Python 프로세스 확인 및 종료
Write-Host ""
Write-Host "[4] 기존 Python 프로세스 확인..." -ForegroundColor Yellow
$pythonProcs = Get-Process -Name python* -ErrorAction SilentlyContinue

if ($pythonProcs) {
    Write-Host "    ⚠️  실행 중인 Python: $($pythonProcs.Count)개" -ForegroundColor Yellow
    $pythonProcs | ForEach-Object {
        Write-Host "       PID $($_.Id): $($_.Path)" -ForegroundColor Gray
    }
    
    $killPython = Read-Host "    종료하시겠습니까? (Y/N)"
    if ($killPython -eq 'Y' -or $killPython -eq 'y') {
        $pythonProcs | Stop-Process -Force
        Start-Sleep -Seconds 2
        Write-Host "    ✅ Python 프로세스 종료 완료" -ForegroundColor Green
    }
} else {
    Write-Host "    ✅ 실행 중인 Python 프로세스 없음" -ForegroundColor Green
}

# 6. 포트 5001 확인
Write-Host ""
Write-Host "[5] 포트 5001 확인..." -ForegroundColor Yellow
$port5001 = netstat -ano | findstr :5001

if ($port5001) {
    Write-Host "    ⚠️  포트 5001 사용 중:" -ForegroundColor Yellow
    Write-Host $port5001 -ForegroundColor Gray
    
    # PID 추출
    $port5001 -match '\s+(\d+)\s*$' | Out-Null
    $pid = $matches[1]
    
    if ($pid) {
        $killPort = Read-Host "    PID $pid 종료하시겠습니까? (Y/N)"
        if ($killPort -eq 'Y' -or $killPort -eq 'y') {
            Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
            Start-Sleep -Seconds 2
            Write-Host "    ✅ 포트 5001 해제 완료" -ForegroundColor Green
        }
    }
} else {
    Write-Host "    ✅ 포트 5001 사용 안 함" -ForegroundColor Green
}

# 7. MySQL 서비스 확인
Write-Host ""
Write-Host "[6] MySQL 서비스 확인..." -ForegroundColor Yellow
$mysqlService = Get-Service -Name MySQL* -ErrorAction SilentlyContinue

if ($mysqlService) {
    if ($mysqlService.Status -eq 'Running') {
        Write-Host "    ✅ MySQL 서비스 실행 중 ($($mysqlService.Name))" -ForegroundColor Green
    } else {
        Write-Host "    ⚠️  MySQL 서비스 중지됨" -ForegroundColor Yellow
        $startMySQL = Read-Host "    MySQL 시작하시겠습니까? (Y/N)"
        if ($startMySQL -eq 'Y' -or $startMySQL -eq 'y') {
            Start-Service -Name $mysqlService.Name
            Write-Host "    ✅ MySQL 서비스 시작 완료" -ForegroundColor Green
        }
    }
} else {
    Write-Host "    ⚠️  MySQL 서비스를 찾을 수 없습니다" -ForegroundColor Yellow
}

# 8. 환경변수 설정
Write-Host ""
Write-Host "[7] 환경변수 설정..." -ForegroundColor Yellow
Write-Host "    MySQL root 비밀번호를 입력하세요" -ForegroundColor White

# 보안 입력
$securePassword = Read-Host "    비밀번호" -AsSecureString
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($securePassword)
$plainPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

$env:MYSQL_PASSWORD = $plainPassword
$env:PORT = "5001"

Write-Host "    ✅ 환경변수 설정 완료" -ForegroundColor Green
Write-Host "       PORT = 5001" -ForegroundColor Gray
Write-Host "       MYSQL_PASSWORD = ******" -ForegroundColor Gray

# 9. 최종 확인
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  📋 최종 확인" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "작업 위치: C:\inetpub\wwwroot\bohun2" -ForegroundColor White
Write-Host "실행 파일: run_production.py" -ForegroundColor White
Write-Host "서버 포트: 5001" -ForegroundColor White
Write-Host "MySQL 연결: localhost:3306" -ForegroundColor White
Write-Host ""

$confirm = Read-Host "Flask 서버를 시작하시겠습니까? (Y/N)"

if ($confirm -eq 'Y' -or $confirm -eq 'y') {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  🚀 Flask 서버 시작!" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "접속 주소:" -ForegroundColor Yellow
    Write-Host "  • 로컬: http://localhost:5001" -ForegroundColor Green
    Write-Host "  • 외부: http://서버IP:5001" -ForegroundColor Green
    Write-Host ""
    Write-Host "종료: Ctrl+C" -ForegroundColor Yellow
    Write-Host ""
    
    # 서버 실행
    python run_production.py
} else {
    Write-Host ""
    Write-Host "❌ 서버 시작 취소" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "수동 실행:" -ForegroundColor White
    Write-Host '  $env:MYSQL_PASSWORD = "비밀번호"' -ForegroundColor Gray
    Write-Host "  python run_production.py" -ForegroundColor Gray
}
