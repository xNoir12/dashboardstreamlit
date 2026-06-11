import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path


# =============================================================================
# KONFIGURASI HALAMAN
# =============================================================================
st.set_page_config(
    page_title="BI Dashboard ISPU Jakarta",
    page_icon="🌫️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =============================================================================
# STYLE / CUSTOM CSS - LIGHT EXECUTIVE MODE
# =============================================================================
st.markdown(
    """
    <style>
        :root {
            --bg-main: #F6F1E8;
            --bg-soft: #FBF8F1;
            --bg-panel: #FFFFFF;
            --bg-panel-warm: #FFF7E8;
            --text-main: #17212B;
            --text-muted: #64748B;
            --text-soft: #475569;
            --accent: #B45309;
            --accent-2: #0F766E;
            --accent-soft: rgba(180, 83, 9, 0.12);
            --teal-soft: rgba(15, 118, 110, 0.10);
            --line: rgba(23, 33, 43, 0.11);
            --shadow: 0 18px 50px rgba(28, 25, 23, 0.10);
            --shadow-soft: 0 10px 24px rgba(28, 25, 23, 0.08);
            --good: #15803D;
            --warn: #B45309;
            --bad: #B91C1C;
        }

        html, body, .stApp {
            background:
                radial-gradient(circle at top left, rgba(180, 83, 9, 0.14), transparent 26%),
                radial-gradient(circle at top right, rgba(15, 118, 110, 0.11), transparent 24%),
                linear-gradient(180deg, #F6F1E8 0%, #FBF8F1 42%, #F6F1E8 100%) !important;
            color: var(--text-main) !important;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #FFFFFF 0%, #FFF7E8 100%) !important;
            border-right: 1px solid var(--line);
            box-shadow: 8px 0 28px rgba(28, 25, 23, 0.06);
        }

        [data-testid="stSidebar"] * {
            color: var(--text-main);
        }

        [data-testid="stSidebar"] .stCaption,
        [data-testid="stSidebar"] p {
            color: var(--text-muted) !important;
        }

        .block-container {
            padding-top: 1.25rem;
            padding-bottom: 2.4rem;
            max-width: 1500px;
        }

        h1, h2, h3 {
            color: var(--text-main) !important;
            letter-spacing: -0.035em;
        }

        p, span, label, div {
            color: inherit;
        }

        .hero {
            position: relative;
            overflow: hidden;
            padding: 1.45rem 1.55rem;
            border-radius: 28px;
            background:
                linear-gradient(135deg, rgba(255,255,255,0.92), rgba(255, 247, 232, 0.92)),
                linear-gradient(90deg, rgba(180,83,9,0.18), rgba(15,118,110,0.12));
            border: 1px solid rgba(180, 83, 9, 0.18);
            box-shadow: var(--shadow);
            margin-bottom: 1.2rem;
        }

        .hero:before {
            content: "";
            position: absolute;
            right: -90px;
            top: -120px;
            width: 310px;
            height: 310px;
            background: conic-gradient(from 120deg, rgba(180,83,9,0.22), rgba(15,118,110,0.16), rgba(180,83,9,0.08));
            border-radius: 50%;
            filter: blur(2px);
            opacity: 0.9;
        }

        .hero:after {
            content: "ISPU";
            position: absolute;
            right: 34px;
            bottom: -4px;
            font-size: 5.8rem;
            line-height: 1;
            letter-spacing: -0.08em;
            font-weight: 900;
            color: rgba(180,83,9,0.07);
        }

        .hero-title {
            position: relative;
            z-index: 1;
            font-size: 2.25rem;
            line-height: 1.06;
            font-weight: 900;
            margin-bottom: 0.42rem;
            color: var(--text-main);
        }

        .hero-subtitle {
            position: relative;
            z-index: 1;
            color: var(--text-soft);
            font-size: 0.98rem;
            max-width: 980px;
            line-height: 1.55;
        }

        .source-pill {
            position: relative;
            z-index: 1;
            display: inline-block;
            margin-top: 0.95rem;
            padding: 0.42rem 0.78rem;
            border-radius: 999px;
            background: #FFFFFF;
            border: 1px solid rgba(180,83,9,0.22);
            color: #92400E;
            font-size: 0.78rem;
            font-weight: 750;
            box-shadow: var(--shadow-soft);
        }

        .metric-card {
            background:
                linear-gradient(180deg, rgba(255,255,255,0.98), rgba(255,247,232,0.84));
            border: 1px solid rgba(23, 33, 43, 0.10);
            border-radius: 24px;
            padding: 1.05rem 1.12rem;
            box-shadow: var(--shadow-soft);
            min-height: 145px;
        }

        .metric-card:hover {
            transform: translateY(-1px);
            transition: 160ms ease;
            box-shadow: 0 16px 36px rgba(28, 25, 23, 0.12);
        }

        .metric-label {
            color: var(--text-muted);
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.09em;
            margin-bottom: 0.42rem;
            font-weight: 800;
        }

        .metric-value {
            color: var(--text-main);
            font-size: 2.45rem;
            line-height: 1.0;
            font-weight: 900;
            letter-spacing: -0.055em;
        }

        .metric-note {
            color: var(--text-soft);
            font-size: 0.82rem;
            margin-top: 0.6rem;
            line-height: 1.35;
        }

        .section-card {
            background: rgba(255,255,255,0.88);
            border: 1px solid rgba(23,33,43,0.10);
            border-radius: 24px;
            padding: 1rem 1.05rem;
            box-shadow: var(--shadow-soft);
            margin-bottom: 1rem;
        }

        .insight-box {
            border-left: 6px solid var(--accent);
            background:
                linear-gradient(90deg, rgba(180, 83, 9, 0.13), rgba(255,255,255,0.92)),
                #FFFFFF;
            border-radius: 20px;
            padding: 1rem 1.12rem;
            margin: 0.8rem 0 1rem 0;
            color: var(--text-main);
            box-shadow: var(--shadow-soft);
            border-top: 1px solid rgba(180,83,9,0.10);
            border-right: 1px solid rgba(180,83,9,0.10);
            border-bottom: 1px solid rgba(180,83,9,0.10);
        }

        .insight-title {
            color: #92400E;
            font-weight: 900;
            font-size: 0.96rem;
            margin-bottom: 0.38rem;
        }

        .insight-text {
            color: #334155;
            font-size: 0.94rem;
            line-height: 1.58;
        }

        div[data-testid="stMetric"] {
            background: #FFFFFF;
            border: 1px solid rgba(23,33,43,0.10);
            padding: 0.85rem 1rem;
            border-radius: 18px;
            box-shadow: var(--shadow-soft);
        }

        div[data-testid="stDataFrame"] {
            border: 1px solid rgba(23,33,43,0.10);
            border-radius: 16px;
            box-shadow: var(--shadow-soft);
            overflow: hidden;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.35rem;
            background: rgba(255,255,255,0.72);
            padding: 0.38rem;
            border-radius: 20px;
            border: 1px solid rgba(23,33,43,0.09);
            box-shadow: var(--shadow-soft);
        }

        .stTabs [data-baseweb="tab"] {
            background: transparent;
            border-radius: 15px;
            padding: 0.68rem 0.95rem;
            color: #475569;
            font-weight: 700;
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(180deg, rgba(180,83,9,0.16), rgba(180,83,9,0.08));
            color: #7C2D12 !important;
            border: 1px solid rgba(180,83,9,0.26);
        }

        .small-muted {
            color: var(--text-muted);
            font-size: 0.82rem;
            font-weight: 650;
        }

        /* Input controls */
        .stMultiSelect [data-baseweb="select"],
        .stDateInput input,
        .stRadio [role="radiogroup"] {
            background-color: #FFFFFF !important;
            border-radius: 14px !important;
        }

        button[kind="secondary"] {
            border-radius: 14px !important;
            border-color: rgba(180,83,9,0.25) !important;
        }

        hr {
            border: none;
            height: 1px;
            background: rgba(23,33,43,0.10);
            margin: 1rem 0;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# =============================================================================
# KONSTANTA
# =============================================================================
DATA_FILE = "ispu_jakarta_final_sot_v4_reviewed_eda_sama.csv"

CATEGORY_ORDER = [
    "BAIK",
    "SEDANG",
    "TIDAK SEHAT",
    "SANGAT TIDAK SEHAT",
    "BERBAHAYA",
]

CATEGORY_COLORS = {
    "BAIK": "#22C55E",
    "SEDANG": "#F59E0B",
    "TIDAK SEHAT": "#EF4444",
    "SANGAT TIDAK SEHAT": "#A855F7",
    "BERBAHAYA": "#7F1D1D",
}

CRITICAL_COLORS = {
    "PM10": "#F97316",
    "PM25": "#EF4444",
    "O3": "#8B5CF6",
    "CO": "#14B8A6",
    "SO2": "#EAB308",
    "NO2": "#38BDF8",
}

MONTH_MAP = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "Mei", 6: "Jun",
    7: "Jul", 8: "Agu", 9: "Sep", 10: "Okt", 11: "Nov", 12: "Des",
}

PLOTLY_TEMPLATE = "plotly_white"


# =============================================================================
# FUNGSI DATA
# =============================================================================
@st.cache_data(show_spinner="Memuat dataset ISPU Jakarta...")
def load_data(path: str = DATA_FILE) -> pd.DataFrame:
    """Load dataset final source of truth."""
    candidate_paths = [
        Path(path),
        Path(__file__).parent / path if "__file__" in globals() else Path(path),
        Path("/mnt/data") / path,
    ]

    data_path = None
    for p in candidate_paths:
        if p.exists():
            data_path = p
            break

    if data_path is None:
        raise FileNotFoundError(
            f"File dataset '{path}' tidak ditemukan. "
            "Pastikan CSV berada dalam folder yang sama dengan app.py."
        )

    df = pd.read_csv(data_path)
    df["tanggal"] = pd.to_datetime(df["tanggal"], errors="coerce")
    df = df.dropna(subset=["tanggal", "stasiun", "max", "critical", "categori"]).copy()

    numeric_cols = ["pm10", "pm25", "so2", "co", "o3", "no2", "max"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["tahun"] = df["tanggal"].dt.year
    df["bulan"] = df["tanggal"].dt.month
    df["nama_bulan"] = df["bulan"].map(MONTH_MAP)
    df["tahun_bulan"] = df["tanggal"].dt.to_period("M").astype(str)
    df["stasiun_kode"] = df["stasiun"].str.extract(r"(DKI\d)", expand=False).fillna(df["stasiun"])
    df["is_tidak_sehat_plus"] = df["categori"].isin(
        ["TIDAK SEHAT", "SANGAT TIDAK SEHAT", "BERBAHAYA"]
    )

    def musim(bulan: int) -> str:
        if bulan in [11, 12, 1, 2, 3]:
            return "Musim Hujan"
        if bulan in [6, 7, 8, 9]:
            return "Musim Kemarau"
        if bulan in [4, 5]:
            return "Peralihan I"
        return "Peralihan II"

    df["musim"] = df["bulan"].apply(musim)
    df["critical_display"] = df["critical"].replace({"PM25": "PM2.5"})

    return df


def apply_global_filters(df: pd.DataFrame, stations: list[str], date_range) -> pd.DataFrame:
    filtered = df.copy()

    if stations:
        filtered = filtered[filtered["stasiun"].isin(stations)]

    if len(date_range) == 2:
        start_date = pd.to_datetime(date_range[0])
        end_date = pd.to_datetime(date_range[1])
        filtered = filtered[
            (filtered["tanggal"] >= start_date)
            & (filtered["tanggal"] <= end_date)
        ]

    return filtered.copy()


def format_pct(value: float) -> str:
    if pd.isna(value):
        return "-"
    return f"{value:.1f}%"


def safe_mode(series: pd.Series, default: str = "-") -> str:
    s = series.dropna()
    if s.empty:
        return default
    return str(s.mode().iloc[0])


def metric_card(label: str, value: str, note: str = "") -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def insight_box(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="insight-box">
            <div class="insight-title">💡 {title}</div>
            <div class="insight-text">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def empty_state() -> None:
    st.warning("Tidak ada data pada kombinasi filter yang dipilih. Ubah stasiun atau rentang waktu di sidebar.")


def style_plotly(fig: go.Figure, height: int = 430) -> go.Figure:
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFFFF",
        font=dict(color="#17212B", family="Inter, Segoe UI, Arial"),
        title=dict(font=dict(size=18, color="#17212B"), x=0.02),
        margin=dict(l=35, r=25, t=65, b=35),
        legend=dict(
            bgcolor="rgba(255,255,255,0)",
            bordercolor="rgba(23,33,43,0)",
            font=dict(size=11, color="#334155"),
        ),
    )
    fig.update_xaxes(
        gridcolor="rgba(23,33,43,0.08)",
        zerolinecolor="rgba(23,33,43,0.12)",
        linecolor="rgba(23,33,43,0.18)",
        tickfont=dict(color="#475569"),
        title_font=dict(color="#334155"),
    )
    fig.update_yaxes(
        gridcolor="rgba(23,33,43,0.08)",
        zerolinecolor="rgba(23,33,43,0.12)",
        linecolor="rgba(23,33,43,0.18)",
        tickfont=dict(color="#475569"),
        title_font=dict(color="#334155"),
    )
    return fig


# =============================================================================
# LOAD DATA
# =============================================================================
try:
    df = load_data(DATA_FILE)
except Exception as exc:
    st.error(str(exc))
    st.stop()


# =============================================================================
# HEADER
# =============================================================================
st.markdown(
    """
    <div class="hero">
        <div class="hero-title">Executive BI Dashboard Kualitas Udara Jakarta</div>
        <div class="hero-subtitle">
            Dashboard interaktif berbasis dataset final ISPU Jakarta dengan prinsip
            <b>single source of truth</b>. Seluruh tab menggunakan sumber data yang sama,
            sehingga KPI, tren, kategori, dan pencemar kritis tetap sinkron.
        </div>
        <span class="source-pill">Source of truth: ispu_jakarta_final_sot_v4_reviewed_eda_sama.csv</span>
    </div>
    """,
    unsafe_allow_html=True,
)


# =============================================================================
# SIDEBAR FILTER GLOBAL
# =============================================================================
with st.sidebar:
    st.markdown("## Filter Global")

    all_stations = sorted(df["stasiun"].dropna().unique())
    selected_stations = st.multiselect(
        "Stasiun SPKU",
        options=all_stations,
        default=all_stations,
        help="Filter ini memengaruhi seluruh tab dashboard.",
    )

    min_date = df["tanggal"].min().date()
    max_date = df["tanggal"].max().date()
    selected_date_range = st.date_input(
        "Rentang Waktu",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        help="Filter tanggal global untuk seluruh visualisasi.",
    )

    st.markdown("---")
    st.markdown("### Catatan Data")
    st.caption(
        "Unit observasi final: 1 tanggal × 1 stasiun. "
        "Kolom max, critical, dan categori dihitung dari nilai polutan pada baris final yang sama."
    )

filtered_df = apply_global_filters(df, selected_stations, selected_date_range)

if filtered_df.empty:
    empty_state()
    st.stop()


# =============================================================================
# RINGKASAN FILTER
# =============================================================================
left, mid, right = st.columns([1.2, 1.2, 1.6])
with left:
    st.markdown(f'<div class="small-muted">Observasi terfilter</div><h3>{len(filtered_df):,}</h3>', unsafe_allow_html=True)
with mid:
    st.markdown(f'<div class="small-muted">Stasiun aktif</div><h3>{filtered_df["stasiun"].nunique()}</h3>', unsafe_allow_html=True)
with right:
    st.markdown(
        f'<div class="small-muted">Periode aktif</div><h3>{filtered_df["tanggal"].min().date()} s.d. {filtered_df["tanggal"].max().date()}</h3>',
        unsafe_allow_html=True,
    )


# =============================================================================
# TABS
# =============================================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "1. Overview Kualitas Udara",
        "2. Tren Temporal",
        "3. Antar Stasiun",
        "4. Pencemar Kritis",
        "5. Pola Musiman",
    ]
)


# =============================================================================
# TAB 1: OVERVIEW
# =============================================================================
with tab1:
    st.subheader("Overview Kualitas Udara Jakarta")

    avg_ispu = filtered_df["max"].mean()
    pct_unhealthy = filtered_df["is_tidak_sehat_plus"].mean() * 100
    dominant_pollutant = safe_mode(filtered_df["critical_display"])
    dominant_share = (
        filtered_df["critical_display"].value_counts(normalize=True).max() * 100
        if not filtered_df.empty
        else np.nan
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card(
            "Rata-rata ISPU Harian",
            f"{avg_ispu:.1f}",
            "Rerata nilai max pada data terfilter",
        )
    with c2:
        metric_card(
            "Hari Tidak Sehat+",
            format_pct(pct_unhealthy),
            "TIDAK SEHAT, SANGAT TIDAK SEHAT, atau BERBAHAYA",
        )
    with c3:
        metric_card(
            "Pencemar Dominan",
            dominant_pollutant,
            f"Muncul pada {dominant_share:.1f}% observasi" if pd.notna(dominant_share) else "-",
        )

    st.markdown("### Ringkasan Metrik per Stasiun")
    station_summary = (
        filtered_df.groupby("stasiun", as_index=False)
        .agg(
            rata_rata_ispu=("max", "mean"),
            median_ispu=("max", "median"),
            max_tertinggi=("max", "max"),
            persen_tidak_sehat_plus=("is_tidak_sehat_plus", lambda x: x.mean() * 100),
            pencemar_dominan=("critical_display", lambda x: safe_mode(x)),
            jumlah_observasi=("max", "size"),
        )
        .sort_values("rata_rata_ispu", ascending=False)
    )

    station_summary_display = station_summary.copy()
    for col in ["rata_rata_ispu", "median_ispu", "max_tertinggi", "persen_tidak_sehat_plus"]:
        station_summary_display[col] = station_summary_display[col].round(2)

    st.dataframe(
        station_summary_display,
        use_container_width=True,
        hide_index=True,
    )

    worst_station = station_summary.iloc[0]["stasiun"]
    best_station = station_summary.iloc[-1]["stasiun"]

    insight_box(
        "Interpretasi kondisi keseluruhan",
        (
            f"Pada periode dan stasiun yang dipilih, rata-rata ISPU berada di angka "
            f"<b>{avg_ispu:.1f}</b> dengan proporsi observasi kategori Tidak Sehat atau lebih buruk "
            f"sebesar <b>{pct_unhealthy:.1f}%</b>. Pencemar yang paling dominan adalah "
            f"<b>{dominant_pollutant}</b>. Untuk kebijakan lingkungan, perhatian utama perlu diarahkan "
            f"pada stasiun dengan rata-rata ISPU tertinggi, yaitu <b>{worst_station}</b>, sambil menjaga "
            f"praktik pemantauan pada stasiun yang relatif lebih baik seperti <b>{best_station}</b>."
        ),
    )


# =============================================================================
# TAB 2: TREN TEMPORAL
# =============================================================================
with tab2:
    st.subheader("Tren Temporal Kualitas Udara")

    granularity = st.radio(
        "Pilih granularitas tren",
        options=["Harian", "Bulanan", "Tahunan"],
        horizontal=True,
        index=1,
    )

    if granularity == "Harian":
        trend_df = (
            filtered_df.groupby("tanggal", as_index=False)
            .agg(rata_rata_ispu=("max", "mean"))
            .sort_values("tanggal")
        )
        x_col = "tanggal"
        x_title = "Tanggal"
    elif granularity == "Bulanan":
        trend_df = (
            filtered_df.groupby("tahun_bulan", as_index=False)
            .agg(rata_rata_ispu=("max", "mean"))
            .sort_values("tahun_bulan")
        )
        x_col = "tahun_bulan"
        x_title = "Bulan"
    else:
        trend_df = (
            filtered_df.groupby("tahun", as_index=False)
            .agg(rata_rata_ispu=("max", "mean"))
            .sort_values("tahun")
        )
        x_col = "tahun"
        x_title = "Tahun"

    fig_trend = px.line(
        trend_df,
        x=x_col,
        y="rata_rata_ispu",
        markers=True,
        title=f"Tren Nilai ISPU ({granularity})",
        labels={"rata_rata_ispu": "Rata-rata ISPU", x_col: x_title},
    )
    fig_trend.update_traces(line=dict(width=3, color="#F59E0B"), marker=dict(size=7))
    st.plotly_chart(style_plotly(fig_trend, height=470), use_container_width=True)

    first_value = trend_df["rata_rata_ispu"].iloc[0]
    last_value = trend_df["rata_rata_ispu"].iloc[-1]
    change = last_value - first_value
    change_pct = (change / first_value * 100) if first_value else 0

    worst_period = trend_df.loc[trend_df["rata_rata_ispu"].idxmax()]
    best_period = trend_df.loc[trend_df["rata_rata_ispu"].idxmin()]

    direction = "memburuk" if change > 0 else "membaik" if change < 0 else "relatif stabil"
    attention_period = worst_period[x_col]

    insight_box(
        "Tren temporal dan periode perhatian",
        (
            f"Dengan granularitas <b>{granularity.lower()}</b>, tren dari awal ke akhir periode terlihat "
            f"<b>{direction}</b> dengan perubahan sekitar <b>{change:+.1f}</b> poin "
            f"(<b>{change_pct:+.1f}%</b>). Periode dengan rata-rata ISPU tertinggi adalah "
            f"<b>{attention_period}</b> dengan nilai <b>{worst_period['rata_rata_ispu']:.1f}</b>, "
            f"sedangkan periode terbaik adalah <b>{best_period[x_col]}</b> dengan nilai "
            f"<b>{best_period['rata_rata_ispu']:.1f}</b>. Periode puncak perlu menjadi sasaran evaluasi "
            f"operasional, terutama untuk pengendalian sumber emisi dan kesiapan komunikasi risiko."
        ),
    )


# =============================================================================
# TAB 3: PERBANDINGAN ANTAR STASIUN
# =============================================================================
with tab3:
    st.subheader("Perbandingan Kualitas Udara Antar Stasiun")

    category_station = (
        filtered_df.groupby(["stasiun", "categori"], as_index=False)
        .size()
        .rename(columns={"size": "jumlah"})
    )
    category_station["categori"] = pd.Categorical(
        category_station["categori"],
        categories=CATEGORY_ORDER,
        ordered=True,
    )
    category_station = category_station.sort_values(["stasiun", "categori"])

    fig_cat_station = px.bar(
        category_station,
        x="stasiun",
        y="jumlah",
        color="categori",
        title="Distribusi Kategori ISPU per Stasiun",
        category_orders={"categori": CATEGORY_ORDER},
        color_discrete_map=CATEGORY_COLORS,
        labels={"jumlah": "Jumlah Observasi", "stasiun": "Stasiun", "categori": "Kategori"},
    )
    fig_cat_station.update_layout(barmode="stack")
    st.plotly_chart(style_plotly(fig_cat_station, height=470), use_container_width=True)

    avg_station = (
        filtered_df.groupby("stasiun", as_index=False)
        .agg(rata_rata_ispu=("max", "mean"))
        .sort_values("rata_rata_ispu", ascending=False)
    )
    fig_avg_station = px.bar(
        avg_station,
        x="stasiun",
        y="rata_rata_ispu",
        title="Rata-rata Nilai ISPU per Stasiun",
        labels={"rata_rata_ispu": "Rata-rata ISPU", "stasiun": "Stasiun"},
        text=avg_station["rata_rata_ispu"].round(1),
    )
    fig_avg_station.update_traces(marker_color="#F59E0B", textposition="outside")
    st.plotly_chart(style_plotly(fig_avg_station, height=430), use_container_width=True)

    worst_station = avg_station.iloc[0]
    best_station = avg_station.iloc[-1]

    unhealthy_by_station = (
        filtered_df.groupby("stasiun", as_index=False)
        .agg(persen_tidak_sehat_plus=("is_tidak_sehat_plus", lambda x: x.mean() * 100))
        .sort_values("persen_tidak_sehat_plus", ascending=False)
    )
    highest_risk_station = unhealthy_by_station.iloc[0]

    insight_box(
        "Prioritas spasial kebijakan",
        (
            f"Stasiun dengan rata-rata ISPU tertinggi adalah <b>{worst_station['stasiun']}</b> "
            f"({worst_station['rata_rata_ispu']:.1f}), sedangkan yang relatif terbaik adalah "
            f"<b>{best_station['stasiun']}</b> ({best_station['rata_rata_ispu']:.1f}). "
            f"Dari sisi proporsi kategori Tidak Sehat atau lebih buruk, titik risiko tertinggi berada pada "
            f"<b>{highest_risk_station['stasiun']}</b> "
            f"({highest_risk_station['persen_tidak_sehat_plus']:.1f}%). Implikasinya, intervensi pengendalian "
            f"polusi sebaiknya diprioritaskan pada stasiun berisiko tinggi melalui investigasi sumber emisi, "
            f"penguatan pengawasan, dan kampanye pengurangan aktivitas penyumbang polutan pada periode puncak."
        ),
    )


# =============================================================================
# TAB 4: ANALISIS PARAMETER PENCEMAR KRITIS
# =============================================================================
with tab4:
    st.subheader("Analisis Parameter Pencemar Kritis")

    critical_count = (
        filtered_df["critical_display"]
        .value_counts()
        .reset_index()
    )
    critical_count.columns = ["critical", "jumlah"]
    critical_count["persentase"] = critical_count["jumlah"] / critical_count["jumlah"].sum() * 100

    col_a, col_b = st.columns([1, 1])
    with col_a:
        fig_critical_bar = px.bar(
            critical_count,
            x="critical",
            y="jumlah",
            title="Distribusi Pencemar Kritis",
            text=critical_count["persentase"].round(1).astype(str) + "%",
            labels={"critical": "Parameter", "jumlah": "Jumlah Kemunculan"},
            color="critical",
            color_discrete_map={k.replace("PM25", "PM2.5"): v for k, v in CRITICAL_COLORS.items()},
        )
        fig_critical_bar.update_traces(textposition="outside")
        st.plotly_chart(style_plotly(fig_critical_bar, height=430), use_container_width=True)

    with col_b:
        fig_critical_pie = px.pie(
            critical_count,
            names="critical",
            values="jumlah",
            title="Komposisi Pencemar Kritis",
            hole=0.55,
            color="critical",
            color_discrete_map={k.replace("PM25", "PM2.5"): v for k, v in CRITICAL_COLORS.items()},
        )
        fig_critical_pie.update_traces(textinfo="percent+label")
        st.plotly_chart(style_plotly(fig_critical_pie, height=430), use_container_width=True)

    critical_trend = (
        filtered_df.groupby(["tahun_bulan", "critical_display"], as_index=False)
        .size()
        .rename(columns={"size": "jumlah"})
        .sort_values("tahun_bulan")
    )
    fig_critical_trend = px.line(
        critical_trend,
        x="tahun_bulan",
        y="jumlah",
        color="critical_display",
        markers=True,
        title="Tren Kemunculan Pencemar Kritis dari Waktu ke Waktu",
        labels={
            "tahun_bulan": "Bulan",
            "jumlah": "Jumlah Kemunculan",
            "critical_display": "Pencemar",
        },
        color_discrete_map={k.replace("PM25", "PM2.5"): v for k, v in CRITICAL_COLORS.items()},
    )
    fig_critical_trend.update_traces(line=dict(width=2.5))
    st.plotly_chart(style_plotly(fig_critical_trend, height=470), use_container_width=True)

    critical_station = (
        filtered_df.groupby(["stasiun", "critical_display"], as_index=False)
        .size()
        .rename(columns={"size": "jumlah"})
    )
    station_top_pollutant = (
        critical_station.sort_values(["stasiun", "jumlah"], ascending=[True, False])
        .groupby("stasiun")
        .head(1)
    )

    dominant_pollutant = critical_count.iloc[0]["critical"]
    dominant_pct = critical_count.iloc[0]["persentase"]

    station_pattern = "; ".join(
        [
            f"{row['stasiun']}: {row['critical_display']}"
            for _, row in station_top_pollutant.iterrows()
        ]
    )

    insight_box(
        "Karakteristik pencemar dominan",
        (
            f"Parameter yang paling dominan sebagai pencemar kritis adalah <b>{dominant_pollutant}</b> "
            f"dengan proporsi <b>{dominant_pct:.1f}%</b> dari observasi terfilter. Pola dominan per stasiun adalah: "
            f"<b>{station_pattern}</b>. Jika dominasi pencemar berbeda antar stasiun, maka program pengurangan emisi "
            f"perlu disesuaikan dengan karakteristik lokal, misalnya pengendalian debu/partikulat untuk PM, "
            f"pengelolaan emisi transportasi, serta evaluasi sumber ozon prekursor pada periode tertentu."
        ),
    )


# =============================================================================
# TAB 5: POLA MUSIMAN
# =============================================================================
with tab5:
    st.subheader("Pola Musiman Kualitas Udara")

    heatmap_df = (
        filtered_df.groupby(["stasiun", "bulan"], as_index=False)
        .agg(rata_rata_ispu=("max", "mean"))
    )
    heatmap_df["nama_bulan"] = heatmap_df["bulan"].map(MONTH_MAP)

    fig_heatmap = px.density_heatmap(
        heatmap_df,
        x="nama_bulan",
        y="stasiun",
        z="rata_rata_ispu",
        title="Heatmap Rata-rata ISPU berdasarkan Bulan dan Stasiun",
        category_orders={"nama_bulan": list(MONTH_MAP.values())},
        color_continuous_scale=[
            [0.0, "#22C55E"],
            [0.35, "#F59E0B"],
            [0.70, "#EF4444"],
            [1.0, "#7F1D1D"],
        ],
        labels={"nama_bulan": "Bulan", "stasiun": "Stasiun", "rata_rata_ispu": "Rata-rata ISPU"},
    )
    st.plotly_chart(style_plotly(fig_heatmap, height=520), use_container_width=True)

    month_summary = (
        filtered_df.groupby(["bulan", "nama_bulan"], as_index=False)
        .agg(rata_rata_ispu=("max", "mean"))
        .sort_values("bulan")
    )
    fig_month = px.bar(
        month_summary,
        x="nama_bulan",
        y="rata_rata_ispu",
        title="Rata-rata ISPU per Bulan",
        category_orders={"nama_bulan": list(MONTH_MAP.values())},
        labels={"nama_bulan": "Bulan", "rata_rata_ispu": "Rata-rata ISPU"},
        text=month_summary["rata_rata_ispu"].round(1),
    )
    fig_month.update_traces(marker_color="#F59E0B", textposition="outside")
    st.plotly_chart(style_plotly(fig_month, height=400), use_container_width=True)

    season_summary = (
        filtered_df.groupby("musim", as_index=False)
        .agg(rata_rata_ispu=("max", "mean"), jumlah_observasi=("max", "size"))
        .sort_values("rata_rata_ispu", ascending=False)
    )

    worst_month = month_summary.loc[month_summary["rata_rata_ispu"].idxmax()]
    best_month = month_summary.loc[month_summary["rata_rata_ispu"].idxmin()]
    worst_season = season_summary.iloc[0]

    insight_box(
        "Pola musim dan rekomendasi operasional",
        (
            f"Bulan dengan rata-rata ISPU terburuk pada data terfilter adalah <b>{worst_month['nama_bulan']}</b> "
            f"({worst_month['rata_rata_ispu']:.1f}), sedangkan bulan terbaik adalah "
            f"<b>{best_month['nama_bulan']}</b> ({best_month['rata_rata_ispu']:.1f}). "
            f"Secara pengelompokan musim, periode dengan rata-rata ISPU tertinggi adalah "
            f"<b>{worst_season['musim']}</b>. Untuk antisipasi operasional, Dinas dapat memperkuat pemantauan, "
            f"komunikasi risiko, inspeksi sumber emisi, dan kebijakan pengurangan aktivitas penyumbang polusi "
            f"menjelang bulan atau musim yang konsisten menunjukkan kualitas udara lebih buruk."
        ),
    )

    st.markdown("### Ringkasan Musim")
    st.dataframe(season_summary.round(2), use_container_width=True, hide_index=True)
