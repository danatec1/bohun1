# 🏥 보훈 병원 관리 시스템 - 빠른 참조 가이드

**버전**: 1.0 | **작성일**: 2025-10-09

---

## 🚀 빠른 시작

### 서버 실행
```powershell
cd c:\bohun1
python run.py
```

### 접속 주소
- http://127.0.0.1:5001

---

## 📁 주요 파일 목록

| 파일 | 역할 | 수정 가능 항목 |
|------|------|----------------|
| `run.py` | 서버 실행 | 포트, 디버그 모드 |
| `app/models/hospital.py` | 데이터 모델 | 속성 추가/제거 |
| `app/repositories/testdb_hospital_repository.py` | MySQL 연결 | 연결 정보, 쿼리 |
| `app/services/folium_map_service.py` | 지도 생성 | 색상, 마커, 타일 |
| `app/controllers/hospital_controller.py` | API 처리 | 엔드포인트 추가 |
| `app/templates/folium_map.html` | 지도 페이지 | UI, JavaScript |
| `public/css/style.css` | 스타일 | 색상, 레이아웃 |

---

## 🎨 마커 색상 변경

**파일**: `app/services/folium_map_service.py`  
**함수**: `_get_marker_color()`

```python
color_map = {
    '종합병원': 'red',      # 여기 색상 변경
    '재활병원': 'orange',   # 여기 색상 변경
    '요양병원': 'green',    # 여기 색상 변경
    '한방병원': 'purple',   # 여기 색상 변경
    '일반병원': 'blue'      # 여기 색상 변경
}
```

**사용 가능한 색상**:
red, blue, green, purple, orange, darkred, lightred, beige, darkblue, darkgreen, cadetblue, darkpurple, white, pink, lightblue, lightgreen, gray, black, lightgray

---

## 🏥 병원 유형 분류 변경

**파일**: `app/services/folium_map_service.py`  
**함수**: `_get_hospital_type()`

```python
def _get_hospital_type(self, medical_departments) -> str:
    departments_str = ' '.join(medical_departments)
    
    if '종합병원' in departments_str:
        return '종합병원'
    elif '재활' in departments_str:
        return '재활병원'
    elif '요양' in departments_str:
        return '요양병원'
    elif '한방' in departments_str or '한의' in departments_str:
        return '한방병원'
    # 새로운 유형 추가 가능
    else:
        return '일반병원'
```

---

## 🗺️ 지도 설정 변경

**파일**: `app/services/folium_map_service.py`  
**함수**: `create_hospital_map()`

### 지도 중심 좌표
```python
center_lat: float = 36.5,   # 위도 변경
center_lng: float = 127.5,  # 경도 변경
```

### 줌 레벨
```python
zoom_start: int = 7  # 7-13 권장
```

### 지도 타일 추가/제거
```python
# 새 타일 추가
folium.TileLayer(
    tiles='타일URL',
    name='표시이름',
    overlay=False,
    control=True
).add_to(m)
```

---

## 🔌 MySQL 연결 설정

**파일**: `app/repositories/testdb_hospital_repository.py`

```python
connection = pymysql.connect(
    host='localhost',      # 서버 주소
    user='root',          # 사용자명
    password='0000',      # 비밀번호
    database='testdb',    # 데이터베이스명
    charset='utf8mb4'
)
```

---

## 📊 Excel 컬럼 수정

**파일**: `app/services/folium_map_service.py`  
**함수**: `export_to_excel()`

```python
data.append({
    'ID': hospital.hospital_id,
    '병원명': hospital.name,
    '주소': hospital.address,
    '위도': hospital.latitude,
    '경도': hospital.longitude,
    '진료과목': ', '.join(hospital.medical_departments),
    # 새 컬럼 추가 가능
})
```

---

## 🎨 스타일 변경

**파일**: `public/css/style.css`

### 배경색
```css
body {
    background: #ffffff;  /* 흰색 */
}
```

### 헤더 색상
```css
.header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

### 버튼 색상
```css
.btn-primary {
    background: linear-gradient(135deg, #667eea, #764ba2);
}
```

---

## 🐛 문제 해결

### 포트 충돌
```powershell
Stop-Process -Name python -Force
python run.py
```

### 패키지 오류
```powershell
pip install -r requirements.txt
```

### 캐시 문제
- **브라우저**: Ctrl + F5
- **코드**: `style.css?v=새버전`

### MySQL 연결 오류
1. MySQL 서버 실행 확인
2. 연결 정보 확인
3. 방화벽 확인

---

## 🔧 자주 사용하는 명령어

### 서버 관리
```powershell
# 서버 시작
python run.py

# 프로세스 종료
Stop-Process -Name python -Force

# API 테스트
curl http://127.0.0.1:5001/api/map/folium
```

### 패키지 관리
```powershell
# 설치
pip install -r requirements.txt

# 업데이트
pip install --upgrade flask folium

# 목록 확인
pip list
```

### 데이터베이스
```sql
-- 병원 수 확인
SELECT COUNT(*) FROM `위탁병원현황`;

-- 유형별 통계
SELECT 종별, COUNT(*) as 개수
FROM `위탁병원현황`
GROUP BY 종별;
```

---

## 📋 체크리스트

### 서버 시작 전
- [ ] MySQL 서버 실행 중
- [ ] Python 패키지 설치 완료
- [ ] 포트 5001 사용 가능

### 지도 생성 전
- [ ] 인터넷 연결 확인 (타일 로드)
- [ ] 데이터베이스 연결 확인
- [ ] 905개 병원 데이터 존재 확인

### 배포 전
- [ ] debug=False 설정
- [ ] SECRET_KEY 설정
- [ ] 로깅 설정
- [ ] 에러 처리 확인

---

## 📞 긴급 연락처

| 항목 | 내용 |
|------|------|
| 시스템 관리자 | [담당자명] |
| 이메일 | [이메일] |
| 전화 | [전화번호] |
| 긴급 | [24시간 지원] |

---

## 📚 상세 문서

전체 운영 매뉴얼: `OPERATION_MANUAL.md`

---

**이 문서는 빠른 참조용입니다. 상세 내용은 OPERATION_MANUAL.md를 참조하세요.**
