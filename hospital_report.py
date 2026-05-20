"""
의료기관 원무과 월간통계 보고서
제작: 주식회사 메디엄 조정윤
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
# 페이지 설정
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="원무과 월간통계 보고서 | 메디엄",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# 커스텀 CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700;900&family=Noto+Serif+KR:wght@400;600;700&display=swap');

:root {
    --primary:   #1a3a5c;
    --accent:    #2E86AB;
    --accent2:   #E84855;
    --accent3:   #F9C74F;
    --bg:        #f4f6fb;
    --card:      #ffffff;
    --border:    #dde4f0;
    --text:      #1e2940;
    --muted:     #7a8ba0;
}

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
    color: var(--text);
}

/* 배경 */
.stApp { background: var(--bg); }

/* 헤더 배너 */
.header-banner {
    background: linear-gradient(135deg, #1a3a5c 0%, #2E86AB 60%, #5dbcd2 100%);
    border-radius: 16px;
    padding: 28px 36px 22px 36px;
    margin-bottom: 24px;
    color: white;
    box-shadow: 0 6px 28px rgba(46,134,171,0.22);
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.header-title {
    font-family: 'Noto Serif KR', serif;
    font-size: 2.1rem;
    font-weight: 700;
    letter-spacing: -0.5px;
    line-height: 1.2;
    margin: 0;
}
.header-sub {
    font-size: 0.88rem;
    opacity: 0.82;
    margin-top: 6px;
    letter-spacing: 0.3px;
}
.header-creator {
    font-size: 0.78rem;
    opacity: 0.7;
    text-align: right;
    white-space: nowrap;
}

/* KPI 카드 */
.kpi-card {
    background: var(--card);
    border-radius: 14px;
    padding: 20px 22px;
    border-left: 5px solid var(--accent);
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    margin-bottom: 12px;
    transition: transform 0.15s;
}
.kpi-card:hover { transform: translateY(-2px); }
.kpi-label { font-size: 0.82rem; color: var(--muted); font-weight: 500; margin-bottom: 4px; }
.kpi-value { font-size: 2.0rem; font-weight: 900; color: var(--primary); line-height: 1; }
.kpi-delta-pos { font-size: 0.82rem; color: #16a34a; font-weight: 600; margin-top: 4px; }
.kpi-delta-neg { font-size: 0.82rem; color: #dc2626; font-weight: 600; margin-top: 4px; }
.kpi-delta-neu { font-size: 0.82rem; color: var(--muted); font-weight: 600; margin-top: 4px; }

/* 섹션 제목 */
.section-title {
    font-family: 'Noto Serif KR', serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--primary);
    border-left: 4px solid var(--accent);
    padding-left: 12px;
    margin: 24px 0 14px 0;
}

/* 비교 배지 */
.badge-up   { background:#dcfce7; color:#16a34a; border-radius:20px; padding:2px 10px; font-size:0.78rem; font-weight:700; }
.badge-down { background:#fee2e2; color:#dc2626; border-radius:20px; padding:2px 10px; font-size:0.78rem; font-weight:700; }
.badge-neu  { background:#f1f5f9; color:#64748b; border-radius:20px; padding:2px 10px; font-size:0.78rem; font-weight:700; }

/* 하단 크레딧 */
.footer-credit {
    text-align: center;
    color: var(--muted);
    font-size: 0.78rem;
    padding: 24px 0 8px 0;
    border-top: 1px solid var(--border);
    margin-top: 36px;
}

/* 탭 스타일 */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: var(--card);
    border-radius: 12px;
    padding: 6px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    margin-bottom: 16px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.88rem;
    padding: 8px 18px;
}

/* 데이터프레임 스타일 */
.dataframe-container {
    background: var(--card);
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

/* 사이드바 */
[data-testid="stSidebar"] {
    background: #1a3a5c;
}
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] label {
    color: #e0eaf7 !important;
}

/* plotly 차트 카드 */
.chart-card {
    background: var(--card);
    border-radius: 14px;
    padding: 4px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    margin-bottom: 16px;
}

/* 경고/정보 박스 */
.info-box {
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    border-radius: 10px;
    padding: 12px 16px;
    font-size: 0.88rem;
    color: #1e40af;
    margin-bottom: 16px;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 유틸 함수
# ─────────────────────────────────────────────

def excel_date_to_date(val):
    """엑셀 날짜 숫자 → datetime"""
    try:
        if isinstance(val, (int, float)):
            return datetime(1899, 12, 30) + timedelta(days=int(val))
        if isinstance(val, datetime):
            return val
        return pd.to_datetime(val)
    except Exception:
        return pd.NaT


def load_detail_file(uploaded_file):
    """접수현황 파일 로드 (상세 컬럼 포함)"""
    try:
        xls = pd.ExcelFile(uploaded_file)
        dfs = []
        for sheet in xls.sheet_names:
            df = pd.read_excel(uploaded_file, sheet_name=sheet, header=0)
            # 컬럼 정리
            df.columns = df.columns.astype(str).str.strip()
            # 수진자/접수일자 컬럼 탐색
            col_map = {}
            for c in df.columns:
                lc = c.lower().replace(' ', '').replace('/', '')
                if '수진자' in c or '환자명' in c or '성함' in c:
                    col_map['수진자'] = c
                elif '접수일자' in c or '일자' in c or '날짜' in c:
                    col_map['접수일자'] = c
                elif '환자유형' in c or '유형' in c:
                    col_map['환자유형'] = c
                elif '초재' in lc or '초/재' in c:
                    col_map['초재진'] = c
                elif '진료의사' in c or '의사' in c:
                    col_map['진료의사'] = c
                elif '주소' in c:
                    col_map['주소'] = c
                elif '내원경로' in c or '경로' in c or '진료메모' in c:
                    col_map['내원경로'] = c
                elif '주상병' in c or '상병' in c:
                    col_map['주상병'] = c
            if '접수일자' not in col_map or '환자유형' not in col_map:
                continue
            rename = {v: k for k, v in col_map.items()}
            df = df.rename(columns=rename)
            needed = list(set(['수진자','접수일자','환자유형','초재진','진료의사','주소','내원경로','주상병']) & set(df.columns))
            df = df[needed].copy()
            df['접수일자'] = df['접수일자'].apply(excel_date_to_date)
            df = df.dropna(subset=['접수일자','환자유형'])
            dfs.append(df)
        if not dfs:
            return None
        result = pd.concat(dfs, ignore_index=True)
        return result
    except Exception as e:
        st.error(f"파일 로드 오류: {e}")
        return None


def load_summary_file(uploaded_file):
    """7월 월간결산 파일 로드 (기존 형식)"""
    try:
        xls = pd.ExcelFile(uploaded_file)
        dfs = []
        for sheet in xls.sheet_names:
            df = pd.read_excel(uploaded_file, sheet_name=sheet, header=0)
            df.columns = df.columns.astype(str).str.strip()
            col_map = {}
            for c in df.columns:
                if '접수일자' in c or '일자' in c:
                    col_map['접수일자'] = c
                elif '환자유형' in c:
                    col_map['환자유형'] = c
                elif '초재' in c or '초/재' in c:
                    col_map['초재진'] = c
                elif '진료의사' in c or '의사' in c:
                    col_map['진료의사'] = c
                elif '내원경로' in c:
                    col_map['내원경로'] = c
            if '환자유형' not in col_map:
                continue
            rename = {v: k for k, v in col_map.items()}
            df = df.rename(columns=rename)
            if '접수일자' in df.columns:
                df['접수일자'] = df['접수일자'].apply(excel_date_to_date)
            df = df.dropna(subset=['환자유형'])
            dfs.append(df)
        if not dfs:
            return None
        return pd.concat(dfs, ignore_index=True)
    except Exception as e:
        st.error(f"파일 로드 오류: {e}")
        return None


def normalize_route(val):
    """내원경로 정규화"""
    if pd.isna(val):
        return '알수없음'
    val = str(val).strip()
    if '지인' in val or '소개' in val:
        return '지인소개'
    if '온라인' in val or '인터넷' in val or '블로그' in val or 'sns' in val.lower():
        return '온라인광고'
    if '오프라인' in val:
        return '오프라인광고'
    if '간판' in val:
        return '간판'
    if '협약' in val:
        return '협약'
    if '직원' in val:
        return '직원'
    if '기타' in val:
        return '기타'
    if '알수없음' in val or val == '' or val == 'nan':
        return '알수없음'
    return val


def extract_city(addr):
    """주소에서 시/군/구 추출"""
    if pd.isna(addr) or str(addr).strip() == '':
        return '미기재'
    addr = str(addr)
    import re
    m = re.search(r'([\w]+시|[\w]+군|[\w]+구)', addr)
    if m:
        return m.group(1)
    return '기타'


def extract_disease_category(val):
    """주상병 코드 → 카테고리"""
    if pd.isna(val):
        return '미분류'
    val = str(val)
    import re
    codes = re.findall(r'\[([A-Z]\d+)', val)
    if not codes:
        return '미분류'
    c = codes[0]
    if c.startswith('S'):
        return '외상/염좌'
    if c.startswith('M'):
        return '근골격계'
    if c.startswith('G'):
        return '신경계'
    if c.startswith('J'):
        return '호흡기계'
    if c.startswith('K'):
        return '소화기계'
    if c.startswith('I'):
        return '심혈관계'
    if c.startswith('E'):
        return '내분비계'
    if c.startswith('R'):
        return '증상/징후'
    if c.startswith('U'):
        return '한방질환'
    if c.startswith('C'):
        return '종양'
    return '기타'


def make_kpi_html(label, value, delta=None, unit=""):
    """KPI 카드 HTML"""
    if delta is not None:
        if delta > 0:
            delta_html = f'<div class="kpi-delta-pos">▲ {delta:+.1f}% 전월 대비</div>'
        elif delta < 0:
            delta_html = f'<div class="kpi-delta-neg">▼ {delta:.1f}% 전월 대비</div>'
        else:
            delta_html = f'<div class="kpi-delta-neu">— 전월 동일</div>'
    else:
        delta_html = ''
    return f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}{unit}</div>
        {delta_html}
    </div>
    """


