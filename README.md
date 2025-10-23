# 보훈 병원 관리 시스템

MVC 패턴을 기반으로 한 병원 정보 관리 및 통계 차트 시각화 웹 애플리케이션입니다.

## 프로젝트 구조

```
bohun1/
├── app/                    # 메인 애플리케이션
│   ├── controllers/        # 컨트롤러 (C)
│   │   ├── hospital_controller.py
│   │   └── main_controller.py
│   ├── models/            # 모델 (M)
│   │   └── hospital.py
│   ├── repositories/      # 데이터 접근 계층
│   │   ├── hospital_repository.py
│   │   └── mysql_hospital_repository.py
│   ├── services/          # 비즈니스 로직 계층
│   │   └── hospital_service.py
│   ├── templates/         # 뷰 템플릿 (V)
│   │   ├── base.html
│   │   ├── index.html      # 메인 랜딩 페이지
│   │   ├── hospitals.html  # 통계 차트 (챠트1)
│   │   ├── c.html         # 스크롤 차트 페이지
│   │   └── c_1.html       # 햄버거 메뉴 차트 페이지 (챠트2)
│   ├── routes/            # 라우팅 설정
│   │   └── __init__.py
│   ├── static/            # 정적 파일 (새 위치)
│   │   ├── chart-app/     # React 차트 앱
│   │   └── images/
│   └── __init__.py        # 애플리케이션 팩토리
├── config/                # 설정 파일
│   └── __init__.py
├── public/                # Plotly 차트 HTML 파일
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── main.js
│   │   └── hospitals.js
│   ├── images/
│   └── chart*.html        # 차트 3-7 (Plotly)
├── Chart/                 # React 차트 프로젝트
├── tests/                 # 테스트 파일
├── run.py                 # 개발 서버 실행 파일
└── run_prod.py           # 프로덕션 서버 실행 파일
```

## 주요 기능

### 1. 병원 정보 관리
- **CRUD 기능**: 병원 정보 생성, 조회, 수정, 삭제
- **검색 기능**: 병원명, 위치 기반 검색
- **지도 시각화**: Leaflet.js를 이용한 병원 위치 표시

### 2. 통계 차트 시스템
- **위탁병원증감현황 (hospitals.html)**: 
  - 연도별, 지자체별 위탁병원수 현황
  - Grafana 스타일 파이 차트 (2022, 2023, 2024)
  - 시군구별 가로 막대 차트
  - Chart.js 사용
  
- **위탁병원이용인원현황 (c_1.html)**:
  - 햄버거 메뉴 방식 네비게이션
  - Plotly 차트 5개 (월별 이용 인원 추이)
  - 사이드바 기본 열림 상태
  - 반응형 디자인

### 3. 네비게이션 시스템
- **메인 페이지**: Split-button 카드 방식 네비게이션
  - 위탁병원증감현황 → `/hospitals` (연도별 증감 통계)
  - 위탁병원이용인원현황 → `/c1` (월별 이용 인원 분석)
- **차트 간 이동**: 각 차트 페이지에 상호 링크 버튼 배치
  - hospitals.html: "📈위탁병원이용인원현황" 버튼
  - c_1.html: "📊위탁병원증감현황" + "🏠홈으로" 버튼

### 4. UI/UX 특징
- **반응형 디자인**: 모바일 친화적 레이아웃
- **모던 스타일**: 그라데이션 버튼, 부드러운 애니메이션
- **다크 테마**: Grafana 스타일 차트 인터페이스

## 기술 스택

### Backend
- **Framework**: Flask (Python 3.x)
- **Database**: SQLite / MySQL
- **ORM**: SQLAlchemy (Repository Pattern)

### Frontend
- **Core**: HTML5, CSS3, JavaScript (ES6+)
- **차트 라이브러리**: 
  - Chart.js (Grafana 스타일 차트)
  - Plotly (인터랙티브 차트)
  - Recharts (React 차트)
- **지도**: Leaflet.js
- **React**: Vite + TypeScript (Chart 앱)

