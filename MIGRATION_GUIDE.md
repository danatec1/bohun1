# React Chart 앱을 Flask로 마이그레이션 가이드

## 📁 파일 이동 계획

### 1. 정적 파일 이동
```
Chart/public/*.html          → app/static/charts/*.html
Chart/data/*.json             → app/static/data/*.json
```
**참고**: 이미지 파일(1.JPG, 2.JPG)은 사용하지 않으므로 복사하지 않습니다.

### 2. 필요한 폴더 구조
```
c:\bohun1\
├── app/
│   ├── static/
│   │   ├── charts/          # 새로 생성
│   │   │   ├── chart3_scatter_matrix.html
│   │   │   ├── chart4_yearly_area.html
│   │   │   ├── chart5_regional_bar.html
│   │   │   ├── chart6_pivot_bar.html
│   │   │   └── chart7_pie_subplots.html
│   │   └── data/            # 새로 생성
│   │       └── chart_sync_info.json
│   └── templates/
│       └── charts.html      # 새로운 차트 페이지
└── Chart/                   # 기존 React 앱 (유지 또는 삭제)
```
**참고**: 이미지 폴더는 생성하지 않습니다 (차트 0, 1 미사용).

## 🔧 코드 수정 사항

### 1. Flask 라우트 추가 (app/routes/__init__.py)

```python
# 차트 페이지 라우트 추가
@main_bp.route('/charts')
def charts():
    return render_template('charts.html')

# 정적 파일 서빙을 위한 라우트 (선택사항)
from flask import send_from_directory

@main_bp.route('/charts/<path:filename>')
def serve_chart(filename):
    return send_from_directory(
        os.path.join(current_app.root_path, 'static', 'charts'),
        filename
    )

@main_bp.route('/data/<path:filename>')
def serve_data(filename):
    return send_from_directory(
        os.path.join(current_app.root_path, 'static', 'data'),
        filename
    )
```

### 2. 템플릿 생성 (app/templates/charts.html)

React App.tsx의 구조를 Flask Jinja2로 변환:

```html
{% extends "base.html" %}

{% block title %}데이터 분석 대시보드{% endblock %}

{% block content %}
<div class="min-h-screen bg-gray-100">
    <div class="flex h-screen relative">
        <!-- Sidebar -->
        <div id="sidebar" class="w-64 h-screen flex flex-col overflow-y-auto" 
             style="background-color: #212529;">
            <!-- 헤더 -->
            <div class="flex-shrink-0 p-6 pb-4 border-b" 
                 style="background-color: #212529; border-color: #343a40;">
                <h1 class="text-xl font-bold text-white">대시보드</h1>
                <p class="mt-1 text-sm" style="color: #adb5bd;">
                    차트를 선택하여 자세히 확인하세요
                </p>
            </div>

            <!-- 메뉴 -->
            <nav class="flex flex-col flex-1 p-0 overflow-y-auto">
                <a href="#" class="menu-item active" data-chart="2">
                    <i class="bi bi-bar-chart-fill"></i>
                    전국 위탁병원 연도, 월, 연월, 인원 상관관계 분석
                </a>
                <a href="#" class="menu-item" data-chart="3">
                    <i class="bi bi-graph-up-arrow"></i>
                    전국 위탁병원 연도별 월별 이용인원 추이
                </a>
                <a href="#" class="menu-item" data-chart="4">
                    <i class="bi bi-geo-alt-fill"></i>
                    광역지자체별 연도별 위탁병원 이용인원
                </a>
                <a href="#" class="menu-item" data-chart="5">
                    <i class="bi bi-bar-chart-fill"></i>
                    광역지자체별 연도별 위탁병원 이용 인원
                </a>
                <a href="#" class="menu-item" data-chart="6">
                    <i class="bi bi-bar-chart-fill"></i>
                    광역지자체별 이용 인원
                </a>
                <a href="#" class="menu-item" data-chart="7">
                    <i class="bi bi-pie-chart-fill"></i>
                    연도별 광역지자체별 위탁병원 이용 인원 비율
                </a>
            </nav>
        </div>

        <!-- 메인 컨텐츠 -->
        <div class="flex-1 flex flex-col overflow-hidden p-8">
            <!-- 차트 2: Plotly HTML (산점도 행렬) -->
            <div class="chart-section active" id="chart-2">
                <iframe src="{{ url_for('static', filename='charts/chart3_scatter_matrix.html') }}"
                        width="100%" height="850px" style="border: none; border-radius: 8px;"></iframe>
            </div>

            <!-- 차트 3: Plotly HTML (연도별 월별 추이) -->
            <div class="chart-section" id="chart-3">
                <iframe src="{{ url_for('static', filename='charts/chart4_yearly_area.html') }}"
                        width="100%" height="650px" style="border: none; border-radius: 8px;"></iframe>
            </div>

            <!-- 차트 4: 플레이스홀더 -->
            <div class="chart-section" id="chart-4">
                <div class="text-center p-8">
                    <i class="bi bi-geo-alt-fill" style="font-size: 4rem; color: #adb5bd;"></i>
                    <p class="text-lg text-muted-foreground mt-4">지역별 차트 준비 중입니다</p>
                </div>
            </div>

            <!-- 차트 5: Plotly HTML (광역지자체별 그룹 막대) -->
            <div class="chart-section" id="chart-5">
                <iframe src="{{ url_for('static', filename='charts/chart5_regional_bar.html') }}"
                        width="100%" height="650px" style="border: none; border-radius: 8px;"></iframe>
            </div>

            <!-- 차트 6: Plotly HTML (Pivot 막대) -->
            <div class="chart-section" id="chart-6">
                <iframe src="{{ url_for('static', filename='charts/chart6_pivot_bar.html') }}"
                        width="100%" height="650px" style="border: none; border-radius: 8px;"></iframe>
            </div>

            <!-- 차트 7: Plotly HTML (파이차트 서브플롯) -->
            <div class="chart-section" id="chart-7">
                <iframe src="{{ url_for('static', filename='charts/chart7_pie_subplots.html') }}"
                        width="100%" height="1050px" style="border: none; border-radius: 8px;"></iframe>
            </div>
        </div>
    </div>
</div>

<script>
// 메뉴 클릭 이벤트
document.querySelectorAll('.menu-item').forEach(item => {
    item.addEventListener('click', function(e) {
        e.preventDefault();
        
        // 활성 메뉴 변경
        document.querySelectorAll('.menu-item').forEach(m => 
            m.classList.remove('active'));
        this.classList.add('active');
        
        // 차트 섹션 변경
        const chartId = this.getAttribute('data-chart');
        document.querySelectorAll('.chart-section').forEach(s => 
            s.classList.remove('active'));
        document.getElementById('chart-' + chartId).classList.add('active');
    });
});

// MySQL 동기화 정보 로드
fetch("{{ url_for('static', filename='data/chart_sync_info.json') }}")
    .then(res => res.json())
    .then(data => {
        console.log('MySQL Sync Info:', data);
        // 동기화 정보 표시 로직
    });
</script>

<style>
.chart-section {
    display: none;
}
.chart-section.active {
    display: block;
}
.menu-item {
    padding: 1rem 1.25rem;
    color: #dee2e6;
    transition: all 0.2s;
    border-left: 4px solid transparent;
}
.menu-item.active {
    background-color: #0d6efd;
    color: #ffffff;
    border-left-color: #0d6efd;
}
.menu-item:hover {
    background-color: #343a40;
    color: #ffffff;
}
</style>
{% endblock %}
```

