#!/usr/bin/env python3
"""
Flask 애플리케이션의 모든 라우트 확인 스크립트
"""

from app import create_app

def list_routes():
    """현재 등록된 모든 라우트 출력"""
    app = create_app()
    
    print("=" * 60)
    print("🌐 Flask 애플리케이션 등록된 라우트 목록")
    print("=" * 60)
    
    routes = []
    for rule in app.url_map.iter_rules():
        methods = ', '.join(sorted(rule.methods - {'HEAD', 'OPTIONS'}))
        routes.append((rule.rule, methods, rule.endpoint))
    
    # 정렬
    routes.sort()
    
    print(f"{'경로':<40} {'메서드':<15} {'엔드포인트'}")
    print("-" * 80)
    
    for route, methods, endpoint in routes:
        print(f"{route:<40} {methods:<15} {endpoint}")
    
    print("-" * 80)
    print(f"총 {len(routes)}개의 라우트가 등록되어 있습니다.")
    print()
    print("🚀 접속 가능한 주요 페이지:")
    print("   메인 페이지: http://127.0.0.1:5001/")
    print("   병원 목록: http://127.0.0.1:5001/hospitals")
    print("   Folium 지도: http://127.0.0.1:5001/folium-map")
    print("   지도 생성 API: http://127.0.0.1:5001/api/map/folium")
    print("   Excel 내보내기: http://127.0.0.1:5001/api/export/excel")
    print("=" * 60)

if __name__ == "__main__":
    list_routes()