### Architecture
- **Pattern**: MVC (Model-View-Controller)
- **Design**: Repository Pattern, Service Layer
- **UI**: Responsive Design, Mobile-First

## 설치 및 실행

### 1. 저장소 복제

```bash
git clone https://github.com/danatec1/bohun1.git
cd bohun1
```

### 2. 가상환경 생성 및 활성화

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. 의존성 설치

```bash
pip install -r requirements.txt
```

### 4. 샘플 데이터 생성 (선택사항)

```bash
python create_sample_data.py
```

### 5. 애플리케이션 실행

**개발 모드:**
```bash
python run.py
```

**프로덕션 모드:**
```bash
python run_prod.py
```

**또는 Flask CLI:**
```bash
flask run
```

### 6. 브라우저에서 접속

```
http://localhost:5000
```

## 페이지 구조 및 라우팅

### 메인 페이지
- **URL**: `/`
- **설명**: 랜딩 페이지, Split-button 네비게이션
- **기능**: 
  - 위탁병원증감현황 버튼 → `/hospitals`
  - 위탁병원이용인원현황 버튼 → `/c1`
  - 위탁병원 검색 → `/hospital_crud`
  - 위탁병원 위치정보(GIS) → `/folium-map`

### 통계 차트 페이지

#### 위탁병원증감현황 (Grafana 스타일)
- **URL**: `/hospitals`
- **차트 유형**: 
  - 파이 차트 3개 (2022, 2023, 2024년도)
  - 가로 막대 차트 (시군구별 현황)
- **기술**: Chart.js
- **네비게이션**: "📈위탁병원이용인원현황" 버튼 (우측 상단)

#### 위탁병원이용인원현황 (햄버거 메뉴)
- **URL**: `/c1`
- **차트 유형**: Plotly 인터랙티브 차트 5개
  - 전국 위탁병원 월별 평균이용 인원추이 (산점도 행렬)
  - 전국 위탁병원 년도년월 인원 상관관계 (Area 차트)
  - 광역지자체별 년도별 위탁병원 이용인원 (그룹 막대)
  - 광역지자체별 년도별 지역별 위탁병원 이용인원 (Pivot 막대)
  - 년도별 광역지자체 코드별 위탁병원 이용인원 비율 (파이 서브플롯)
- **기술**: Plotly
- **네비게이션**: 
  - 햄버거 메뉴 (좌측)
  - "📊위탁병원증감현황" + "🏠홈으로" 버튼 (우측)

#### 스크롤 차트 페이지
- **URL**: `/c`
- **설명**: 모든 차트를 스크롤 방식으로 표시
- **차트 크기**: 1800px 너비

### 개별 차트 라우트
- `/chart3` - 상관관계 히트맵
- `/chart4` - 연도별 영역 차트
- `/chart5` - 지역별 막대 차트
- `/chart6` - 피벗 막대 차트
- `/chart7` - 파이 서브플롯

## API 엔드포인트

### 병원 관리 API
- `GET /api/hospitals` - 모든 병원 목록 조회
- `POST /api/hospitals` - 새 병원 생성
- `GET /api/hospitals/<id>` - 특정 병원 조회
- `PUT /api/hospitals/<id>` - 병원 정보 수정
- `DELETE /api/hospitals/<id>` - 병원 삭제
- `GET /api/hospitals/search` - 병원 검색

### 통계 API
- `GET /api/statistics/yearly` - 연도별 통계 데이터
  - 응답 형식: `{ success: true, data: [...] }`
  - 데이터: 광역지자체별 2022/2023/2024년 위탁병원 수

### 지도 API
- `GET /folium-map` - Folium 지도 생성 및 표시

## 환경 변수

`.env` 파일 또는 환경 변수 설정:

```bash
# Flask 설정
FLASK_ENV=development          # 환경 설정 (development/production/testing)
FLASK_APP=run.py              # Flask 앱 진입점
SECRET_KEY=your-secret-key    # Flask 보안 키 (필수)

# 데이터베이스 설정
DATABASE_PATH=hospital.db     # SQLite 데이터베이스 경로

# 서버 설정
PORT=5000                     # 서버 포트
HOST=0.0.0.0                  # 호스트 (프로덕션: 0.0.0.0)

# 디버그 모드
DEBUG=True                    # 개발 모드 디버깅 활성화
```

