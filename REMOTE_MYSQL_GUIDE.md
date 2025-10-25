# 원격 MySQL 서버 연결 가이드

## 연결 정보
- **호스트**: 121.157.160.22
- **포트**: 3306
- **사용자**: root
- **비밀번호**: zzaaqq
- **데이터베이스**: testdb

## 1. 연결 전 확인사항

### 방화벽 설정
원격 서버(121.157.160.22)에서 포트 3306이 열려있어야 합니다:
```bash
# Linux 서버에서 확인
sudo firewall-cmd --list-ports
sudo ufw status

# 포트 열기 (필요시)
sudo firewall-cmd --permanent --add-port=3306/tcp
sudo firewall-cmd --reload
```

### MySQL 원격 접속 허용 설정
MySQL 서버에서 원격 접속을 허용해야 합니다:

```sql
-- 원격 접속 허용
GRANT ALL PRIVILEGES ON testdb.* TO 'root'@'%' IDENTIFIED BY 'zzaaqq';
FLUSH PRIVILEGES;

-- 또는 특정 IP만 허용
GRANT ALL PRIVILEGES ON testdb.* TO 'root'@'<your-ip>' IDENTIFIED BY 'zzaaqq';
FLUSH PRIVILEGES;
```

MySQL 설정 파일 수정:
```bash
# /etc/mysql/mysql.conf.d/mysqld.cnf 또는 /etc/my.cnf
bind-address = 0.0.0.0  # 모든 IP에서 접속 허용

# MySQL 재시작
sudo systemctl restart mysql
```

## 2. 연결 테스트

### PowerShell에서 테스트
```powershell
python -c "import pymysql; conn = pymysql.connect(host='121.157.160.22', port=3306, user='root', password='zzaaqq', database='testdb'); print('✅ 연결 성공'); conn.close()"
```

### MySQL CLI로 테스트
```powershell
mysql -h 121.157.160.22 -P 3306 -u root -pzzaaqq testdb
```

## 3. Flask 애플리케이션 실행

### 방법 1: 환경 변수 설정 (권장)
```powershell
# 스크립트 실행
.\set_remote_mysql.ps1

# 또는 직접 설정
$env:MYSQL_HOST = "121.157.160.22"
$env:MYSQL_PORT = "3306"  
$env:MYSQL_USER = "root"
$env:MYSQL_PASSWORD = "zzaaqq"
$env:MYSQL_DATABASE = "testdb"

# Flask 실행
python run.py
```

### 방법 2: 코드에 직접 설정 (이미 적용됨)
다음 파일들이 121.157.160.22로 설정되었습니다:
- `app/repositories/testdb_hospital_repository.py`
- `app/repositories/user_repository.py`
- `app/controllers/hospital_controller.py`

단순히 실행:
```powershell
python run.py
```

## 4. 접속 확인

브라우저에서:
- http://127.0.0.1:5000/folium-map

## 5. 문제 해결

### 연결 타임아웃
- 방화벽 확인
- MySQL 서버의 bind-address 확인
- 네트워크 연결 확인

### Access Denied 에러
```sql
-- MySQL 서버에서 실행
SELECT user, host FROM mysql.user WHERE user='root';
GRANT ALL PRIVILEGES ON testdb.* TO 'root'@'%' IDENTIFIED BY 'zzaaqq';
FLUSH PRIVILEGES;
```

### 데이터베이스 없음
```sql
-- MySQL 서버에서 실행
CREATE DATABASE testdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## 6. localhost로 되돌리기

원래대로 localhost 연결로 되돌리려면:
```powershell
# 각 파일에서 host를 'localhost'로 변경
# testdb_hospital_repository.py: host='localhost'
# user_repository.py: host='localhost'  
# hospital_controller.py: 'host': 'localhost'
```

또는 환경 변수 사용:
```powershell
$env:MYSQL_HOST = "localhost"
python run.py
```
