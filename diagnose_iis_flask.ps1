# IIS와 Flask 충돌 진단 및 해결 스크립트
# Windows Server IIS 환경에서 Flask 앱 실행 문제 해결

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  🔍 IIS + Flask 충돌 진단 도구" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. IIS 상태 확인
Write-Host "[1] IIS 서비스 상태 확인..." -ForegroundColor Yellow
try {
    $iisService = Get-Service -Name W3SVC -ErrorAction Stop
    Write-Host "  📊 IIS 상태: $($iisService.Status)" -ForegroundColor $(if ($iisService.Status -eq 'Running') { 'Green' } else { 'Yellow' })
    
    if ($iisService.Status -eq 'Running') {
        Write-Host "  ⚠️  IIS가 실행 중입니다. 포트 80/443을 사용 중일 수 있습니다." -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ℹ️  IIS가 설치되어 있지 않습니다." -ForegroundColor Gray
}

# 2. IIS 사이트 확인
Write-Host "`n[2] IIS 웹사이트 확인..." -ForegroundColor Yellow
try {
    Import-Module WebAdministration -ErrorAction Stop
    $sites = Get-Website
    
    if ($sites) {
        Write-Host "  📋 등록된 IIS 사이트:" -ForegroundColor White
        foreach ($site in $sites) {
            $bindings = $site.bindings.Collection | ForEach-Object { $_.bindingInformation }
            Write-Host "    • $($site.name) - 상태: $($site.state)" -ForegroundColor White
            Write-Host "      경로: $($site.physicalPath)" -ForegroundColor Gray
            Write-Host "      바인딩: $($bindings -join ', ')" -ForegroundColor Gray
        }
    } else {
        Write-Host "  ℹ️  등록된 IIS 사이트가 없습니다." -ForegroundColor Gray
    }
} catch {
    Write-Host "  ⚠️  IIS 관리 모듈을 불러올 수 없습니다." -ForegroundColor Yellow
}

# 3. 포트 80, 443, 5001 사용 현황
Write-Host "`n[3] 주요 포트 사용 현황..." -ForegroundColor Yellow
$ports = @(80, 443, 5001, 5211)
foreach ($port in $ports) {
    $connections = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
    if ($connections) {
        Write-Host "  🔴 포트 $port 사용 중:" -ForegroundColor Red
        foreach ($conn in $connections) {
            try {
                $process = Get-Process -Id $conn.OwningProcess -ErrorAction Stop
                Write-Host "    • PID $($conn.OwningProcess): $($process.Name) - $($process.Path)" -ForegroundColor White
            } catch {
                Write-Host "    • PID $($conn.OwningProcess): (알 수 없음)" -ForegroundColor Gray
            }
        }
    } else {
        Write-Host "  ✅ 포트 $port 사용 안 함" -ForegroundColor Green
    }
}

# 4. wwwroot 경로 확인
Write-Host "`n[4] wwwroot 경로 확인..." -ForegroundColor Yellow
$commonPaths = @(
    "C:\inetpub\wwwroot",
    "C:\inetpub\wwwroot\danatec1",
    "C:\bohun1"
)

foreach ($path in $commonPaths) {
    if (Test-Path $path) {
        Write-Host "  ✅ $path 존재" -ForegroundColor Green
        
        # Python 파일 확인
        $pyFiles = Get-ChildItem -Path $path -Filter "*.py" -ErrorAction SilentlyContinue
        if ($pyFiles) {
            Write-Host "    • Python 파일: $($pyFiles.Count)개 발견" -ForegroundColor Gray
        }
        
        # web.config 확인
        if (Test-Path "$path\web.config") {
            Write-Host "    • web.config 파일 존재 (IIS 배포 설정)" -ForegroundColor Cyan
        }
    } else {
        Write-Host "  ❌ $path 없음" -ForegroundColor Red
    }
}

# 5. Python 프로세스 확인
Write-Host "`n[5] 실행 중인 Python 프로세스..." -ForegroundColor Yellow
$pythonProcesses = Get-Process -Name python* -ErrorAction SilentlyContinue
if ($pythonProcesses) {
    Write-Host "  📊 Python 프로세스:" -ForegroundColor White
    foreach ($proc in $pythonProcesses) {
        Write-Host "    • PID $($proc.Id): $($proc.Name) - $($proc.Path)" -ForegroundColor White
        Write-Host "      시작 시간: $($proc.StartTime)" -ForegroundColor Gray
    }
} else {
    Write-Host "  ℹ️  실행 중인 Python 프로세스 없음" -ForegroundColor Gray
}

# 6. 문제 진단
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  📋 진단 결과 및 권장 사항" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# IIS가 80 또는 443 사용 중인지 확인
$port80Used = Get-NetTCPConnection -LocalPort 80 -State Listen -ErrorAction SilentlyContinue
$port443Used = Get-NetTCPConnection -LocalPort 443 -State Listen -ErrorAction SilentlyContinue

if ($port80Used -or $port443Used) {
    Write-Host "⚠️  IIS가 포트 80/443을 사용 중입니다." -ForegroundColor Yellow
    Write-Host "    Flask 개발 서버는 포트 5001을 사용하므로 충돌하지 않습니다." -ForegroundColor White
    Write-Host ""
}

# 포트 5001 사용 중인지 확인
$port5001Used = Get-NetTCPConnection -LocalPort 5001 -State Listen -ErrorAction SilentlyContinue
if ($port5001Used) {
    Write-Host "❌ 포트 5001이 이미 사용 중입니다!" -ForegroundColor Red
    Write-Host "    해결책: .\kill_port.ps1 -Port 5001 실행" -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "📝 권장 배포 방법:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1️⃣  IIS에서 Flask 배포 (운영 환경 권장)" -ForegroundColor White
Write-Host "   • HttpPlatformHandler 또는 Reverse Proxy 사용" -ForegroundColor Gray
Write-Host "   • 가이드: docs\IIS_DEPLOYMENT_GUIDE.md 참조" -ForegroundColor Gray
Write-Host ""
Write-Host "2️⃣  Waitress로 직접 실행 (간단한 배포)" -ForegroundColor White
Write-Host "   • python run_production.py 실행" -ForegroundColor Gray
Write-Host "   • 포트 5001에서 실행, IIS와 별도" -ForegroundColor Gray
Write-Host ""
Write-Host "3️⃣  개발 서버 실행 (개발/테스트용)" -ForegroundColor White
Write-Host "   • python run.py 실행" -ForegroundColor Gray
Write-Host "   • 포트 5001에서 실행, IIS와 별도" -ForegroundColor Gray
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  다음 단계" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "구체적인 에러 메시지를 알려주시면 정확한 해결책을 제공하겠습니다." -ForegroundColor Yellow
Write-Host "예: '액세스 권한', '포트 사용 중', 'Permission denied' 등" -ForegroundColor Gray
