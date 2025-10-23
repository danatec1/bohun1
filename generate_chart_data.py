#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chart 데이터 생성기
CSV 파일을 분석하여 7개 차트용 JSON 데이터 생성
"""

import pandas as pd
import json
from pathlib import Path
import numpy as np

def load_csv_data():
    """CSV 파일 로드"""
    csv_path = Path(__file__).parent / 'Chart' / 'data' / '지역별위탁병원이용인원2.csv'
    return pd.read_csv(csv_path)

def create_chart_data():
    """Chart 3~6용 CSV 데이터 생성 (Chart 1,2는 이미지 사용)"""
    df = load_csv_data()
    
    # 데이터 전처리
    df['인원'] = pd.to_numeric(df['인원'], errors='coerce').fillna(0)
    df['연도'] = pd.to_numeric(df['연도'], errors='coerce')
    df['월'] = pd.to_numeric(df['월'], errors='coerce')
    
    chart_data = {}
    
    # 1. 보훈병원 사용 인원현황1 (이미지 사용)
    chart_data['chart1'] = {
        'title': '보훈병원 사용 인원현황1',
        'type': 'image',
        'image_path': '/data/images/1.JPG',
        'description': '보훈병원 사용 인원현황 분석 차트'
    }
    
    # 2. 보훈병원 사용인원현황2 (이미지 사용)
    chart_data['chart2'] = {
        'title': '보훈병원 사용인원현황2',
        'type': 'image', 
        'image_path': '/data/images/2.JPG',
        'description': '보훈병원 사용인원 상세 현황 차트'
    }
    
    # 3. 전국위탁병원 월별 평균이용 인원추이 (CSV 데이터 차트)
    top_regions = df.groupby('광역지자체')['인원'].sum().nlargest(5).index
    chart3_filtered = df[df['광역지자체'].isin(top_regions)]
    chart3_data = chart3_filtered.groupby('광역지자체')['인원'].sum()
    total = chart3_data.sum()
    chart_data['chart3'] = {
        'title': '전국위탁병원 월별 평균이용 인원추이',
        'type': 'pie',
        'image_path': '/data/images/3.JPG',
        'data': [
            {
                'name': region, 
                'value': int(count), 
                'percentage': round((count/total)*100, 1),
                'fill': f"hsl({i * 72}, 70%, 50%)"
            }
            for i, (region, count) in enumerate(chart3_data.items())
        ]
    }
    
    # 4. 전국위탁병원 년도,년월상관관계분석 (CSV 데이터 차트)
    chart4_data = df.groupby('연도')['인원'].agg(['sum', 'count']).reset_index()
    chart4_data.columns = ['연도', '총인원', '건수']
    chart_data['chart4'] = {
        'title': '전국위탁병원 년도,년월상관관계분석',
        'type': 'area',
        'image_path': '/data/images/4.JPG',
        'data': [
            {
                'year': f"{int(row['연도'])}년", 
                'total': int(row['총인원']), 
                'count': int(row['건수'])
            }
            for _, row in chart4_data.iterrows()
        ]
    }
    
    # 5. 광역지자체별 연도별 위탁병원 이용인원 프로그램 결과 (CSV 데이터)
    chart5_data = df.groupby(['광역지자체', '연도'])['인원'].sum().reset_index()
    top5_regions = df.groupby('광역지자체')['인원'].sum().nlargest(5).index
    chart5_filtered = chart5_data[chart5_data['광역지자체'].isin(top5_regions)]
    
    radial_data = []
    colors = ['#8884d8', '#82ca9d', '#ffc658', '#ff7c7c', '#8dd1e1']
    for i, region in enumerate(top5_regions):
        region_data = chart5_filtered[chart5_filtered['광역지자체'] == region]
        region_total = region_data['인원'].sum()
        radial_data.append({
            'name': region,
            'value': int(region_total),
            'fill': colors[i % len(colors)]
        })
    
    chart_data['chart5'] = {
        'title': '광역지자체별 연도별 위탁병원 이용인원 프로그램 결과',
        'type': 'radialBar',
        'image_path': '/data/images/5.JPG',
        'data': radial_data
    }
    
    # 6. 연도별 광역지자체 코드별 위탁병원이용 비율 파이차트 (CSV 데이터)
    chart6_monthly = df.groupby(['연도', '월'])['인원'].sum().reset_index()
    chart6_monthly['date'] = chart6_monthly.apply(
        lambda x: f"{int(x['연도'])}-{int(x['월']):02d}", axis=1
    )
    chart_data['chart6'] = {
        'title': '연도별 광역지자체 코드별 위탁병원이용 비율 파이차트 프로그램결과',
        'type': 'line',
        'image_path': '/data/images/6.JPG',
        'data': [
            {
                'date': row['date'], 
                'users': int(row['인원']),
                'year': int(row['연도']),
                'month': int(row['월'])
            }
            for _, row in chart6_monthly.head(24).iterrows()  # 최근 24개월
        ]
    }
    
    # 7. 공백 (통계 요약)
    total_users = df['인원'].sum()
    total_regions = df['광역지자체'].nunique()
    avg_monthly = df.groupby(['연도', '월'])['인원'].sum().mean()
    
    chart_data['chart7'] = {
        'title': '공백',
        'type': 'summary',
        'data': {
            'total_users': int(total_users),
            'total_regions': int(total_regions),
            'avg_monthly': int(avg_monthly),
            'data_period': f"{df['연도'].min()}-{df['연도'].max()}"
        }
    }
    
    return chart_data

def main():
    """메인 실행 함수"""
    try:
        print("📊 CSV 데이터 분석 시작...")
        chart_data = create_chart_data()
        
        # JSON 파일로 저장
        output_path = Path(__file__).parent / 'Chart' / 'data' / 'chartData.json'
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(chart_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 차트 데이터 생성 완료: {output_path}")
        print(f"📈 총 {len(chart_data)}개 차트 데이터 생성")
        
        # 데이터 미리보기
        for key, data in chart_data.items():
            print(f"  - {key}: {data['title']} ({data['type']})")
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
