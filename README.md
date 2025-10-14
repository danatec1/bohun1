# 보훈 병원 관리 시스템

MVC 패턴을 기반으로 한 병원 정보 관리 웹 애플리케이션입니다.

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
│   │   └── hospital_repository.py
│   ├── services/          # 비즈니스 로직 계층
│   │   └── hospital_service.py
│   ├── templates/         # 뷰 템플릿 (V)
│   │   ├── base.html
│   │   ├── index.html
│   │   └── hospitals.html
│   ├── routes/            # 라우팅 설정
│   │   └── __init__.py
│   ├── utils/             # 유틸리티
│   └── __init__.py        # 애플리케이션 팩토리
├── config/                # 설정 파일
│   └── __init__.py
├── public/                # 정적 파일
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── main.js
│   │   └── hospitals.js
│   └── images/
├── tests/                 # 테스트 파일
└── run.py                 # 애플리케이션 실행 파일
```

## 주요 기능

- **병원 관리**: CRUD 기능을 통한 병원 정보 관리
- **지도 시각화**: Leaflet.js를 이용한 병원 위치 표시
- **검색 기능**: 병원명, 위치 기반 검색
- **반응형 디자인**: 모바일 친화적 UI/UX

## 기술 스택

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Database**: SQLite
- **Map**: Leaflet.js
- **Architecture**: MVC Pattern

## 설치 및 실행

### 1. 가상환경 생성 및 활성화

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 애플리케이션 실행

```bash
python run.py
```

또는

```bash
flask run
```

### 4. 브라우저에서 접속

```
http://localhost:5000
```

## API 엔드포인트

### 병원 관리

- `GET /api/hospitals` - 모든 병원 목록 조회
- `POST /api/hospitals` - 새 병원 생성
- `GET /api/hospitals/<id>` - 특정 병원 조회
- `PUT /api/hospitals/<id>` - 병원 정보 수정
- `DELETE /api/hospitals/<id>` - 병원 삭제
- `GET /api/hospitals/search` - 병원 검색

## 환경 변수

```bash
FLASK_ENV=development          # 환경 설정 (development/production/testing)
SECRET_KEY=your-secret-key    # Flask 보안 키
DATABASE_PATH=/path/to/db     # 데이터베이스 경로
PORT=5000                     # 서버 포트
```

## MVC 아키텍처

### Model (모델)
- `hospital.py`: 병원 데이터 모델
- `hospital_repository.py`: 데이터베이스 접근 계층
- `hospital_service.py`: 비즈니스 로직 계층

### View (뷰)
- `templates/`: HTML 템플릿
- `public/`: CSS, JavaScript, 이미지 등 정적 파일

### Controller (컨트롤러)
- `hospital_controller.py`: 병원 관련 HTTP 요청 처리
- `main_controller.py`: 메인 페이지 요청 처리
- `routes/__init__.py`: URL 라우팅 설정

## 라이센스

MIT License

## 개발자

보훈 병원 관리 시스템 개발팀