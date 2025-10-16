# 차트 API 종합 진단 스크립트
# 사용법: .\check_chart_api.ps1 [-ServerUrl "http://localhost:5001"]

param(
    [string]$ServerUrl = "http://localhost:5001"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  📊 차트 API 종합 진단 도구" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. 서버 응답 확인
Write-Host "[1] 메인 서버 응답 확인..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$ServerUrl" -TimeoutSec 5 -UseBasicParsing
    Write-Host "    ✅ 서버 응답 정상 (Status: $($response.StatusCode))" -ForegroundColor Green
} catch {
    Write-Host "    ❌ 서버 응답 없음: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "    해결: python run.py 또는 python run_production.py 실행 확인" -ForegroundColor Yellow
    exit 1
}

# 2. 차트 API 확인
Write-Host "`n[2] 차트 API 엔드포인트 확인..." -ForegroundColor Yellow
try {
    $apiResponse = Invoke-RestMethod -Uri "$ServerUrl/api/statistics/yearly" -Method GET
    if ($apiResponse.success) {
        Write-Host "    ✅ API 응답 정상" -ForegroundColor Green
        Write-Host "    📊 데이터 개수: $($apiResponse.data.Count)개 시도" -ForegroundColor Gray
        if ($apiResponse.data.Count -gt 0) {
            Write-Host "`n    샘플 데이터 (상위 3개):" -ForegroundColor Gray
            $apiResponse.data | Select-Object -First 3 | Format-Table -AutoSize
        }
    } else {
        Write-Host "    ❌ API 오류: $($apiResponse.error)" -ForegroundColor Red
    }
} catch {
    Write-Host "    ❌ API 호출 실패: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "    해결: MySQL 서버 및 테이블 '위탁병원현황_연도별현황' 확인" -ForegroundColor Yellow
}

# 3. Chart.js CDN 확인
Write-Host "`n[3] Chart.js CDN 접근성 확인..." -ForegroundColor Yellow
try {
    $cdnResponse = Invoke-WebRequest -Uri "https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js" -TimeoutSec 5 -UseBasicParsing
    $sizeKB = [math]::Round($cdnResponse.RawContentLength / 1024, 2)
    Write-Host "    ✅ Chart.js CDN 접근 가능 (크기: $sizeKB KB)" -ForegroundColor Green
} catch {
    Write-Host "    ❌ Chart.js CDN 접근 불가: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "    해결: public/js/chart.min.js로 로컬 파일 사용 권장" -ForegroundColor Yellow
}

# 4. MySQL 포트 확인
Write-Host "`n[4] MySQL 서비스 확인..." -ForegroundColor Yellow
try {
    $mysqlPort = Get-NetTCPConnection -LocalPort 3306 -State Listen -ErrorAction Stop
    Write-Host "    ✅ MySQL 서비스 실행 중 (포트 3306)" -ForegroundColor Green
    Write-Host "    PID: $($mysqlPort[0].OwningProcess)" -ForegroundColor Gray
} catch {
    Write-Host "    ❌ MySQL 서비스 미실행 (포트 3306 닫힘)" -ForegroundColor Red
    Write-Host "    해결: MySQL 서비스 시작 필요" -ForegroundColor Yellow
}

# 5. 애플리케이션 포트 확인
Write-Host "`n[5] 애플리케이션 포트 상태 확인..." -ForegroundColor Yellow
$appPorts = @(5001, 5211)
foreach ($port in $appPorts) {
    try {
        $portCheck = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction Stop
        Write-Host "    ✅ 포트 $port 리스닝 중 (PID: $($portCheck[0].OwningProcess))" -ForegroundColor Green
    } catch {
        Write-Host "    ⚠️  포트 $port 사용 안 함" -ForegroundColor Yellow
    }
}

# 6. 방화벽 규칙 확인
Write-Host "`n[6] 방화벽 규칙 확인..." -ForegroundColor Yellow
$firewallRules = Get-NetFirewallRule -DisplayName "*Flask*", "*5001*", "*5211*" -ErrorAction SilentlyContinue | 
                 Select-Object DisplayName, Enabled, Direction
if ($firewallRules) {
    Write-Host "    ✅ 방화벽 규칙 발견:" -ForegroundColor Green
    $firewallRules | Format-Table -AutoSize
} else {
    Write-Host "    ⚠️  방화벽 규칙 없음" -ForegroundColor Yellow
    Write-Host "    해결: New-NetFirewallRule로 포트 허용 필요" -ForegroundColor Yellow
}

# 7. 간단한 연결 테스트
Write-Host "`n[7] 최종 연결 테스트..." -ForegroundColor Yellow
$testUrl = "$ServerUrl/api/statistics/yearly"
try {
    $testResponse = Invoke-WebRequest -Uri $testUrl -TimeoutSec 3 -UseBasicParsing
    $contentLength = $testResponse.Content.Length
    Write-Host "    ✅ 최종 테스트 통과" -ForegroundColor Green
    Write-Host "    URL: $testUrl" -ForegroundColor Gray
    Write-Host "    응답 크기: $contentLength bytes" -ForegroundColor Gray
    Write-Host "    응답 시간: $($testResponse.Headers['Date'])" -ForegroundColor Gray
} catch {
    Write-Host "    ❌ 최종 테스트 실패" -ForegroundColor Red
    Write-Host "    $($_.Exception.Message)" -ForegroundColor Red
}

# 종합 판정
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  📋 진단 완료" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "다음 단계:" -ForegroundColor Yellow
Write-Host "1. 브라우저에서 F12 → Console 탭 확인" -ForegroundColor White
Write-Host "2. $ServerUrl/hospitals 페이지 접속" -ForegroundColor White
Write-Host "3. 차트가 안 보이면 Console 에러 메시지 확인" -ForegroundColor White
Write-Host ""
Write-Host "상세 가이드: docs\CHART_TROUBLESHOOTING.md" -ForegroundColor Cyan
