# 원격 MySQL 서버 연결 설정
$env:MYSQL_HOST = "121.157.160.22"
$env:MYSQL_PORT = "3306"
$env:MYSQL_USER = "root"
$env:MYSQL_PASSWORD = "zzaaqq"
$env:MYSQL_DATABASE = "testdb"

Write-Host "✅ MySQL 환경 변수 설정 완료" -ForegroundColor Green
Write-Host "호스트: $env:MYSQL_HOST" -ForegroundColor Cyan
Write-Host "포트: $env:MYSQL_PORT" -ForegroundColor Cyan
Write-Host "데이터베이스: $env:MYSQL_DATABASE" -ForegroundColor Cyan
Write-Host ""
Write-Host "Flask 서버를 시작하려면:" -ForegroundColor Yellow
Write-Host "python run.py" -ForegroundColor White