COLOR_SEQ = ['#2E86AB','#E84855','#F9C74F','#06D6A0','#8338EC','#FF6B6B','#4ECDC4','#45B7D1','#96CEB4','#FFEAA7']
CHART_TEMPLATE = "plotly_white"

def pie_chart(df_count, names_col, values_col, title, color_seq=None):
    colors = color_seq or COLOR_SEQ
    fig = px.pie(
        df_count, names=names_col, values=values_col,
        title=title, color_discrete_sequence=colors,
        hole=0.42
    )
    fig.update_traces(textposition='outside', textinfo='percent+label', pull=[0.04]*len(df_count))
    fig.update_layout(
        template=CHART_TEMPLATE,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.28, xanchor="center", x=0.5),
        margin=dict(t=50, b=60, l=10, r=10),
        title_font_size=14,
        font_family="Noto Sans KR",
        height=380,
    )
    return fig


def bar_chart(df, x, y, title, color=None, orientation='v'):
    fig = px.bar(
        df, x=x, y=y, title=title,
        color=color or y,
        color_discrete_sequence=COLOR_SEQ,
        orientation=orientation,
        text_auto=True,
        template=CHART_TEMPLATE
    )
    fig.update_layout(
        showlegend=False,
        margin=dict(t=50, b=40, l=30, r=10),
        title_font_size=14,
        font_family="Noto Sans KR",
        height=360,
    )
    fig.update_traces(textfont_size=11, textangle=0, textposition="outside", cliponaxis=False)
    return fig


