#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Folium 지도 생성 테스트 스크립트
"""

import requests
import json

def test_folium_map():
    """Folium 지도 생성 테스트"""
    
    base_url = "http://127.0.0.1:5001"
    
    print("🗺️ Folium 지도 생성 테스트")
    print("=" * 50)
    
    # 1. Folium 지도 생성 테스트
    print("\n1. 전체 병원 지도 생성...")
    try:
        response = requests.post(f"{base_url}/api/map/folium")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"✅ 성공: {result.get('message')}")
                print(f"📁 파일: {result.get('filename')}")
                print(f"📍 경로: {result.get('filepath')}")
            else:
                print(f"❌ 실패: {result.get('error')}")
        else:
            print(f"❌ HTTP 오류: {response.status_code}")
            print(f"응답: {response.text}")
    except Exception as e:
        print(f"❌ 연결 오류: {e}")
    
    # 2. Excel 내보내기 테스트
    print("\n2. Excel 파일 생성...")
    try:
        response = requests.post(f"{base_url}/api/export/excel")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"✅ 성공: {result.get('message')}")
                print(f"📁 파일: {result.get('filename')}")
                print(f"📍 경로: {result.get('filepath')}")
            else:
                print(f"❌ 실패: {result.get('error')}")
        else:
            print(f"❌ HTTP 오류: {response.status_code}")
            print(f"응답: {response.text}")
    except Exception as e:
        print(f"❌ 연결 오류: {e}")
    
    # 3. 병원 데이터 확인
    print("\n3. 병원 데이터 확인...")
    try:
        response = requests.get(f"{base_url}/api/hospitals")
        
        if response.status_code == 200:
            hospitals = response.json()
            print(f"✅ 병원 데이터 로드 성공")
            print(f"📊 총 병원 수: {len(hospitals)}개")
            
            if hospitals:
                sample = hospitals[0]
                print(f"📋 샘플 데이터:")
                print(f"   - 이름: {sample.get('name')}")
                print(f"   - 주소: {sample.get('address')}")
                print(f"   - 위도: {sample.get('latitude')}")
                print(f"   - 경도: {sample.get('longitude')}")
        else:
            print(f"❌ HTTP 오류: {response.status_code}")
    except Exception as e:
        print(f"❌ 연결 오류: {e}")

if __name__ == "__main__":
    test_folium_map()