## 프로젝트 특징

### 1. 네비게이션 시스템
- **Split-Button 카드**: 메인 페이지에서 명확한 차트 옵션 제공
  - 위탁병원증감현황 (연도별 증감 통계)
  - 위탁병원이용인원현황 (월별 이용 인원 분석)
- **상호 링크**: 각 차트 페이지 간 원활한 이동
- **햄버거 메뉴**: 이용인원현황에서 5개 차트 간 빠른 전환

### 2. 차트 시각화
- **Grafana 스타일**: 다크 테마, 프로페셔널한 디자인
- **인터랙티브**: Plotly를 통한 줌, 팬, 호버 기능
- **반응형**: 모바일/태블릿/데스크톱 대응

### 3. 코드 구조
- **MVC 패턴**: 명확한 관심사 분리
- **Repository 패턴**: 데이터 접근 추상화
- **Service Layer**: 비즈니스 로직 캡슐화

### 4. UI/UX 개선사항
- **모던 디자인**: 그라데이션 버튼, 부드러운 트랜지션
- **직관적 네이밍**: 
  - 기존: "챠트1", "챠트2"
  - 개선: "위탁병원증감현황", "위탁병원이용인원현황"
- **사용자 경험**: 
  - 햄버거 메뉴 기본 열림 (차트 즉시 접근)
  - 우측 네비게이션 버튼 그룹
  - 시각적 피드백 (호버 효과)
  - 명확한 페이지 제목 및 버튼 레이블

## MVC 아키텍처

### Model (모델)
- **`hospital.py`**: 병원 데이터 모델 정의
  - 병원 ID, 이름, 주소, 진료과목 등
- **`hospital_repository.py`**: SQLite 데이터베이스 접근 계층
  - CRUD 작업 추상화
- **`mysql_hospital_repository.py`**: MySQL 데이터베이스 접근 계층
- **`hospital_service.py`**: 비즈니스 로직 계층
  - 데이터 검증, 변환, 집계

### View (뷰)
- **`templates/`**: Jinja2 HTML 템플릿
  - `base.html`: 기본 레이아웃 (네비게이션, 푸터)
  - `index.html`: 메인 랜딩 페이지
  - `hospitals.html`: 통계 차트 페이지 (챠트1)
  - `c_1.html`: 햄버거 메뉴 차트 페이지 (챠트2)
  - `c.html`: 스크롤 차트 페이지
  
- **`public/` & `app/static/`**: 정적 파일
  - CSS: 스타일시트
  - JavaScript: 클라이언트 로직
  - Images: 이미지 리소스
  - Chart HTML: Plotly 생성 차트

### Controller (컨트롤러)
- **`hospital_controller.py`**: 병원 관련 HTTP 요청 처리
  - REST API 엔드포인트
  - JSON 응답 생성
- **`main_controller.py`**: 페이지 렌더링 요청 처리
  - 템플릿 렌더링
  - 차트 페이지 라우팅
- **`routes/__init__.py`**: URL 라우팅 설정
  - Blueprint 등록
  - URL 패턴 매핑

## 개발 가이드

### 새 차트 추가하기

1. **Plotly 차트 생성**:
   ```python
   # generate_plotly_chart.py
   import plotly.graph_objects as go
   fig = go.Figure(...)
   fig.write_html('public/chart8.html')
   ```

2. **라우트 추가** (`app/routes/__init__.py`):
   ```python
   @app.route('/chart8')
   def chart8():
       return send_from_directory('public', 'chart8.html')
   ```

3. **네비게이션 추가** (`c_1.html`):
   ```html
   <li><a href="/chart8" data-chart="8">📊 Chart 8</a></li>
   ```

### 스타일 커스터마이징

- **차트 색상**: `hospitals.html` 내 `pieColors`, `barColors` 배열 수정
- **버튼 스타일**: `.home-button` CSS 클래스 수정
- **레이아웃**: `.chart-header`, `.nav-buttons` 클래스 조정