def comparison_bar(labels, val_curr, val_prev, label_curr, label_prev, title):
    fig = go.Figure(data=[
        go.Bar(name=label_prev, x=labels, y=val_prev, marker_color='#b0c4de', text=val_prev,
               textposition='outside', textfont_size=10),
        go.Bar(name=label_curr, x=labels, y=val_curr, marker_color='#2E86AB', text=val_curr,
               textposition='outside', textfont_size=10),
    ])
    fig.update_layout(
        barmode='group', title=title,
        template=CHART_TEMPLATE,
        legend=dict(orientation="h", y=1.12, x=0),
        margin=dict(t=60, b=40, l=30, r=10),
        font_family="Noto Sans KR",
        height=380,
        title_font_size=14,
    )
    return fig


def line_chart_daily(df, date_col, title):
    df2 = df.copy()
    df2['날짜'] = pd.to_datetime(df2[date_col]).dt.date
    daily = df2.groupby('날짜').size().reset_index(name='환자수')
    fig = px.line(daily, x='날짜', y='환자수', title=title,
                  markers=True, template=CHART_TEMPLATE,
                  color_discrete_sequence=['#2E86AB'])
    fig.update_traces(line_width=2.5, marker_size=6)
    fig.update_layout(
        font_family="Noto Sans KR", height=320,
        margin=dict(t=50, b=30, l=30, r=10), title_font_size=14
    )
    return fig


