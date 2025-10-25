# MySQL 원격 연결 테스트 결과

## 📋 테스트 일시
2025-10-24

## 🎯 테스트 대상
- **호스트**: 121.157.160.22
- **포트**: 3306
- **데이터베이스**: testdb
- **사용자**: root

## ✅ 테스트 결과

### 1. Ping 테스트: **성공**
```
121.157.160.22의 응답: 바이트=32 시간=5ms TTL=113
121.157.160.22의 응답: 바이트=32 시간=8ms TTL=113
손실 = 0 (0% 손실)
```
✅ 서버는 온라인 상태이며 네트워크 연결이 정상입니다.

### 2. MySQL 포트(3306) 테스트: **실패 (타임아웃)**
❌ 포트 3306에 연결할 수 없습니다.

## 🔍 문제 원인 분석

포트 3306이 차단되어 있거나 MySQL이 외부 접속을 허용하지 않습니다.

## ✅ 해결 방법

### 원격 서버(121.157.160.22)에서 수행할 작업:

#### 1. MySQL 서비스 상태 확인
```bash
sudo systemctl status mysql
# 또는
sudo service mysql status
```

#### 2. 방화벽 포트 열기

**UFW 사용 시:**
```bash
sudo ufw allow 3306/tcp
sudo ufw reload
sudo ufw status
```

**firewalld 사용 시:**
```bash
sudo firewall-cmd --permanent --add-port=3306/tcp
sudo firewall-cmd --reload
sudo firewall-cmd --list-ports
```

**iptables 사용 시:**
```bash
sudo iptables -A INPUT -p tcp --dport 3306 -j ACCEPT
sudo service iptables save
```

#### 3. MySQL 외부 접속 허용 설정

**설정 파일 수정:**
```bash
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
# 또는
sudo nano /etc/my.cnf
```

다음 줄을 찾아서 수정:
```ini
# 기존 (로컬만 허용)
bind-address = 127.0.0.1

# 변경 (모든 IP 허용)
bind-address = 0.0.0.0
```

**MySQL 재시작:**
```bash
sudo systemctl restart mysql
# 또는
sudo service mysql restart
```

#### 4. MySQL 사용자 권한 설정

MySQL에 접속:
```bash
mysql -u root -p
```

권한 부여:
```sql
-- 모든 IP에서 접속 허용
GRANT ALL PRIVILEGES ON testdb.* TO 'root'@'%' IDENTIFIED BY 'zzaaqq';

-- 또는 특정 IP만 허용 (더 안전)
GRANT ALL PRIVILEGES ON testdb.* TO 'root'@'<your-client-ip>' IDENTIFIED BY 'zzaaqq';

-- 변경사항 적용
FLUSH PRIVILEGES;

-- 확인
SELECT user, host FROM mysql.user WHERE user='root';
```

#### 5. 클라우드/호스팅 서비스 보안 그룹 확인

AWS, Azure, GCP 등을 사용하는 경우:
- 보안 그룹(Security Group)에서 포트 3306 인바운드 규칙 추가
- 네트워크 ACL 확인

## 🧪 재테스트 방법

모든 설정 완료 후 다음 명령으로 테스트:

### Windows (PowerShell)에서:
```powershell
# 포트 테스트
Test-NetConnection -ComputerName 121.157.160.22 -Port 3306

# MySQL 연결 테스트
python -c "import pymysql; conn = pymysql.connect(host='121.157.160.22', port=3306, user='root', password='zzaaqq', database='testdb'); print('연결 성공!'); conn.close()"
```

### MySQL CLI로:
```powershell
mysql -h 121.157.160.22 -P 3306 -u root -pzzaaqq testdb
```

## 📝 현재 프로젝트 상태

코드는 이미 원격 서버 연결로 설정되어 있습니다:
- ✅ `app/repositories/testdb_hospital_repository.py`
- ✅ `app/repositories/user_repository.py`
- ✅ `app/controllers/hospital_controller.py`

원격 서버 설정이 완료되면:
```powershell
python run.py
```
만 실행하면 됩니다.

## 🔄 localhost로 되돌리기

원격 연결이 안 되면 임시로 localhost로 되돌릴 수 있습니다:

```powershell
# testdb_hospital_repository.py의 12번째 줄:
# host='121.157.160.22' → host='localhost'

# user_repository.py의 14번째 줄:
# host='121.157.160.22' → host='localhost'

# hospital_controller.py의 24번째 줄:
# 'host': '121.157.160.22' → 'host': 'localhost'
```

## 💡 추천 사항

1. **SSH 터널링 사용** (더 안전한 방법):
   ```powershell
   ssh -L 3307:localhost:3306 user@121.157.160.22
   ```
   그 후 localhost:3307로 연결

2. **VPN 사용**: 회사 네트워크라면 VPN 연결 후 시도

3. **localhost 유지**: 보안상 MySQL을 인터넷에 직접 노출하지 않는 것을 권장

## 📞 다음 단계

1. 원격 서버 관리자에게 위의 설정 확인 요청
2. 설정 완료 후 재테스트
3. 연결 성공 시 Flask 앱 실행

## ⚠️ 보안 경고

MySQL을 인터넷에 직접 노출하는 것은 보안 위험이 있습니다.
가능하면:
- SSH 터널링 사용
- VPN 사용
- 특정 IP만 허용
- 강력한 비밀번호 사용
