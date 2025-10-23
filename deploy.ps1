# Windows Server 배포 스크립트
# 사용법: .\deploy.ps1 -TargetPath "C:\webapp\bohun1"

param(
    [Parameter(Mandatory=$true)]
    [string]$TargetPath
)

Write-Host "=== Flask 차트 애플리케이션 배포 시작 ===" -ForegroundColor Cyan

# 1. 대상 폴더 생성
Write-Host "`n[1/5] 대상 폴더 생성..." -ForegroundColor Yellow
if (!(Test-Path $TargetPath)) {
    New-Item -Path $TargetPath -ItemType Directory -Force | Out-Null
    Write-Host "✅ 폴더 생성: $TargetPath" -ForegroundColor Green
} else {
    Write-Host "✅ 폴더 존재: $TargetPath" -ForegroundColor Green
}

# 2. 필수 파일 복사
Write-Host "`n[2/5] 필수 파일 복사..." -ForegroundColor Yellow

# app 폴더 (Python 코드)
Write-Host "  - app 폴더 복사 중..." -ForegroundColor Gray
robocopy "app" "$TargetPath\app" /E /NFL /NDL /NJH /NJS /NC /NS /NP | Out-Null
Write-Host "  ✅ app 폴더 복사 완료" -ForegroundColor Green

# public 폴더 (차트 HTML)
Write-Host "  - public 폴더 복사 중..." -ForegroundColor Gray
robocopy "public" "$TargetPath\public" /E /NFL /NDL /NJH /NJS /NC /NS /NP | Out-Null
Write-Host "  ✅ public 폴더 복사 완료" -ForegroundColor Green

# config 폴더
Write-Host "  - config 폴더 복사 중..." -ForegroundColor Gray
robocopy "config" "$TargetPath\config" /E /NFL /NDL /NJH /NJS /NC /NS /NP | Out-Null
Write-Host "  ✅ config 폴더 복사 완료" -ForegroundColor Green

# 루트 파일들
Write-Host "  - 루트 파일 복사 중..." -ForegroundColor Gray
Copy-Item "run.py" "$TargetPath\" -Force
Copy-Item "requirements.txt" "$TargetPath\" -Force
if (Test-Path "hospital.db") {
    Copy-Item "hospital.db" "$TargetPath\" -Force
}
Write-Host "  ✅ 루트 파일 복사 완료" -ForegroundColor Green

# 3. 차트 파일 확인
Write-Host "`n[3/5] 차트 파일 확인..." -ForegroundColor Yellow
$chartFiles = @(
    "chart3_scatter_matrix.html",
    "chart4_yearly_area.html", 
    "chart5_regional_bar.html",
    "chart6_pivot_bar.html",
    "chart7_pie_subplots.html"
)

$missingCharts = @()
foreach ($file in $chartFiles) {
    $path = Join-Path "$TargetPath\public" $file
    if (Test-Path $path) {
        Write-Host "  ✅ $file" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $file (누락됨!)" -ForegroundColor Red
        $missingCharts += $file
    }
}

if ($missingCharts.Count -gt 0) {
    Write-Host "`n⚠️  경고: 일부 차트 파일이 누락되었습니다!" -ForegroundColor Red
    Write-Host "누락된 파일: $($missingCharts -join ', ')" -ForegroundColor Red
}

# 4. Python 환경 확인
Write-Host "`n[4/5] Python 환경 확인..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✅ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ❌ Python이 설치되지 않았습니다!" -ForegroundColor Red
    Write-Host "  → https://www.python.org/downloads/ 에서 다운로드하세요" -ForegroundColor Yellow
    exit 1
}

# 5. 배포 요약
Write-Host "`n[5/5] 배포 완료 요약" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "📦 배포 경로: $TargetPath" -ForegroundColor White
Write-Host "📊 차트 파일: $($chartFiles.Count - $missingCharts.Count)/$($chartFiles.Count)개" -ForegroundColor White

$totalSize = (Get-ChildItem -Path $TargetPath -Recurse -ErrorAction SilentlyContinue | 
              Measure-Object -Property Length -Sum).Sum / 1MB
Write-Host "💾 전체 크기: $("{0:N2}" -f $totalSize) MB" -ForegroundColor White
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

# 6. 다음 단계 안내
Write-Host "`n📋 다음 단계:" -ForegroundColor Cyan
Write-Host "1. 배포 폴더로 이동:" -ForegroundColor Yellow
Write-Host "   cd $TargetPath" -ForegroundColor White
Write-Host "`n2. Python 패키지 설치:" -ForegroundColor Yellow
Write-Host "   pip install -r requirements.txt" -ForegroundColor White
Write-Host "`n3. MySQL 연결 정보 수정:" -ForegroundColor Yellow
Write-Host "   app\__init__.py 또는 config\ 파일 수정" -ForegroundColor White
Write-Host "`n4. 서버 실행:" -ForegroundColor Yellow
Write-Host "   python run.py" -ForegroundColor White
Write-Host "`n5. 브라우저에서 확인:" -ForegroundColor Yellow
Write-Host "   http://localhost:5000/c" -ForegroundColor White

Write-Host "`n🎉 배포 준비 완료!" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Cyan
