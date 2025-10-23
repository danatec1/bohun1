"""
위탁병원현황_연도별현황 테이블 데이터로 정적 차트 이미지 생성
Chart 1: 광역지자체별 연도별 위탁병원 현황 (1.jpg)
Chart 2: 전국 위탁병원 연도별 전체 합계 추세 (2.jpg)

MySQL 데이터와 동기화되어 자동으로 업데이트됩니다.
"""

import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
from pathlib import Path
from datetime import datetime
import json
import os

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# MySQL 연결 설정
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'zzaaqq',
    'database': 'testdb',
    'charset': 'utf8mb4'
}

def load_yearly_statistics():
    """위탁병원현황_연도별현황 테이블 데이터 로드"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        query = "SELECT * FROM 위탁병원현황_연도별현황"
        df = pd.read_sql(query, connection)
        connection.close()
        print(f"✅ 연도별 통계 데이터 로드 완료: {len(df)} 행")
        return df
    except Exception as e:
        print(f"❌ 데이터 로드 실패: {e}")
        return None

def create_chart1_image(df):
    """
    Chart 1: 광역지자체별 연도별 위탁병원 현황 (grouped bar chart)
    """
    print("\n📊 Chart 1: 광역지자체별 연도별 위탁병원 현황 생성 중...")
    
    # 데이터 재구조화 (wide to long format)
    data_list = []
    for _, row in df.iterrows():
        region = row['광역지자체']
        for year_col in ['2022년12월', '2023년12월', '2024년12월']:
            data_list.append({
                '광역지자체': region,
                '연도': year_col.replace('년12월', ''),
                '병원수': row[year_col]
            })
    
    df_long = pd.DataFrame(data_list)
    
    # 연도별로 피벗
    df_pivot = df_long.pivot(index='광역지자체', columns='연도', values='병원수')
    
    # 그래프 크기 설정 (다른 차트와 동일하게)
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # 막대 그래프 그리기
    x = np.arange(len(df_pivot.index))
    width = 0.25
    
    colors = ['#4e79a7', '#f28e2c', '#e15759']  # 파란색, 주황색, 빨간색
    years = ['2022', '2023', '2024']
    
    for i, year in enumerate(years):
        offset = width * (i - 1)
        bars = ax.bar(x + offset, df_pivot[year], width, 
                      label=f'{year}년', color=colors[i], alpha=0.8)
        
        # 데이터 레이블 추가
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height):,}',
                   ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # 그래프 꾸미기
    ax.set_xlabel('광역지자체', fontsize=12, fontweight='bold')
    ax.set_ylabel('위탁병원 수', fontsize=12, fontweight='bold')
    ax.set_title('광역지자체별 연도별 위탁병원 현황 (2022~2024)', 
                fontsize=16, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(df_pivot.index, rotation=45, ha='right', fontsize=10)
    ax.legend(fontsize=10, loc='upper right')
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.tick_params(axis='y', labelsize=10)
    
    # 레이아웃 조정
    plt.tight_layout()
    
    # 저장
    output_path = Path('c:/bohun1/Chart/data/images/1.JPG')
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"✅ Chart 1 저장 완료: {output_path}")

def create_chart2_image(df):
    """
    Chart 2: 전국 위탁병원 연도별 전체 합계 추세 (pie chart)
    """
    print("\n� Chart 2: 전국 위탁병원 연도별 비율 파이 차트 생성 중...")
    
    # 연도별 합계 계산
    yearly_totals = {
        '2022년': df['2022년12월'].sum(),
        '2023년': df['2023년12월'].sum(),
        '2024년': df['2024년12월'].sum()
    }
    
    labels = list(yearly_totals.keys())
    sizes = list(yearly_totals.values())
    total = sum(sizes)
    
    # 색상 설정
    colors = ['#ff9999', '#66b3ff', '#99ff99']
    explode = (0.05, 0.05, 0.05)  # 모든 조각 약간 분리
    
    # 그래프 크기 설정 (다른 차트와 동일하게)
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # 파이 차트 그리기
    wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels,
                                        colors=colors, autopct='%1.1f%%',
                                        shadow=True, startangle=90,
                                        textprops={'fontsize': 11, 'fontweight': 'bold'})
    
    # 퍼센트 텍스트 스타일 설정
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(13)
        autotext.set_fontweight('bold')
    
    # 레이블 텍스트 스타일 설정
    for text in texts:
        text.set_fontsize(13)
        text.set_fontweight('bold')
    
    # 범례 추가 (개수와 비율 표시)
    legend_labels = []
    for label, size in zip(labels, sizes):
        percentage = (size / total) * 100
        legend_labels.append(f'{label}: {int(size):,}개 ({percentage:.1f}%)')
    
    ax.legend(legend_labels, loc='upper left', bbox_to_anchor=(1, 1),
             fontsize=10, frameon=True, shadow=True)
    
    # 제목
    ax.set_title('전국 위탁병원 연도별 비율 (2022~2024)', 
                fontsize=16, fontweight='bold', pad=15)
    
    # 총합 정보 추가
    plt.figtext(0.5, 0.02, f'총 위탁병원 수 (3개년 합계): {total:,}개', 
               ha='center', fontsize=11, fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.3))
    
    # 증감 정보 추가
    change_2022_2023 = sizes[1] - sizes[0]
    change_2023_2024 = sizes[2] - sizes[1]
    change_rate_2022_2023 = (change_2022_2023 / sizes[0]) * 100
    change_rate_2023_2024 = (change_2023_2024 / sizes[1]) * 100
    
    info_text = f'📊 증감 추이:\n'
    info_text += f'2022→2023: {change_2022_2023:+,}개 ({change_rate_2022_2023:+.1f}%)\n'
    info_text += f'2023→2024: {change_2023_2024:+,}개 ({change_rate_2023_2024:+.1f}%)'
    
    plt.figtext(0.5, 0.92, info_text, ha='center', fontsize=9,
               bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.5))
    
    # Equal aspect ratio ensures that pie is drawn as a circle
    ax.axis('equal')
    
    # 레이아웃 조정
    plt.tight_layout()
    
    # 저장
    output_path = Path('c:/bohun1/Chart/data/images/2.JPG')
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"✅ Chart 2 저장 완료: {output_path}")

def save_sync_info(df):
    """차트 동기화 정보 저장"""
    sync_info = {
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_regions': len(df),
        'data_years': ['2022년12월', '2023년12월', '2024년12월'],
        'yearly_totals': {
            '2022': int(df['2022년12월'].sum()),
            '2023': int(df['2023년12월'].sum()),
            '2024': int(df['2024년12월'].sum())
        }
    }
    
    sync_file = Path('c:/bohun1/Chart/data/chart_sync_info.json')
    with open(sync_file, 'w', encoding='utf-8') as f:
        json.dump(sync_info, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 동기화 정보 저장: {sync_file}")
    return sync_info


def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("📊 MySQL 동기화 정적 차트 이미지 생성 시작...")
    print("=" * 60)
    
    # 데이터 로드
    df = load_yearly_statistics()
    if df is None:
        print("❌ 데이터 로드 실패. 프로그램 종료.")
        return
    
    print(f"\n📊 MySQL 데이터 정보:")
    print(f"  - 데이터베이스: testdb")
    print(f"  - 테이블: 위탁병원현황_연도별현황")
    print(f"  - 총 행 수: {len(df)}개 광역지자체")
    print(f"  - 컬럼: {list(df.columns)}")
    print(f"\n📈 연도별 전체 합계:")
    print(f"  - 2022년 12월: {df['2022년12월'].sum():,}개")
    print(f"  - 2023년 12월: {df['2023년12월'].sum():,}개")
    print(f"  - 2024년 12월: {df['2024년12월'].sum():,}개")
    
    # Chart 1 생성
    create_chart1_image(df)
    
    # Chart 2 생성
    create_chart2_image(df)
    
    # 동기화 정보 저장
    sync_info = save_sync_info(df)
    
    print("\n" + "=" * 60)
    print("✅ MySQL 동기화 완료! 모든 차트 이미지 생성 완료!")
    print("=" * 60)
    print(f"\n📌 생성된 파일:")
    print(f"  1. c:/bohun1/Chart/data/images/1.JPG - 광역지자체별 연도별 위탁병원 현황")
    print(f"  2. c:/bohun1/Chart/data/images/2.JPG - 전국 위탁병원 연도별 전체 합계 추세")
    print(f"  3. c:/bohun1/Chart/data/chart_sync_info.json - 동기화 정보")
    print(f"\n⏰ 마지막 동기화: {sync_info['last_updated']}")
    print(f"💡 MySQL 데이터가 업데이트되면 이 스크립트를 다시 실행하세요!")


if __name__ == "__main__":
    main()
