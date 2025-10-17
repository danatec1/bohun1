# 포트 사용 중인 프로세스 강제 종료 스크립트
# 사용법: .\kill_port.ps1 -Port 5001

param(
    [int]$Port = 5001
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  🔍 포트 $Port 사용 프로세스 확인" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 포트 사용 중인 프로세스 찾기
$connections = netstat -ano | findstr ":$Port"

if ($connections) {
    Write-Host "📊 포트 $Port 사용 현황:" -ForegroundColor Yellow
    Write-Host $connections
    Write-Host ""
    
    # PID 추출
    $pids = @()
    $connections -split "`n" | ForEach-Object {
        if ($_ -match '\s+(\d+)\s*$') {
            $pid = $matches[1]
            if ($pid -and $pid -ne "0" -and $pids -notcontains $pid) {
                $pids += $pid
            }
        }
    }
    
    if ($pids.Count -gt 0) {
        Write-Host "발견된 프로세스:" -ForegroundColor Yellow
        foreach ($pid in $pids) {
            try {
                $process = Get-Process -Id $pid -ErrorAction Stop
                Write-Host "  PID $pid : $($process.Name) - $($process.Path)" -ForegroundColor White
            } catch {
                Write-Host "  PID $pid : (알 수 없는 프로세스)" -ForegroundColor Gray
            }
        }
        
        Write-Host ""
        $confirm = Read-Host "이 프로세스들을 종료하시겠습니까? (Y/N)"
        
        if ($confirm -eq 'Y' -or $confirm -eq 'y') {
            foreach ($pid in $pids) {
                try {
                    Stop-Process -Id $pid -Force
                    Write-Host "  ✅ PID $pid 종료 완료" -ForegroundColor Green
                } catch {
                    Write-Host "  ❌ PID $pid 종료 실패: $($_.Exception.Message)" -ForegroundColor Red
                }
            }
            
            Start-Sleep -Seconds 2
            
            # 다시 확인
            $checkAgain = netstat -ano | findstr ":$Port"
            if ($checkAgain) {
                Write-Host ""
                Write-Host "⚠️  일부 프로세스가 아직 실행 중입니다:" -ForegroundColor Yellow
                Write-Host $checkAgain
            } else {
                Write-Host ""
                Write-Host "✅ 포트 $Port 가 정상적으로 해제되었습니다!" -ForegroundColor Green
            }
        } else {
            Write-Host "❌ 종료가 취소되었습니다." -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "✅ 포트 $Port 는 사용 중이 아닙니다." -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  다음 단계: python run.py 실행" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