## 📝 마이그레이션 단계별 실행

### Step 1: 폴더 생성
```powershell
# PowerShell 명령어
New-Item -ItemType Directory -Path "c:\bohun1\app\static\charts"
New-Item -ItemType Directory -Path "c:\bohun1\app\static\data"
```

### Step 2: 파일 복사
```powershell
# Plotly Chart HTML 파일들 복사 (chart3~chart7만)
Copy-Item "c:\bohun1\Chart\public\chart3_scatter_matrix.html" -Destination "c:\bohun1\app\static\charts\"
Copy-Item "c:\bohun1\Chart\public\chart4_yearly_area.html" -Destination "c:\bohun1\app\static\charts\"
Copy-Item "c:\bohun1\Chart\public\chart5_regional_bar.html" -Destination "c:\bohun1\app\static\charts\"
Copy-Item "c:\bohun1\Chart\public\chart6_pivot_bar.html" -Destination "c:\bohun1\app\static\charts\"
Copy-Item "c:\bohun1\Chart\public\chart7_pie_subplots.html" -Destination "c:\bohun1\app\static\charts\"

# JSON 파일 복사
Copy-Item "c:\bohun1\Chart\data\chart_sync_info.json" -Destination "c:\bohun1\app\static\data\"
```

**참고**: 
- 차트 0, 1은 이미지 기반이므로 제외
- chart3~chart7만 Plotly HTML 파일로 사용

### Step 3: Flask 라우트 추가
`app/routes/__init__.py` 파일에 차트 라우트 추가

### Step 4: 템플릿 생성
`app/templates/charts.html` 생성

### Step 5: 테스트
```
http://localhost/charts
```

## ⚠️ 주의사항

### 1. **Plotly HTML 파일 크기**
- Plotly HTML 파일은 크기가 클 수 있음 (1-5MB)
- 느린 로딩 시 로딩 스피너 추가 고려

### 2. **iframe 보안 정책**
- 동일 출처 정책(Same-Origin Policy) 준수
- Flask static 폴더에서 서빙하면 문제없음

### 3. **MySQL 동기화**
- `chart_sync_info.json` 파일 업데이트 필요
- `generate_static_charts.py` 스크립트의 저장 경로 수정:
  ```python
  # 기존
  json_path = 'Chart/data/chart_sync_info.json'
  
  # 변경
  json_path = 'app/static/data/chart_sync_info.json'
  ```

## 🎯 장점

1. ✅ **단일 서버**: Flask만 실행 (포트 80)
2. ✅ **통합 관리**: 병원 CRUD + 차트를 하나의 앱에서
3. ✅ **배포 간소화**: React 빌드 과정 불필요
4. ✅ **라우팅 통합**: `/`, `/hospitals`, `/charts` 모두 Flask에서

## ❌ 단점

1. ❌ **반응성**: React의 인터랙티브한 UI 손실
2. ❌ **성능**: Vite 개발 서버의 HMR 기능 없음
3. ❌ **컴포넌트**: shadcn/ui, Tailwind 설정 다시 필요
4. ❌ **유지보수**: JavaScript로 DOM 조작 필요

## 🔄 대안: 하이브리드 방식

React 앱을 빌드하여 Flask static에 서빙:

```powershell
# Chart 앱 빌드
cd c:\bohun1\Chart
npm run build

# 빌드 파일을 Flask static에 복사
Copy-Item "dist/*" -Destination "c:\bohun1\app\static\chart-app\" -Recurse
```

Flask 라우트:
```python
@main_bp.route('/chart-app')
def chart_app():
    return send_from_directory('static/chart-app', 'index.html')
```

이 방법은 React 앱의 모든 기능을 유지하면서 Flask에서 서빙할 수 있습니다.