### 데이터 업데이트

1. **CSV 데이터 준비**: 광역지자체, 연도별 데이터
2. **데이터베이스 갱신**: `create_sample_data.py` 실행
3. **API 확인**: `/api/statistics/yearly` 응답 검증

## 배포

### 프로덕션 체크리스트

- [ ] `FLASK_ENV=production` 설정
- [ ] `DEBUG=False` 설정
- [ ] `SECRET_KEY` 강력한 값으로 변경
- [ ] 데이터베이스 백업
- [ ] HTTPS 설정
- [ ] CORS 설정 확인
- [ ] 정적 파일 캐싱 설정

### 추천 배포 방법

**Gunicorn + Nginx:**
```bash
# Gunicorn 설치
pip install gunicorn

# 실행
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

**Docker:**
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "run_prod.py"]
```

## 문제 해결

### 차트가 표시되지 않음
- 브라우저 콘솔에서 JavaScript 오류 확인
- `/api/statistics/yearly` API 응답 확인
- Chart.js / Plotly 라이브러리 로드 확인

### 데이터베이스 오류
- `hospital.db` 파일 존재 확인
- `create_sample_data.py` 실행하여 초기 데이터 생성
- 파일 권한 확인

### 포트 충돌
- `PORT` 환경 변수 변경
- 또는 `run.py`에서 포트 번호 수정

## 업데이트 이력

### v2.1 (2025-10-23)
- 🏷️ 네비게이션 레이블 개선
  - Split-button 레이블 명확화
    - "챠트1" → "위탁병원증감현황"
    - "챠트2" → "위탁병원이용인원현황"
  - 모든 페이지 간 네비게이션 버튼 통일
  - 사용자 친화적 한글 레이블 적용
- 📝 메인 페이지 기능 카드 설명 개선
  - "위탁병원 증감 및 이용인원 현황" 제목 추가
  - 상세 설명: "연도별, 지역별 증감 및 이용인원 데이터 통계 시각화"

### v2.0 (2025-10-23)
- ✨ 챠트2 네비게이션 버튼 추가 (hospitals.html)
- 🎨 Split-button 카드 디자인 개선
- 📊 5개 Plotly 차트 추가 (c_1.html)
- 🔧 햄버거 메뉴 기본 열림 상태 설정
- 📱 반응형 네비게이션 시스템 구현
- 📦 Chart 폴더 추가 (React + Vite)
- 🗂️ 프로젝트 구조 재구성

### v1.0 (Initial Release)
- 🏥 병원 CRUD 기능
- 🗺️ Leaflet 지도 연동
- 📊 기본 통계 차트
- 🔍 검색 기능

## 스크린샷

### 메인 페이지
- Split-button 네비게이션 카드
- 모던하고 직관적인 UI

### 챠트1 (hospitals.html)
- Grafana 스타일 다크 테마
- 3개 파이 차트 (연도별 위탁병원 수)
- 가로 막대 차트 (지역별 비교)
- 우측 상단: "위탁병원이용인원현황" 버튼

### 챠트2 (c_1.html)
- 햄버거 메뉴 사이드바 (기본 열림)
- 5개 인터랙티브 Plotly 차트
  - 월별 평균이용 인원추이
  - 년도년월 인원 상관관계
  - 광역지자체별 년도별 이용인원
  - 지역별 이용인원 피벗 차트
  - 년도별 이용인원 비율
- 반응형 레이아웃
- 우측 상단: "위탁병원증감현황" + "홈으로" 버튼

## 기여

프로젝트에 기여하고 싶으시다면:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 라이센스

MIT License

## 연락처

**프로젝트 저장소**: [github.com/danatec1/bohun1](https://github.com/danatec1/bohun1)

## 감사의 글

- **Chart.js**: 아름다운 차트 라이브러리
- **Plotly**: 강력한 인터랙티브 차트
- **Flask**: 간결한 웹 프레임워크
- **Leaflet.js**: 오픈소스 지도 라이브러리

---

**보훈 병원 관리 시스템 개발팀**  
*Last Updated: 2025-10-23 v2.1*