#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plotly 차트 생성기 - 지역별 위탁병원 이용인원 데이터 시각화
testdb.지역별위탁병원이용인원2 테이블에서 데이터를 가져와 인터랙티브 차트 생성
"""

import pymysql
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
import json

# MySQL 연결 설정
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'zzaaqq',
    'database': 'testdb',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def load_data_from_mysql():
    """MySQL에서 지역별위탁병원이용인원2 데이터 로드"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        query = "SELECT * FROM 지역별위탁병원이용인원2"
        
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
        
        connection.close()
        
        # DataFrame 생성
        df = pd.DataFrame(results)
        print(f"✅ 데이터 로드 완료: {len(df)} 행")
        return df
        
    except Exception as e:
        print(f"❌ 데이터 로드 실패: {e}")
        return None


def load_yearly_statistics():
    """MySQL에서 위탁병원현황_연도별현황 데이터 로드 (Chart 1, 2용)"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        query = "SELECT * FROM 위탁병원현황_연도별현황"
        
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
        
        connection.close()
        
        # DataFrame 생성
        df = pd.DataFrame(results)
        print(f"✅ 연도별 통계 데이터 로드 완료: {len(df)} 행")
        return df
        
    except Exception as e:
        print(f"❌ 연도별 통계 데이터 로드 실패: {e}")
        return None


def create_chart1_regional_yearly_bar(df_yearly):
    """Chart 1: 광역지자체별 연도별 막대 차트 (위탁병원현황_연도별현황 사용)"""
    # 데이터 재구성
    data_list = []
    for _, row in df_yearly.iterrows():
        data_list.append({'광역지자체': row['광역지자체'], '연도': '2022년12월', '인원': row['2022년12월']})
        data_list.append({'광역지자체': row['광역지자체'], '연도': '2023년12월', '인원': row['2023년12월']})
        data_list.append({'광역지자체': row['광역지자체'], '연도': '2024년12월', '인원': row['2024년12월']})
    
    chart_df = pd.DataFrame(data_list)
    
    # 막대 차트 생성
    fig = px.bar(
        chart_df,
        x='광역지자체',
        y='인원',
        color='연도',
        title='광역지자체별 연도별 위탁병원 현황 (2022~2024년 12월 기준)',
        labels={'인원': '병원 수 (개)', '광역지자체': '광역지자체'},
        barmode='group',
        color_discrete_sequence=['#1f77b4', '#ff7f0e', '#2ca02c']
    )
    
    fig.update_layout(
        xaxis_title="광역지자체",
        yaxis_title="병원 수 (개)",
        xaxis=dict(tickangle=-45),
        yaxis=dict(tickformat=','),
        height=600,
        width=1100,
        title_x=0.5,
        legend_title="연도"
    )
    
    return fig


def create_chart2_yearly_trend_line(df_yearly):
    """Chart 2: 연도별 전체 합계 추세 라인 차트 (위탁병원현황_연도별현황 사용)"""
    # 연도별 합계 계산
    trend_data = pd.DataFrame({
        '연도': ['2022년12월', '2023년12월', '2024년12월'],
        '전체병원수': [
            df_yearly['2022년12월'].sum(),
            df_yearly['2023년12월'].sum(),
            df_yearly['2024년12월'].sum()
        ]
    })
    
    # 라인 차트 생성
    fig = px.line(
        trend_data,
        x='연도',
        y='전체병원수',
        title='연도별 전국 위탁병원 전체 현황 추이 (2022~2024년 12월 기준)',
        labels={'전체병원수': '전체 병원 수 (개)', '연도': '연도'},
        markers=True
    )
    
    fig.update_traces(
        line=dict(width=4, color='#1f77b4'),
        marker=dict(size=12, color='#ff7f0e', line=dict(width=2, color='white'))
    )
    
    fig.update_layout(
        xaxis_title="연도",
        yaxis_title="전체 병원 수 (개)",
        yaxis=dict(tickformat=','),
        height=600,
        width=1100,
        hovermode='x unified',
        title_x=0.5
    )
    
    return fig


def create_scatter_matrix_chart(df):
    """산점도 행렬 차트 생성 (사용자 제공 코드)"""
    # 숫자 컬럼만 선택 (fhospital_data → df)
    num_df = df[['연도', '월', '연월', '광역지자체코드', '인원']].copy()
    
    # 데이터 타입 변환
    num_df['연도'] = pd.to_numeric(num_df['연도'], errors='coerce')
    num_df['월'] = pd.to_numeric(num_df['월'], errors='coerce')
    num_df['연월'] = pd.to_numeric(num_df['연월'], errors='coerce')
    num_df['광역지자체코드'] = pd.to_numeric(num_df['광역지자체코드'], errors='coerce')
    num_df['인원'] = pd.to_numeric(num_df['인원'], errors='coerce')
    
    # NaN 제거
    num_df = num_df.dropna()
    
    # 산점도 행렬 생성 (사용자 코드 그대로)
    fig = px.scatter_matrix(
        num_df,
        dimensions=['연도', '월', '연월', '광역지자체코드', '인원'],  # 표시할 변수들
        title='전국 위탁병원 연도, 월, 연월, 인원 상관관계 분석',
        color='인원',
        height=800,
        width=800
    )
    
    fig.update_traces(diagonal_visible=False)
    fig.update_layout(title_x=0.5)
    
    return fig

def create_better_correlation_chart(df):
    """개선된 상관관계 히트맵 차트"""
    # 숫자 컬럼만 선택
    num_df = df[['연도', '월', '연월', '광역지자체코드', '인원']].copy()
    
    # 데이터 타입 변환
    for col in num_df.columns:
        num_df[col] = pd.to_numeric(num_df[col], errors='coerce')
    
    num_df = num_df.dropna()
    
    # 상관계수 계산
    correlation_matrix = num_df.corr()
    
    # 히트맵 생성
    fig = go.Figure(data=go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.columns,
        colorscale='RdBu',
        zmid=0,
        text=correlation_matrix.values.round(2),
        texttemplate='%{text}',
        textfont={"size": 12},
        colorbar=dict(title="상관계수")
    ))
    
    fig.update_layout(
        title='전국 위탁병원 변수 간 상관관계 히트맵',
        title_x=0.5,
        width=800,
        height=800,
        xaxis=dict(title=''),
        yaxis=dict(title='')
    )
    
    return fig

def create_regional_trend_chart(df):
    """지역별 인원 추이 차트 (더 실용적)"""
    # 데이터 전처리
    df['인원'] = pd.to_numeric(df['인원'], errors='coerce')
    df['연도'] = pd.to_numeric(df['연도'], errors='coerce')
    df['월'] = pd.to_numeric(df['월'], errors='coerce')
    
    # 날짜 생성
    df['날짜'] = pd.to_datetime(df['연도'].astype(str) + '-' + df['월'].astype(str).str.zfill(2) + '-01')
    
    # 상위 10개 지역 선택
    top_regions = df.groupby('광역지자체')['인원'].sum().nlargest(10).index
    df_filtered = df[df['광역지자체'].isin(top_regions)]
    
    # 시계열 차트 생성
    fig = px.line(
        df_filtered.groupby(['날짜', '광역지자체'])['인원'].sum().reset_index(),
        x='날짜',
        y='인원',
        color='광역지자체',
        title='상위 10개 지역 위탁병원 이용인원 추이',
        labels={'인원': '이용인원 (명)', '날짜': '연월'},
        height=600
    )
    
    fig.update_layout(
        title_x=0.5,
        hovermode='x unified',
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02
        )
    )
    
    return fig


def create_yearly_area_chart(df):
    """연도별 위탁병원 이용인원 Area 차트 생성 (Chart 4용)"""
    # 데이터 전처리
    df['인원'] = pd.to_numeric(df['인원'], errors='coerce')
    df['연도'] = pd.to_numeric(df['연도'], errors='coerce')
    df['월'] = pd.to_numeric(df['월'], errors='coerce')
    
    # 연도별, 월별 집계
    yearly_monthly = df.groupby(['연도', '월'])['인원'].sum().reset_index()
    
    # 날짜 컬럼 생성
    yearly_monthly['연월'] = yearly_monthly['연도'].astype(str) + '-' + yearly_monthly['월'].astype(str).str.zfill(2)
    yearly_monthly['날짜'] = pd.to_datetime(yearly_monthly['연월'] + '-01')
    
    # Area 차트 생성
    fig = go.Figure()
    
    # 연도별로 분리해서 Area 추가
    for year in sorted(yearly_monthly['연도'].unique()):
        year_data = yearly_monthly[yearly_monthly['연도'] == year].sort_values('월')
        
        fig.add_trace(go.Scatter(
            x=year_data['월'],
            y=year_data['인원'],
            name=f'{int(year)}년',
            mode='lines+markers',
            fill='tonexty' if year != yearly_monthly['연도'].min() else 'tozeroy',
            line=dict(width=3),
            marker=dict(size=8),
            hovertemplate='%{fullData.name}<br>월: %{x}월<br>인원: %{y:,.0f}명<extra></extra>'
        ))
    
    fig.update_layout(
        title=dict(
            text='전국 위탁병원 연도별 월별 이용인원 추이',
            x=0.5,
            font=dict(size=20)
        ),
        xaxis=dict(
            title='월',
            tickmode='linear',
            tick0=1,
            dtick=1,
            range=[0.5, 12.5],
            gridcolor='rgba(128, 128, 128, 0.2)'
        ),
        yaxis=dict(
            title='이용인원 (명)',
            tickformat=',',
            gridcolor='rgba(128, 128, 128, 0.2)'
        ),
        hovermode='x unified',
        width=1600,
        height=700,
        plot_bgcolor='white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            bgcolor='rgba(255, 255, 255, 0.95)',
            bordercolor='rgba(0, 0, 0, 0.3)',
            borderwidth=2,
            font=dict(size=12)
        ),
        margin=dict(t=100, r=50, l=80, b=120)
    )
    
    return fig


def create_regional_bar_chart(df):
    """광역지자체별 연도별 막대 차트 생성 (Chart 5용 - 사용자 제공 코드)"""
    # 연도별, 광역지자체별 인원 합계 계산 + 연도를 정수형으로 변환
    grouped_data = df.groupby(['연도', '광역지자체'])['인원'].sum().reset_index()
    grouped_data['연도'] = grouped_data['연도'].astype(int)  # 연도를 정수형으로 변환
    
    # Plotly 막대 차트 생성 (최종 수정 버전)
    fig = px.bar(
        grouped_data,
        x="광역지자체",  # x축: 광역지자체
        y="인원",           # y축: 이용 인원
        color="연도",       # 색상: 연도별 구분
        title="광역지자체별 연도별 위탁병원 이용 인원(이용 기간 : 2023년3월 ~ 2025년4월)",
        labels={'인원': '이용 인원'},
        barmode='group',    # 그룹별 병렬 막대
        category_orders={"연도": sorted(grouped_data['연도'].unique())}  # 고유 연도 자동 정렬
    )
    
    # 차트 레이아웃 최적화
    fig.update_layout(
        xaxis_title="광역지자체",
        yaxis_title="이용 인원",
        hoverlabel=dict(namelength=-1),  # 호버 툴팁 길이 제한 해제
        hovermode="closest",            # 마우스 근처 항목 강조
        xaxis=dict(tickangle=-45),      # x축 레이블 회전
        height=600,
        width=1000
    )
    
    return fig


def create_pivot_bar_chart(df):
    """광역지자체별 연도별 Pivot 막대 차트 생성 (Chart 6용 - Matplotlib 스타일)"""
    # 필요한 컬럼만 선택
    cols_needed = ["연도", "광역지자체", "인원"]
    df_filtered = df[cols_needed].copy()
    
    # 연도별, 광역지자체별 인원 합계 계산
    grouped = df_filtered.groupby(["연도", "광역지자체"], as_index=False)["인원"].sum()
    
    # Pivot 테이블 생성
    pivot_df = grouped.pivot(index="광역지자체", columns="연도", values="인원").fillna(0)
    
    # Plotly 막대 차트 생성
    fig = go.Figure()
    
    # 각 연도별로 막대 추가
    for year in sorted(pivot_df.columns):
        fig.add_trace(go.Bar(
            name=str(int(year)),
            x=pivot_df.index,
            y=pivot_df[year],
            text=pivot_df[year].apply(lambda x: f'{int(x):,}' if x > 0 else ''),
            textposition='auto',
            hovertemplate='%{x}<br>%{fullData.name}년<br>인원: %{y:,.0f}명<extra></extra>'
        ))
    
    fig.update_layout(
        title='광역지자체별 이용 인원(이용 기간 : 2023년3월 ~ 2025년4월)',
        title_font_size=16,
        xaxis_title="광역지자체",
        xaxis_title_font_size=12,
        yaxis_title="이용 인원 수",
        yaxis_title_font_size=12,
        barmode='group',
        xaxis=dict(
            tickangle=45,
            tickmode='linear'
        ),
        yaxis=dict(
            tickformat=','
        ),
        legend=dict(
            title="연도",
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="right",
            x=1
        ),
        height=600,
        width=1100,
        hovermode='closest'
    )
    
    return fig


def create_yearly_pie_subplots(df):
    """연도별 광역지자체별 파이차트 서브플롯 생성 (Chart 7용 - 사용자 제공 코드)"""
    # 연도별, 광역지자체별 인원 합계 계산
    grouped_data = df.groupby(['연도', '광역지자체'])['인원'].sum().reset_index()
    
    # 고유 연도 목록 추출 및 서브플롯 행/열 계산
    unique_years = grouped_data['연도'].unique()
    n_years = len(unique_years)
    rows = int(n_years ** 0.5) + 1
    cols = int((n_years + rows - 1) // rows)
    
    # 올바른 2차원 specs 생성 (행 x 열 구조)
    specs = [[{'type': 'pie'} for _ in range(cols)] for _ in range(rows)]
    
    # 서브플롯 생성
    fig = make_subplots(
        specs=specs,
        rows=rows,
        cols=cols,
        subplot_titles=[f"연도 {int(year)}" for year in unique_years]
    )
    
    # 각 연도별 파이차트 생성
    for i, year in enumerate(unique_years):
        # 현재 연도 데이터 필터링
        year_data = grouped_data[grouped_data['연도'] == year].sort_values('인원', ascending=False)
        
        # 파이차트 생성 (go.Pie 사용)
        fig.add_trace(
            go.Pie(
                labels=year_data['광역지자체'],
                values=year_data['인원'],
                name=f"연도 {int(year)}",
                hole=0.4,
                marker=dict(colors=px.colors.qualitative.Plotly[:len(year_data)]),
                hoverinfo='label+value',
                textinfo='label+percent',
                textposition='inside',
                domain={'x': [0, 1], 'y': [0, 1]}  # 서브플롯 영역 채우기
            ),
            row=(i // cols) + 1,  # 행 인덱스 (1-based)
            col=i % cols + 1       # 열 인덱스 (1-based)
        )
    
    # 전체 레이아웃 최적화
    fig.update_layout(
        title='연도별 광역지자체코드별 위탁병원 이용 인원 비율 파이차트(이용 기간 : 2023년3월 ~ 2025년4월)',
        height=1000,
        width=1000
    )
    
    return fig


def save_chart_as_html(fig, filename, chart_folder='Chart/public'):
    """차트를 HTML 파일로 저장"""
    output_path = Path(__file__).parent / chart_folder / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    fig.write_html(
        str(output_path),
        include_plotlyjs='cdn',
        config={'responsive': True}
    )
    
    print(f"✅ 차트 저장 완료: {output_path}")
    return output_path

def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("📊 Plotly 차트 생성 시작...")
    print("=" * 60)
    
    # 연도별 통계 데이터 로드 (Chart 1, 2용)
    df_yearly = load_yearly_statistics()
    if df_yearly is not None:
        print(f"\n연도별 통계 데이터 정보:")
        print(f"  - 총 행 수: {len(df_yearly)}")
        print(f"  - 컬럼: {list(df_yearly.columns)}")
        
        # Chart 1: 광역지자체별 연도별 막대 차트
        print("\n📊 Chart 1: 광역지자체별 연도별 막대 차트 생성 중...")
        fig_chart1 = create_chart1_regional_yearly_bar(df_yearly)
        save_chart_as_html(fig_chart1, 'chart1_regional_yearly.html')
        
        # Chart 2: 연도별 전체 합계 추세 라인 차트
        print("\n📈 Chart 2: 연도별 전체 합계 추세 라인 차트 생성 중...")
        fig_chart2 = create_chart2_yearly_trend_line(df_yearly)
        save_chart_as_html(fig_chart2, 'chart2_yearly_trend.html')
    else:
        print("\n⚠️ 연도별 통계 데이터를 불러올 수 없어 Chart 1, 2를 건너뜁니다.")
    
    # 지역별 이용인원 데이터 로드 (Chart 3~7용)
    df = load_data_from_mysql()
    if df is None:
        return
    
    print(f"\n데이터 정보:")
    print(f"  - 총 행 수: {len(df)}")
    print(f"  - 컬럼: {list(df.columns)}")
    print(f"  - 지역 수: {df['광역지자체'].nunique()}")
    
    # 3. 원본 산점도 행렬 (Chart 3)
    print("\n1️⃣ 산점도 행렬 차트 생성 중...")
    fig1 = create_scatter_matrix_chart(df)
    save_chart_as_html(fig1, 'chart3_scatter_matrix.html')
    
    # 2. 상관관계 히트맵 (더 나은 방법)
    print("\n2️⃣ 상관관계 히트맵 생성 중...")
    fig2 = create_better_correlation_chart(df)
    save_chart_as_html(fig2, 'chart3_correlation_heatmap.html')
    
    # 3. 지역별 추이 차트 (실용적)
    print("\n3️⃣ 지역별 추이 차트 생성 중...")
    fig3 = create_regional_trend_chart(df)
    save_chart_as_html(fig3, 'chart3_regional_trend.html')
    
    # 4. 연도별 월별 Area 차트 (Chart 4용)
    print("\n4️⃣ 연도별 월별 Area 차트 생성 중...")
    fig4 = create_yearly_area_chart(df)
    save_chart_as_html(fig4, 'chart4_yearly_area.html')
    
    # 5. 광역지자체별 연도별 막대 차트 (Chart 5용)
    print("\n5️⃣ 광역지자체별 연도별 막대 차트 생성 중...")
    fig5 = create_regional_bar_chart(df)
    save_chart_as_html(fig5, 'chart5_regional_bar.html')
    
    # 6. 광역지자체별 연도별 Pivot 막대 차트 (Chart 6용)
    print("\n6️⃣ 광역지자체별 연도별 Pivot 막대 차트 생성 중...")
    fig6 = create_pivot_bar_chart(df)
    save_chart_as_html(fig6, 'chart6_pivot_bar.html')
    
    # 7. 연도별 광역지자체별 파이차트 서브플롯 (Chart 7용)
    print("\n7️⃣ 연도별 광역지자체별 파이차트 서브플롯 생성 중...")
    fig7 = create_yearly_pie_subplots(df)
    save_chart_as_html(fig7, 'chart7_pie_subplots.html')
    
    print("\n" + "=" * 60)
    print("✅ 모든 차트 생성 완료!")
    print("=" * 60)
    print("\n📌 생성된 파일:")
    print("  Chart 1. chart1_regional_total.html - 광역지자체별 전체 이용인원 (NEW!)")
    print("  Chart 2. chart2_monthly_trend.html - 월별 전체 이용인원 추세 (NEW!)")
    print("  Chart 3. chart3_scatter_matrix.html - 산점도 행렬")
    print("  Chart 4. chart4_yearly_area.html - 연도별 월별 추이")
    print("  Chart 5. chart5_regional_bar.html - 광역지자체별 연도별 막대 차트")
    print("  Chart 6. chart6_pivot_bar.html - 광역지자체별 연도별 Pivot 막대 차트")
    print("  Chart 7. chart7_pie_subplots.html - 연도별 광역지자체별 파이차트 서브플롯")
    print("\n💡 React 앱에서 iframe으로 임베드하세요!")

if __name__ == "__main__":
    main()