# ─────────────────────────────────────────────
# 사이드바
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 18px 0 12px 0;">
        <div style="font-size:2.4rem;">🏥</div>
        <div style="color:#e0eaf7; font-size:1.05rem; font-weight:700; margin-top:6px;">원무과 통계 시스템</div>
        <div style="color:#8aaecb; font-size:0.76rem; margin-top:4px;">Medical Statistics Dashboard</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    st.markdown('<p style="color:#93b9d4; font-size:0.83rem; font-weight:600;">📂 이번달 접수현황 파일</p>', unsafe_allow_html=True)
    file_curr = st.file_uploader("이번달 (접수현황 xlsx)", type=["xlsx","xls"], key="curr",
                                  label_visibility="collapsed")

    st.markdown('<p style="color:#93b9d4; font-size:0.83rem; font-weight:600; margin-top:12px;">📂 저번달 접수현황 파일</p>', unsafe_allow_html=True)
    file_prev = st.file_uploader("저번달 (접수현황 xlsx)", type=["xlsx","xls"], key="prev",
                                  label_visibility="collapsed")

    st.markdown('<p style="color:#93b9d4; font-size:0.83rem; font-weight:600; margin-top:12px;">📂 월간결산 파일 (선택)</p>', unsafe_allow_html=True)
    file_summary = st.file_uploader("월간결산 xlsx", type=["xlsx","xls"], key="sum",
                                     label_visibility="collapsed")

    st.markdown("---")
    st.markdown('<p style="color:#93b9d4; font-size:0.83rem;">🔧 보고서 옵션</p>', unsafe_allow_html=True)
    show_rawdata = st.checkbox("원본 데이터 테이블 표시", value=False)
    top_disease_n = st.slider("주상병 Top N", 5, 20, 10)
    st.markdown("---")
    st.markdown("""
    <div style="color:#8aaecb; font-size:0.72rem; text-align:center; line-height:1.8;">
        제작: 주식회사 메디엄<br>
        조정윤
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 헤더
# ─────────────────────────────────────────────
now_str = datetime.now().strftime("%Y년 %m월 %d일")
st.markdown(f"""
<div class="header-banner">
    <div>
        <div class="header-title">🏥 의료기관 원무과 월간통계 보고서</div>
        <div class="header-sub">Medical Administration Monthly Statistics Report</div>
    </div>
    <div class="header-creator">
        주식회사 메디엄 조정윤<br>
        <span style="font-size:0.72rem; opacity:0.6;">{now_str} 기준</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 파일 없을 때 안내
# ─────────────────────────────────────────────
if not file_curr and not file_prev and not file_summary:
    st.markdown("""
    <div class="info-box">
        ℹ️ 좌측 사이드바에서 <b>이번달</b> 및 <b>저번달 접수현황 파일(xlsx)</b>을 업로드하면
        자동으로 비교 분석 보고서가 생성됩니다.<br>
        월간결산 파일은 선택사항입니다.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#fff; border-radius:14px; padding:28px 32px; box-shadow:0 2px 12px rgba(0,0,0,0.07);">
    <div class="section-title">📋 지원하는 분석 항목</div>
    <table style="width:100%; border-collapse:collapse; font-size:0.9rem;">
    <tr style="background:#f0f6ff;">
        <th style="padding:10px 16px; text-align:left; border-bottom:2px solid #dde4f0;">분석 구분</th>
        <th style="padding:10px 16px; text-align:left; border-bottom:2px solid #dde4f0;">세부 항목</th>
    </tr>
    <tr><td style="padding:9px 16px; border-bottom:1px solid #eee;">📊 핵심 지표 (KPI)</td>
        <td style="padding:9px 16px; border-bottom:1px solid #eee;">총 내원환자수, 신환수, 재진수, 자보환자수, 전월 대비 증감</td></tr>
    <tr><td style="padding:9px 16px; border-bottom:1px solid #eee;">🩺 환자유형 분석</td>
        <td style="padding:9px 16px; border-bottom:1px solid #eee;">건강보험 / 자보 / 의료급여 / 일반 비율 및 전월 비교</td></tr>
    <tr><td style="padding:9px 16px; border-bottom:1px solid #eee;">👨‍⚕️ 진료의사별 분석</td>
        <td style="padding:9px 16px; border-bottom:1px solid #eee;">한방1·2·3·5과, 양방6·7과 등 과별 내원환자 현황</td></tr>
    <tr><td style="padding:9px 16px; border-bottom:1px solid #eee;">📅 초·재진 현황</td>
        <td style="padding:9px 16px; border-bottom:1px solid #eee;">신규·초진·재진·미산정 구분, 전월 비교</td></tr>
    <tr><td style="padding:9px 16px; border-bottom:1px solid #eee;">📍 내원경로 분석</td>
        <td style="padding:9px 16px; border-bottom:1px solid #eee;">간판/온라인/지인소개/협약 등 경로별 비율</td></tr>
    <tr><td style="padding:9px 16px; border-bottom:1px solid #eee;">🗺️ 주소(지역) 분석</td>
        <td style="padding:9px 16px; border-bottom:1px solid #eee;">환자 거주 지역 분포</td></tr>
    <tr><td style="padding:9px 16px; border-bottom:1px solid #eee;">🏷️ 주상병 분석</td>
        <td style="padding:9px 16px; border-bottom:1px solid #eee;">다빈도 상병 Top N, 카테고리별 분류</td></tr>
    <tr><td style="padding:9px 16px;">📈 일별 내원 추이</td>
        <td style="padding:9px 16px;">일자별 환자수 변동 그래프</td></tr>
    </table>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="footer-credit">
        ⓒ 주식회사 메디엄 조정윤 | Medical Administration Statistics System
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# ─────────────────────────────────────────────
# 데이터 로드
# ─────────────────────────────────────────────
df_curr = load_detail_file(file_curr) if file_curr else None
df_prev = load_detail_file(file_prev) if file_prev else None
df_sum  = load_summary_file(file_summary) if file_summary else None

# 내원경로 정규화
for df in [df_curr, df_prev, df_sum]:
    if df is not None and '내원경로' in df.columns:
        df['내원경로'] = df['내원경로'].apply(normalize_route)

# 주소 → 시군구
for df in [df_curr, df_prev]:
    if df is not None and '주소' in df.columns:
        df['지역'] = df['주소'].apply(extract_city)

# 주상병 카테고리
for df in [df_curr, df_prev]:
    if df is not None and '주상병' in df.columns:
        df['상병카테고리'] = df['주상병'].apply(extract_disease_category)

# 월 레이블
def get_month_label(df):
    if df is None or '접수일자' not in df.columns:
        return '?월'
    valid = df['접수일자'].dropna()
    if len(valid) == 0:
        return '?월'
    m = pd.to_datetime(valid).dt.month.mode()
    y = pd.to_datetime(valid).dt.year.mode()
    if len(m) == 0:
        return '?월'
    return f"{int(y.iloc[0])}년 {int(m.iloc[0])}월"

label_curr = get_month_label(df_curr) if df_curr is not None else "이번달"
label_prev = get_month_label(df_prev) if df_prev is not None else "저번달"


# ─────────────────────────────────────────────
# 탭 구성
# ─────────────────────────────────────────────
tabs = st.tabs([
    "📊 핵심 요약",
    "🩺 환자유형",
    "👨‍⚕️ 진료의사",
    "📅 초·재진",
    "📍 내원경로",
    "🗺️ 지역 분포",
    "🏷️ 주상병",
    "📈 일별 추이",
    "📋 원본 데이터"
])


# ─────────────────────────────────────────────────
# TAB 0: 핵심 요약
# ─────────────────────────────────────────────────
with tabs[0]:
    st.markdown('<div class="section-title">📊 핵심 지표 (KPI) 요약</div>', unsafe_allow_html=True)

    def safe_count(df):
        return len(df) if df is not None else 0

    def safe_filter_count(df, col, val):
        if df is None or col not in df.columns:
            return 0
        return len(df[df[col].str.contains(val, na=False)])

    def delta_pct(curr, prev):
        if prev == 0:
            return None
        return round((curr - prev) / prev * 100, 1)

    n_curr = safe_count(df_curr)
    n_prev = safe_count(df_prev)

    # 신환 (신규 or 초진)
    def new_patient_count(df):
        if df is None or '초재진' not in df.columns:
            return 0
        return len(df[df['초재진'].isin(['신규','초진'])])

    # 자보환자
    def jabo_count(df):
        if df is None or '환자유형' not in df.columns:
            return 0
        return len(df[df['환자유형'] == '자보'])

    n_new_curr = new_patient_count(df_curr)
    n_new_prev = new_patient_count(df_prev)
    n_jabo_curr = jabo_count(df_curr)
    n_jabo_prev = jabo_count(df_prev)

    # 재진
    def re_count(df):
        if df is None or '초재진' not in df.columns:
            return 0
        return len(df[df['초재진'] == '재진'])

    n_re_curr = re_count(df_curr)
    n_re_prev = re_count(df_prev)

    cols = st.columns(4)
    with cols[0]:
        st.markdown(make_kpi_html("총 내원 환자수", f"{n_curr:,}", delta_pct(n_curr, n_prev), "명"), unsafe_allow_html=True)
    with cols[1]:
        st.markdown(make_kpi_html("신환 (신규·초진)", f"{n_new_curr:,}", delta_pct(n_new_curr, n_new_prev), "명"), unsafe_allow_html=True)
    with cols[2]:
        st.markdown(make_kpi_html("재진 환자수", f"{n_re_curr:,}", delta_pct(n_re_curr, n_re_prev), "명"), unsafe_allow_html=True)
    with cols[3]:
        st.markdown(make_kpi_html("자보 환자수", f"{n_jabo_curr:,}", delta_pct(n_jabo_curr, n_jabo_prev), "명"), unsafe_allow_html=True)

    # 2행 KPI
    def ins_count(df):
        if df is None or '환자유형' not in df.columns:
            return 0
        return len(df[df['환자유형'] == '건강보험'])

    def med_aid_count(df):
        if df is None or '환자유형' not in df.columns:
            return 0
        return len(df[df['환자유형'] == '의료급여'])

    def doctor_count(df):
        if df is None or '진료의사' not in df.columns:
            return 0
        return df['진료의사'].nunique()

    def route_top(df):
        if df is None or '내원경로' not in df.columns:
            return '-'
        s = df['내원경로'].value_counts()
        return s.index[0] if len(s) > 0 else '-'

    cols2 = st.columns(4)
    with cols2[0]:
        c = ins_count(df_curr); p = ins_count(df_prev)
        st.markdown(make_kpi_html("건강보험 환자수", f"{c:,}", delta_pct(c, p), "명"), unsafe_allow_html=True)
    with cols2[1]:
        c = med_aid_count(df_curr); p = med_aid_count(df_prev)
        st.markdown(make_kpi_html("의료급여 환자수", f"{c:,}", delta_pct(c, p), "명"), unsafe_allow_html=True)
    with cols2[2]:
        st.markdown(make_kpi_html("활동 진료과 수", f"{doctor_count(df_curr):,}", None, "과"), unsafe_allow_html=True)
    with cols2[3]:
        rt = route_top(df_curr)
        st.markdown(make_kpi_html("주요 내원경로", rt, None, ""), unsafe_allow_html=True)

    # 전월 비교 요약 테이블
    if df_curr is not None and df_prev is not None:
        st.markdown('<div class="section-title">📋 전월 대비 핵심 비교표</div>', unsafe_allow_html=True)

        rows = []
        def type_cnt(df, t):
            if df is None or '환자유형' not in df.columns: return 0
            return int((df['환자유형'] == t).sum())

        for label, c_val, p_val in [
            ("총 내원환자", n_curr, n_prev),
            ("신환", n_new_curr, n_new_prev),
            ("재진", n_re_curr, n_re_prev),
            ("건강보험", type_cnt(df_curr,'건강보험'), type_cnt(df_prev,'건강보험')),
            ("자보", type_cnt(df_curr,'자보'), type_cnt(df_prev,'자보')),
            ("의료급여", type_cnt(df_curr,'의료급여'), type_cnt(df_prev,'의료급여')),
            ("일반", type_cnt(df_curr,'일반'), type_cnt(df_prev,'일반')),
        ]:
            diff = c_val - p_val
            pct = round(diff / p_val * 100, 1) if p_val else 0
            badge = "▲" if diff > 0 else ("▼" if diff < 0 else "—")
            color = "#16a34a" if diff > 0 else ("#dc2626" if diff < 0 else "#64748b")
            rows.append({
                "항목": label,
                label_prev: p_val,
                label_curr: c_val,
                "증감": f"{diff:+d}",
                "증감률": f"{pct:+.1f}%",
                "추세": badge
            })
        compare_df = pd.DataFrame(rows)
        st.dataframe(compare_df, use_container_width=True, hide_index=True,
                     column_config={
                         "추세": st.column_config.TextColumn("추세", width="small"),
                         "증감률": st.column_config.TextColumn("증감률", width="small"),
                     })

        # 전월 비교 막대그래프
        fig_cmp = comparison_bar(
            [r["항목"] for r in rows],
            [r[label_curr] for r in rows],
            [r[label_prev] for r in rows],
            label_curr, label_prev,
            "전월 대비 핵심 지표 비교"
        )
        st.plotly_chart(fig_cmp, use_container_width=True)


# ─────────────────────────────────────────────────
# TAB 1: 환자유형
# ─────────────────────────────────────────────────
with tabs[1]:
    st.markdown('<div class="section-title">🩺 환자유형 분석</div>', unsafe_allow_html=True)

    def type_dist(df):
        if df is None or '환자유형' not in df.columns:
            return pd.DataFrame()
        vc = df['환자유형'].value_counts()
        return pd.DataFrame({'환자유형': vc.index, '환자수': vc.values})

    col1, col2 = st.columns(2)
    with col1:
        td = type_dist(df_curr)
        if not td.empty:
            fig = pie_chart(td, '환자유형', '환자수', f"{label_curr} 환자유형 분포")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("이번달 데이터 없음")

    with col2:
        td2 = type_dist(df_prev)
        if not td2.empty:
            fig2 = pie_chart(td2, '환자유형', '환자수', f"{label_prev} 환자유형 분포")
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("저번달 데이터 없음")

    # 비교 막대
    if df_curr is not None and df_prev is not None and '환자유형' in df_curr.columns and '환자유형' in df_prev.columns:
        all_types = sorted(set(df_curr['환자유형'].unique()) | set(df_prev['환자유형'].unique()))
        c_vals = [int((df_curr['환자유형']==t).sum()) for t in all_types]
        p_vals = [int((df_prev['환자유형']==t).sum()) for t in all_types]
        fig3 = comparison_bar(all_types, c_vals, p_vals, label_curr, label_prev, "환자유형 전월 비교")
        st.plotly_chart(fig3, use_container_width=True)

        # 비율 비교 테이블
        st.markdown('<div class="section-title">환자유형 비율 비교</div>', unsafe_allow_html=True)
        total_c = len(df_curr); total_p = len(df_prev)
        tbl = []
        for t, c, p in zip(all_types, c_vals, p_vals):
            tbl.append({
                "환자유형": t,
                f"{label_prev} 수": p,
                f"{label_prev} 비율": f"{p/total_p*100:.1f}%" if total_p else "-",
                f"{label_curr} 수": c,
                f"{label_curr} 비율": f"{c/total_c*100:.1f}%" if total_c else "-",
                "증감": f"{c-p:+d}",
            })
        st.dataframe(pd.DataFrame(tbl), use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────
# TAB 2: 진료의사
# ─────────────────────────────────────────────────
with tabs[2]:
    st.markdown('<div class="section-title">👨‍⚕️ 진료의사(과)별 내원 현황</div>', unsafe_allow_html=True)

    def doc_dist(df):
        if df is None or '진료의사' not in df.columns:
            return pd.DataFrame()
        vc = df['진료의사'].value_counts()
        return pd.DataFrame({'진료의사': vc.index, '환자수': vc.values})

    col1, col2 = st.columns(2)
    with col1:
        dd = doc_dist(df_curr)
        if not dd.empty:
            fig = bar_chart(dd, '진료의사', '환자수', f"{label_curr} 진료의사별 환자수")
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        dd2 = doc_dist(df_prev)
        if not dd2.empty:
            fig2 = bar_chart(dd2, '진료의사', '환자수', f"{label_prev} 진료의사별 환자수")
            st.plotly_chart(fig2, use_container_width=True)

    # 전월 비교
    if df_curr is not None and df_prev is not None and '진료의사' in df_curr.columns and '진료의사' in df_prev.columns:
        all_docs = sorted(set(df_curr['진료의사'].unique()) | set(df_prev['진료의사'].unique()))
        c_vals = [int((df_curr['진료의사']==d).sum()) for d in all_docs]
        p_vals = [int((df_prev['진료의사']==d).sum()) for d in all_docs]
        fig3 = comparison_bar(all_docs, c_vals, p_vals, label_curr, label_prev, "진료의사별 전월 비교")
        st.plotly_chart(fig3, use_container_width=True)

        # 상세 테이블
        total_c = len(df_curr); total_p = len(df_prev)
        tbl = []
        for d, c, p in zip(all_docs, c_vals, p_vals):
            # 환자유형별 breakdown
            if '환자유형' in df_curr.columns:
                types_c = df_curr[df_curr['진료의사']==d]['환자유형'].value_counts().to_dict()
            else:
                types_c = {}
            tbl.append({
                "진료의사": d,
                f"{label_prev}": p,
                f"{label_prev} 비율": f"{p/total_p*100:.1f}%" if total_p else "-",
                f"{label_curr}": c,
                f"{label_curr} 비율": f"{c/total_c*100:.1f}%" if total_c else "-",
                "증감": f"{c-p:+d}",
                "건강보험": types_c.get('건강보험', 0),
                "자보": types_c.get('자보', 0),
            })
        st.dataframe(pd.DataFrame(tbl), use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────
# TAB 3: 초재진
# ─────────────────────────────────────────────────
with tabs[3]:
    st.markdown('<div class="section-title">📅 초·재진 현황 분석</div>', unsafe_allow_html=True)

    def cr_dist(df):
        if df is None or '초재진' not in df.columns:
            return pd.DataFrame()
        vc = df['초재진'].value_counts()
        return pd.DataFrame({'구분': vc.index, '환자수': vc.values})

    col1, col2 = st.columns(2)
    with col1:
        cd = cr_dist(df_curr)
        if not cd.empty:
            fig = pie_chart(cd, '구분', '환자수', f"{label_curr} 초·재진 현황")
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        cd2 = cr_dist(df_prev)
        if not cd2.empty:
            fig2 = pie_chart(cd2, '구분', '환자수', f"{label_prev} 초·재진 현황")
            st.plotly_chart(fig2, use_container_width=True)

    # 전월 비교
    if df_curr is not None and df_prev is not None and '초재진' in df_curr.columns and '초재진' in df_prev.columns:
        all_cr = sorted(set(df_curr['초재진'].dropna().unique()) | set(df_prev['초재진'].dropna().unique()))
        c_vals = [int((df_curr['초재진']==t).sum()) for t in all_cr]
        p_vals = [int((df_prev['초재진']==t).sum()) for t in all_cr]
        fig3 = comparison_bar(all_cr, c_vals, p_vals, label_curr, label_prev, "초·재진 전월 비교")
        st.plotly_chart(fig3, use_container_width=True)

    # 진료의사별 초재진 교차분석
    if df_curr is not None and '진료의사' in df_curr.columns and '초재진' in df_curr.columns:
        st.markdown('<div class="section-title">진료의사 × 초·재진 교차분석</div>', unsafe_allow_html=True)
        cross = pd.crosstab(df_curr['진료의사'], df_curr['초재진'])
        cross['합계'] = cross.sum(axis=1)
        cross = cross.sort_values('합계', ascending=False)
        st.dataframe(cross, use_container_width=True)

        fig_heat = px.imshow(
            cross.drop(columns=['합계']),
            title="진료의사별 초·재진 히트맵",
            color_continuous_scale='Blues',
            template=CHART_TEMPLATE,
            text_auto=True,
            aspect='auto'
        )
        fig_heat.update_layout(font_family="Noto Sans KR", height=350, title_font_size=14)
        st.plotly_chart(fig_heat, use_container_width=True)


# ─────────────────────────────────────────────────
# TAB 4: 내원경로
# ─────────────────────────────────────────────────
with tabs[4]:
    st.markdown('<div class="section-title">📍 내원경로 분석</div>', unsafe_allow_html=True)

    def route_dist(df):
        if df is None or '내원경로' not in df.columns:
            return pd.DataFrame()
        vc = df['내원경로'].value_counts()
        return pd.DataFrame({'경로': vc.index, '환자수': vc.values})

    col1, col2 = st.columns(2)
    with col1:
        rd = route_dist(df_curr)
        if not rd.empty:
            fig = pie_chart(rd, '경로', '환자수', f"{label_curr} 내원경로 분포")
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        rd2 = route_dist(df_prev)
        if not rd2.empty:
            fig2 = pie_chart(rd2, '경로', '환자수', f"{label_prev} 내원경로 분포")
            st.plotly_chart(fig2, use_container_width=True)

    # 전월 비교 가로 막대
    if df_curr is not None and df_prev is not None and '내원경로' in df_curr.columns and '내원경로' in df_prev.columns:
        all_routes = sorted(set(df_curr['내원경로'].dropna().unique()) | set(df_prev['내원경로'].dropna().unique()))
        c_vals = [int((df_curr['내원경로']==r).sum()) for r in all_routes]
        p_vals = [int((df_prev['내원경로']==r).sum()) for r in all_routes]
        fig3 = comparison_bar(all_routes, c_vals, p_vals, label_curr, label_prev, "내원경로 전월 비교")
        st.plotly_chart(fig3, use_container_width=True)

        # 비율 테이블
        total_c = len(df_curr); total_p = len(df_prev)
        tbl = []
        for r, c, p in zip(all_routes, c_vals, p_vals):
            tbl.append({
                "내원경로": r,
                f"{label_prev}": p,
                f"{label_prev} 비율": f"{p/total_p*100:.1f}%" if total_p else "-",
                f"{label_curr}": c,
                f"{label_curr} 비율": f"{c/total_c*100:.1f}%" if total_c else "-",
                "증감": f"{c-p:+d}",
            })
        st.dataframe(pd.DataFrame(tbl), use_container_width=True, hide_index=True)

    # 내원경로 × 환자유형 교차
    if df_curr is not None and '내원경로' in df_curr.columns and '환자유형' in df_curr.columns:
        st.markdown('<div class="section-title">내원경로 × 환자유형 교차분석</div>', unsafe_allow_html=True)
        cross2 = pd.crosstab(df_curr['내원경로'], df_curr['환자유형'])
        cross2['합계'] = cross2.sum(axis=1)
        st.dataframe(cross2.sort_values('합계', ascending=False), use_container_width=True)


# ─────────────────────────────────────────────────
# TAB 5: 지역 분포
# ─────────────────────────────────────────────────
with tabs[5]:
    st.markdown('<div class="section-title">🗺️ 환자 거주지역 분포</div>', unsafe_allow_html=True)

    def region_dist(df):
        if df is None or '지역' not in df.columns:
            return pd.DataFrame()
        vc = df['지역'].value_counts()
        return pd.DataFrame({'지역': vc.index, '환자수': vc.values})

    col1, col2 = st.columns(2)
    with col1:
        rgd = region_dist(df_curr)
        if not rgd.empty:
            fig = px.bar(rgd.head(15), x='지역', y='환자수',
                         title=f"{label_curr} 지역별 환자수 (상위 15)",
                         color='환자수', color_continuous_scale='Blues',
                         template=CHART_TEMPLATE, text_auto=True)
            fig.update_layout(font_family="Noto Sans KR", height=380, title_font_size=14,
                               margin=dict(t=50,b=40,l=30,r=10))
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        rgd2 = region_dist(df_prev)
        if not rgd2.empty:
            fig2 = px.bar(rgd2.head(15), x='지역', y='환자수',
                          title=f"{label_prev} 지역별 환자수 (상위 15)",
                          color='환자수', color_continuous_scale='Oranges',
                          template=CHART_TEMPLATE, text_auto=True)
            fig2.update_layout(font_family="Noto Sans KR", height=380, title_font_size=14,
                                margin=dict(t=50,b=40,l=30,r=10))
            st.plotly_chart(fig2, use_container_width=True)

    # 주소에서 읍/면/동 추출 (세부)
    if df_curr is not None and '주소' in df_curr.columns:
        import re
        st.markdown('<div class="section-title">세부 주소 분석 (읍·면·동)</div>', unsafe_allow_html=True)
        def extract_dong(addr):
            if pd.isna(addr): return '미기재'
            m = re.search(r'([\w]+읍|[\w]+면|[\w]+동)', str(addr))
            return m.group(1) if m else '기타'
        df_curr['읍면동'] = df_curr['주소'].apply(extract_dong)
        vc_dong = df_curr['읍면동'].value_counts()
        dong_dist = pd.DataFrame({'읍면동': vc_dong.index, '환자수': vc_dong.values})
        fig_dong = px.bar(dong_dist.head(20), x='읍면동', y='환자수',
                          title="읍·면·동별 환자수 (상위 20)",
                          color='환자수', color_continuous_scale='Teal',
                          template=CHART_TEMPLATE, text_auto=True)
        fig_dong.update_layout(font_family="Noto Sans KR", height=380, title_font_size=14)
        st.plotly_chart(fig_dong, use_container_width=True)


# ─────────────────────────────────────────────────
# TAB 6: 주상병
# ─────────────────────────────────────────────────
with tabs[6]:
    st.markdown('<div class="section-title">🏷️ 주상병 분석</div>', unsafe_allow_html=True)

    def disease_dist(df, n=10):
        if df is None or '주상병' not in df.columns:
            return pd.DataFrame()
        # 상병명만 추출 (코드 제거)
        import re
        def clean(val):
            if pd.isna(val): return None
            val = str(val)
            # [코드] 제거 후 질병명만
            cleaned = re.sub(r'\[[^\]]+\]\s*', '', val).strip()
            if not cleaned:
                m = re.search(r'\[([^\]]+)\]', val)
                return m.group(1) if m else val
            return cleaned[:40] if cleaned else None
        df2 = df.copy()
        df2['상병명'] = df2['주상병'].apply(clean)
        df2 = df2.dropna(subset=['상병명'])
        vc = df2['상병명'].value_counts().head(n)
        return pd.DataFrame({'상병명': vc.index, '환자수': vc.values})

    col1, col2 = st.columns(2)
    with col1:
        dd = disease_dist(df_curr, top_disease_n)
        if not dd.empty:
            fig = px.bar(dd, x='환자수', y='상병명', orientation='h',
                         title=f"{label_curr} 다빈도 상병 Top {top_disease_n}",
                         color='환자수', color_continuous_scale='Blues',
                         template=CHART_TEMPLATE, text_auto=True)
            fig.update_layout(yaxis={'categoryorder':'total ascending'},
                               font_family="Noto Sans KR", height=420, title_font_size=14)
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        dd2 = disease_dist(df_prev, top_disease_n)
        if not dd2.empty:
            fig2 = px.bar(dd2, x='환자수', y='상병명', orientation='h',
                          title=f"{label_prev} 다빈도 상병 Top {top_disease_n}",
                          color='환자수', color_continuous_scale='Oranges',
                          template=CHART_TEMPLATE, text_auto=True)
            fig2.update_layout(yaxis={'categoryorder':'total ascending'},
                                font_family="Noto Sans KR", height=420, title_font_size=14)
            st.plotly_chart(fig2, use_container_width=True)

    # 상병 카테고리
    if df_curr is not None and '상병카테고리' in df_curr.columns:
        st.markdown('<div class="section-title">상병 카테고리별 분포</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        vc_cat_c = df_curr['상병카테고리'].value_counts()
        cat_c = pd.DataFrame({'카테고리': vc_cat_c.index, '환자수': vc_cat_c.values})
        with col1:
            fig_cat = pie_chart(cat_c, '카테고리', '환자수', f"{label_curr} 상병 카테고리")
            st.plotly_chart(fig_cat, use_container_width=True)
        if df_prev is not None and '상병카테고리' in df_prev.columns:
            vc_cat_p = df_prev['상병카테고리'].value_counts()
            cat_p = pd.DataFrame({'카테고리': vc_cat_p.index, '환자수': vc_cat_p.values})
            with col2:
                fig_cat2 = pie_chart(cat_p, '카테고리', '환자수', f"{label_prev} 상병 카테고리")
                st.plotly_chart(fig_cat2, use_container_width=True)


# ─────────────────────────────────────────────────
# TAB 7: 일별 추이
# ─────────────────────────────────────────────────
with tabs[7]:
    st.markdown('<div class="section-title">📈 일별 내원환자 추이</div>', unsafe_allow_html=True)

    def daily_trend(df, label):
        if df is None or '접수일자' not in df.columns:
            return None
        df2 = df.copy()
        df2['날짜'] = pd.to_datetime(df2['접수일자']).dt.date
        daily = df2.groupby('날짜').size().reset_index(name='환자수')
        daily['월'] = label
        return daily

    d_curr = daily_trend(df_curr, label_curr)
    d_prev = daily_trend(df_prev, label_prev)

    if d_curr is not None:
        fig_daily = px.line(d_curr, x='날짜', y='환자수',
                            title=f"{label_curr} 일별 내원환자 추이",
                            markers=True, template=CHART_TEMPLATE,
                            color_discrete_sequence=['#2E86AB'])
        fig_daily.update_traces(line_width=2.5, marker_size=7)
        fig_daily.update_layout(font_family="Noto Sans KR", height=360, title_font_size=14)
        st.plotly_chart(fig_daily, use_container_width=True)

    if d_prev is not None:
        fig_daily2 = px.line(d_prev, x='날짜', y='환자수',
                             title=f"{label_prev} 일별 내원환자 추이",
                             markers=True, template=CHART_TEMPLATE,
                             color_discrete_sequence=['#E84855'])
        fig_daily2.update_traces(line_width=2.5, marker_size=7)
        fig_daily2.update_layout(font_family="Noto Sans KR", height=360, title_font_size=14)
        st.plotly_chart(fig_daily2, use_container_width=True)

    # 요일별 분석
    for df, lbl, color in [(df_curr, label_curr, '#2E86AB'), (df_prev, label_prev, '#E84855')]:
        if df is not None and '접수일자' in df.columns:
            st.markdown(f'<div class="section-title">요일별 환자수 ({lbl})</div>', unsafe_allow_html=True)
            df2 = df.copy()
            df2['요일'] = pd.to_datetime(df2['접수일자']).dt.day_name()
            day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
            day_kor = {'Monday':'월','Tuesday':'화','Wednesday':'수','Thursday':'목','Friday':'금','Saturday':'토','Sunday':'일'}
            df2['요일_한'] = df2['요일'].map(day_kor)
            vc_dow = df2['요일'].value_counts().reindex(day_order, fill_value=0)
            dow = pd.DataFrame({'요일_en': vc_dow.index, '환자수': vc_dow.values})
            dow['요일'] = dow['요일_en'].map(day_kor)
            fig_dow = px.bar(dow, x='요일', y='환자수', title=f"{lbl} 요일별 환자수",
                             color_discrete_sequence=[color],
                             template=CHART_TEMPLATE, text_auto=True)
            fig_dow.update_layout(font_family="Noto Sans KR", height=320, title_font_size=14)
            st.plotly_chart(fig_dow, use_container_width=True)
            break  # 이번달만


# ─────────────────────────────────────────────────
# TAB 8: 원본 데이터
# ─────────────────────────────────────────────────
with tabs[8]:
    st.markdown('<div class="section-title">📋 원본 데이터</div>', unsafe_allow_html=True)

    if df_curr is not None:
        st.markdown(f"**{label_curr}** — {len(df_curr):,}건")
        display_cols_curr = [c for c in ['수진자','접수일자','환자유형','초재진','진료의사','주소','내원경로','주상병'] if c in df_curr.columns]
        df_show = df_curr[display_cols_curr].copy()
        if '접수일자' in df_show.columns:
            df_show['접수일자'] = pd.to_datetime(df_show['접수일자']).dt.strftime('%Y-%m-%d')
        st.dataframe(df_show, use_container_width=True, hide_index=True)

    if df_prev is not None:
        st.markdown(f"**{label_prev}** — {len(df_prev):,}건")
        display_cols_prev = [c for c in ['수진자','접수일자','환자유형','초재진','진료의사','주소','내원경로','주상병'] if c in df_prev.columns]
        df_show2 = df_prev[display_cols_prev].copy()
        if '접수일자' in df_show2.columns:
            df_show2['접수일자'] = pd.to_datetime(df_show2['접수일자']).dt.strftime('%Y-%m-%d')
        st.dataframe(df_show2, use_container_width=True, hide_index=True)

    if df_sum is not None:
        st.markdown(f"**월간결산** — {len(df_sum):,}건")
        st.dataframe(df_sum.head(200), use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────
# 하단 크레딧
# ─────────────────────────────────────────────────
st.markdown("""
<div class="footer-credit">
    ⓒ 주식회사 메디엄 조정윤 | Medical Administration Monthly Statistics Report System<br>
    본 보고서는 의료기관 원무과 월간통계 분석을 위해 제작되었습니다.
</div>
""", unsafe_allow_html=True)
