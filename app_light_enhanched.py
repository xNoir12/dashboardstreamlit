
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="Dashboard ISPU Jakarta V5",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =============================================================================
# CUSTOM CSS - EXECUTIVE LIGHT MODE
# =============================================================================
st.markdown(
    """
    <style>
        :root {
            --bg-main: #F6F1E8;
            --bg-soft: #FBF8F1;
            --panel: #FFFFFF;
            --text-main: #17212B;
            --text-muted: #64748B;
            --text-soft: #475569;
            --accent: #B45309;
            --teal: #0F766E;
            --danger: #DC2626;
            --success: #15803D;
            --line: rgba(23, 33, 43, 0.11);
            --shadow: 0 18px 50px rgba(28, 25, 23, 0.10);
            --shadow-soft: 0 10px 24px rgba(28, 25, 23, 0.08);
        }

        html, body, .stApp {
            background:
                radial-gradient(circle at top left, rgba(180, 83, 9, 0.12), transparent 26%),
                radial-gradient(circle at top right, rgba(15, 118, 110, 0.10), transparent 24%),
                linear-gradient(180deg, #F6F1E8 0%, #FBF8F1 42%, #F6F1E8 100%) !important;
            color: var(--text-main) !important;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #FFFFFF 0%, #FFF7E8 100%) !important;
            border-right: 1px solid var(--line);
            box-shadow: 8px 0 28px rgba(28, 25, 23, 0.06);
        }

        [data-testid="stSidebar"] * { color: var(--text-main); }

        .block-container {
            padding-top: 1.25rem;
            padding-bottom: 2.4rem;
            max-width: 1500px;
        }

        h1, h2, h3 {
            color: var(--text-main) !important;
            letter-spacing: -0.035em;
        }

        .hero {
            position: relative;
            overflow: hidden;
            padding: 1.45rem 1.55rem;
            border-radius: 28px;
            background:
                linear-gradient(135deg, rgba(255,255,255,0.96), rgba(255,247,232,0.96)),
                linear-gradient(90deg, rgba(180,83,9,0.18), rgba(15,118,110,0.12));
            border: 1px solid rgba(180, 83, 9, 0.18);
            box-shadow: var(--shadow);
            margin-bottom: 1.2rem;
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
        }

        .hero-subtitle {
            position: relative;
            z-index: 1;
            color: var(--text-soft);
            font-size: 0.98rem;
            max-width: 1120px;
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
            background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(255,247,232,0.84));
            border: 1px solid rgba(23, 33, 43, 0.10);
            border-radius: 24px;
            padding: 1.05rem 1.12rem;
            box-shadow: var(--shadow-soft);
            min-height: 145px;
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

        .metric-severity {
            display: inline-flex;
            margin-top: 0.68rem;
            padding: 0.28rem 0.58rem;
            border-radius: 999px;
            font-size: 0.74rem;
            font-weight: 850;
            letter-spacing: 0.02em;
            border: 1px solid rgba(23,33,43,0.10);
            background: rgba(255,255,255,0.82);
        }

        .insight-box {
            border-left: 6px solid var(--accent);
            background: linear-gradient(90deg, rgba(180, 83, 9, 0.13), rgba(255,255,255,0.92)), #FFFFFF;
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

        .threshold-note {
            display: inline-flex;
            flex-wrap: wrap;
            gap: 0.45rem;
            align-items: center;
            margin: 0.35rem 0 0.65rem 0;
            color: #475569;
            font-size: 0.83rem;
        }

        .threshold-pill {
            display: inline-flex;
            padding: 0.28rem 0.55rem;
            border-radius: 999px;
            background: #FFFFFF;
            border: 1px solid rgba(23,33,43,0.10);
            box-shadow: 0 6px 14px rgba(28,25,23,0.06);
            font-weight: 700;
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

        div[data-testid="stDataFrame"] {
            border: 1px solid rgba(23,33,43,0.10);
            border-radius: 16px;
            box-shadow: var(--shadow-soft);
            overflow: hidden;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# =============================================================================
# CONSTANTS
# =============================================================================
DATA_FILE = "D00_ispu_jakarta_final_sot_v5_drop_over50.csv"

CATEGORY_ORDER = ["BAIK", "SEDANG", "TIDAK SEHAT", "SANGAT TIDAK SEHAT", "BERBAHAYA"]
CATEGORY_COLORS = {
    "BAIK": "#15803D",
    "SEDANG": "#D97706",
    "TIDAK SEHAT": "#DC2626",
    "SANGAT TIDAK SEHAT": "#7C3AED",
    "BERBAHAYA": "#7F1D1D",
}
CRITICAL_COLORS = {
    "PM10": "#EA580C",
    "SO2": "#CA8A04",
    "CO": "#0F766E",
    "O3": "#7C3AED",
    "NO2": "#0284C7",
}
MONTH_ABBR = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "Mei", 6: "Jun",
    7: "Jul", 8: "Agu", 9: "Sep", 10: "Okt", 11: "Nov", 12: "Des",
}
BAIK_THRESHOLD = 50
TIDAK_SEHAT_THRESHOLD = 100


# =============================================================================
# DATA
# =============================================================================
@st.cache_data(show_spinner="Memuat dataset final ISPU Jakarta V5...")
def load_data(path: str = DATA_FILE):
    candidate_paths = [
        Path(path),
        Path(__file__).parent / path if "__file__" in globals() else Path(path),
        Path("/mnt/data") / path,
    ]
    data_path = next((p for p in candidate_paths if p.exists()), None)
    if data_path is None:
        raise FileNotFoundError(f"Dataset '{path}' tidak ditemukan. Letakkan CSV di folder yang sama dengan app.py.")

    df = pd.read_csv(data_path)
    df["tanggal"] = pd.to_datetime(df["tanggal"], errors="coerce")
    pollutant_cols = [c for c in ["pm10", "pm25", "so2", "co", "o3", "no2"] if c in df.columns]

    for col in pollutant_cols + ["max"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["tanggal", "stasiun", "max", "critical", "categori"]).copy()
    df["tahun"] = df["tanggal"].dt.year
    df["bulan"] = df["tanggal"].dt.month
    df["bulan_abbr"] = df["bulan"].map(MONTH_ABBR)
    df["tahun_bulan"] = df["tanggal"].dt.to_period("M").astype(str)
    df["stasiun_kode"] = df["stasiun"].str.extract(r"(DKI\d)", expand=False).fillna(df["stasiun"])
    df["critical_display"] = df["critical"]
    df["is_tidak_sehat_plus"] = df["categori"].isin(["TIDAK SEHAT", "SANGAT TIDAK SEHAT", "BERBAHAYA"])

    def musim(bulan: int) -> str:
        if bulan in [11, 12, 1, 2, 3]:
            return "Musim Hujan"
        if bulan in [6, 7, 8, 9]:
            return "Musim Kemarau"
        if bulan in [4, 5]:
            return "Peralihan I"
        return "Peralihan II"

    df["musim"] = df["bulan"].apply(musim)
    return df, pollutant_cols


def apply_global_filters(df, stations, date_range):
    out = df.copy()
    if stations:
        out = out[out["stasiun"].isin(stations)]
    if len(date_range) == 2:
        start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
        out = out[(out["tanggal"] >= start) & (out["tanggal"] <= end)]
    return out


# =============================================================================
# UI HELPERS
# =============================================================================
def safe_mode(series, default="-"):
    s = series.dropna()
    if s.empty:
        return default
    return str(s.mode().iloc[0])


def format_pct(value):
    return "-" if pd.isna(value) else f"{value:.1f}%"


def metric_card(label, value, note="", value_color="#17212B", severity_label=None, severity_color=None):
    severity_html = ""
    if severity_label:
        pill_color = severity_color or value_color
        severity_html = (
            f'<div class="metric-severity" '
            f'style="color:{pill_color}; border-color:{pill_color}55; background:{pill_color}12;">'
            f'{severity_label}</div>'
        )

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value" style="color:{value_color};">{value}</div>
            <div class="metric-note">{note}</div>
            {severity_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def ispu_category_and_color(value):
    """Warna KPI mengikuti kelas ISPU agar stakeholder cepat menangkap kegawatan."""
    if pd.isna(value):
        return "Tidak tersedia", "#64748B"
    if value <= 50:
        return "BAIK", "#15803D"
    if value <= 100:
        return "SEDANG", "#D97706"
    if value <= 199:
        return "TIDAK SEHAT", "#DC2626"
    if value <= 299:
        return "SANGAT TIDAK SEHAT", "#7C3AED"
    return "BERBAHAYA", "#7F1D1D"


def risk_rate_label_and_color(value):
    """Warna KPI persentase risiko dibuat sederhana untuk kebutuhan komunikasi stakeholder."""
    if pd.isna(value):
        return "Tidak tersedia", "#64748B"
    if value < 10:
        return "RISIKO RENDAH", "#15803D"
    if value < 20:
        return "PERLU DIPANTAU", "#D97706"
    if value < 35:
        return "RISIKO TINGGI", "#DC2626"
    return "RISIKO SANGAT TINGGI", "#7C3AED"


def pollutant_color(pollutant):
    return CRITICAL_COLORS.get(str(pollutant).upper(), "#334155")


def insight_box(title, body, icon="💡"):
    st.markdown(
        f"""
        <div class="insight-box">
            <div class="insight-title">{icon} {title}</div>
            <div class="insight-text">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def threshold_note():
    st.markdown(
        """
        <div class="threshold-note">
            <span class="threshold-pill">Garis hijau: ISPU 50 = batas kategori BAIK</span>
            <span class="threshold-pill">Garis merah: ISPU 100 = mulai Tidak Sehat+</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def category_legend_note():
    st.markdown(
        """
        <div class="threshold-note">
            <span class="threshold-pill">BAIK: 0–50</span>
            <span class="threshold-pill">SEDANG: 51–100</span>
            <span class="threshold-pill">TIDAK SEHAT+: >100</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def critical_legend_note(pollutant_cols):
    pollutant_text = ", ".join([c.upper() for c in pollutant_cols])
    st.markdown(
        f"""
        <div class="threshold-note">
            <span class="threshold-pill">Pencemar kritis = parameter dengan nilai ISPU tertinggi pada baris yang sama</span>
            <span class="threshold-pill">Polutan aktif V5: {pollutant_text}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def season_mapping_note():
    st.markdown(
        """
        <div class="threshold-note">
            <span class="threshold-pill">Musim Hujan: Nov, Des, Jan, Feb, Mar</span>
            <span class="threshold-pill">Peralihan I: Apr, Mei</span>
            <span class="threshold-pill">Musim Kemarau: Jun, Jul, Agu, Sep</span>
            <span class="threshold-pill">Peralihan II: Okt</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def style_plotly(fig, height=430):
    fig.update_layout(
        template="plotly_white",
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFFFF",
        font=dict(color="#17212B", family="Inter, Segoe UI, Arial"),
        title=dict(font=dict(size=18, color="#17212B"), x=0.02),
        margin=dict(l=35, r=25, t=65, b=35),
        legend=dict(bgcolor="rgba(255,255,255,0)", font=dict(size=11, color="#334155")),
    )
    fig.update_xaxes(gridcolor="rgba(23,33,43,0.08)", linecolor="rgba(23,33,43,0.18)")
    fig.update_yaxes(gridcolor="rgba(23,33,43,0.08)", linecolor="rgba(23,33,43,0.18)")
    return fig


def add_ispu_threshold_lines(fig, y_max_hint=None):
    fig.add_hline(
        y=BAIK_THRESHOLD,
        line_dash="dot",
        line_color="#15803D",
        line_width=2,
        annotation_text="Batas BAIK (50)",
        annotation_position="top left",
        annotation_font=dict(color="#15803D", size=11),
    )
    fig.add_hline(
        y=TIDAK_SEHAT_THRESHOLD,
        line_dash="dash",
        line_color="#DC2626",
        line_width=2.5,
        annotation_text="Mulai Tidak Sehat+ (100)",
        annotation_position="top left",
        annotation_font=dict(color="#DC2626", size=11),
    )
    if y_max_hint is not None:
        fig.update_yaxes(range=[0, max(120, y_max_hint * 1.15)])
    return fig


def add_unhealthy_rate_reference(fig, target=20):
    """Adds a reference line for risk proportion charts."""
    fig.add_hline(
        y=target,
        line_dash="dot",
        line_color="#DC2626",
        line_width=2,
        annotation_text=f"Referensi risiko {target}%",
        annotation_position="top left",
        annotation_font=dict(color="#DC2626", size=11),
    )
    return fig


def period_trend(df, granularity):
    if granularity == "Harian":
        return df.groupby("tanggal", as_index=False).agg(rata_rata_ispu=("max", "mean")).sort_values("tanggal"), "tanggal", "Tanggal"
    if granularity == "Bulanan":
        return df.groupby("tahun_bulan", as_index=False).agg(rata_rata_ispu=("max", "mean")).sort_values("tahun_bulan"), "tahun_bulan", "Bulan"
    return df.groupby("tahun", as_index=False).agg(rata_rata_ispu=("max", "mean")).sort_values("tahun"), "tahun", "Tahun"


def station_period_trend(df, granularity):
    if granularity == "Harian":
        return df.groupby(["tanggal", "stasiun"], as_index=False).agg(rata_rata_ispu=("max", "mean")).sort_values("tanggal"), "tanggal"
    if granularity == "Bulanan":
        return df.groupby(["tahun_bulan", "stasiun"], as_index=False).agg(rata_rata_ispu=("max", "mean")).sort_values("tahun_bulan"), "tahun_bulan"
    return df.groupby(["tahun", "stasiun"], as_index=False).agg(rata_rata_ispu=("max", "mean")).sort_values("tahun"), "tahun"


# =============================================================================
# LOAD DATA
# =============================================================================
try:
    df, pollutant_cols = load_data(DATA_FILE)
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
            Dashboard V5 untuk analisis ISPU Jakarta. Dashboard ini sudah mengikuti feedback asesor dan menambahkan mode chart kategori:
            kolom dengan missing value lebih dari 50% tidak diimputasi, sehingga PM2.5 di-drop dari source of truth.
            Visualisasi ditingkatkan agar tidak hanya menampilkan data, tetapi juga informasi melalui garis ambang ISPU.
        </div>
        <span class="source-pill">Source of truth: D00_ispu_jakarta_final_sot_v5_drop_over50.csv</span>
    </div>
    """,
    unsafe_allow_html=True,
)


# =============================================================================
# SIDEBAR
# =============================================================================
with st.sidebar:
    st.markdown("## Filter Global")
    all_stations = sorted(df["stasiun"].dropna().unique())
    selected_stations = st.multiselect("Stasiun SPKU", all_stations, default=all_stations)
    selected_date_range = st.date_input(
        "Rentang Waktu",
        value=(df["tanggal"].min().date(), df["tanggal"].max().date()),
        min_value=df["tanggal"].min().date(),
        max_value=df["tanggal"].max().date(),
    )

    st.markdown("---")
    st.markdown("### Catatan Dataset V5")
    st.caption("PM2.5 di-drop karena missing value >50%.")
    st.caption(f"Polutan aktif final: {', '.join([c.upper() for c in pollutant_cols])}.")
    st.caption("Ambang informasi: ISPU 50 = batas BAIK; ISPU 100 = mulai Tidak Sehat+.")

filtered_df = apply_global_filters(df, selected_stations, selected_date_range)

if filtered_df.empty:
    st.warning("Tidak ada data pada kombinasi filter yang dipilih.")
    st.stop()


# =============================================================================
# FILTER SUMMARY
# =============================================================================
left, mid, right = st.columns([1.1, 1.1, 1.8])
with left:
    st.markdown(f'<div class="small-muted">Observasi terfilter</div><h3>{len(filtered_df):,}</h3>', unsafe_allow_html=True)
with mid:
    st.markdown(f'<div class="small-muted">SPKU aktif</div><h3>{filtered_df["stasiun"].nunique()}</h3>', unsafe_allow_html=True)
with right:
    st.markdown(
        f'<div class="small-muted">Periode aktif</div><h3>{filtered_df["tanggal"].min().date()} s.d. {filtered_df["tanggal"].max().date()}</h3>',
        unsafe_allow_html=True,
    )


# =============================================================================
# TABS
# =============================================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "1. Overview Kualitas Udara",
    "2. Tren Temporal",
    "3. Antar Stasiun",
    "4. Pencemar Kritis",
    "5. Pola Musiman",
])


# =============================================================================
# TAB 1 — OVERVIEW
# =============================================================================
with tab1:
    st.subheader("Dashboard 1 — Overview Kualitas Udara Jakarta")
    st.caption("Membaca kondisi umum kualitas udara berdasarkan KPI utama, risiko Tidak Sehat+, dan ringkasan stasiun. Warna angka KPI mengikuti kelas/kegawatan agar informasi cepat terbaca.")

    avg_ispu = filtered_df["max"].mean()
    pct_unhealthy = filtered_df["is_tidak_sehat_plus"].mean() * 100
    dominant_pollutant = safe_mode(filtered_df["critical_display"])
    dominant_share = filtered_df["critical_display"].value_counts(normalize=True).max() * 100

    category_legend_note()
    critical_legend_note(pollutant_cols)

    avg_category, avg_color = ispu_category_and_color(avg_ispu)
    risk_label, risk_color = risk_rate_label_and_color(pct_unhealthy)
    dominant_color = pollutant_color(dominant_pollutant)

    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card(
            "Rata-rata ISPU Harian",
            f"{avg_ispu:.1f}",
            "Rerata kolom max pada data terfilter",
            value_color=avg_color,
            severity_label=f"Kelas: {avg_category}",
            severity_color=avg_color,
        )
    with c2:
        metric_card(
            "Observasi Tidak Sehat+",
            format_pct(pct_unhealthy),
            "TIDAK SEHAT, SANGAT TIDAK SEHAT, atau BERBAHAYA",
            value_color=risk_color,
            severity_label=risk_label,
            severity_color=risk_color,
        )
    with c3:
        metric_card(
            "Pencemar Dominan",
            dominant_pollutant,
            f"Muncul pada {dominant_share:.1f}% observasi",
            value_color=dominant_color,
            severity_label="Pencemar paling sering menjadi critical",
            severity_color=dominant_color,
        )

    station_summary = (
        filtered_df.groupby("stasiun", as_index=False)
        .agg(
            rata_rata_ispu=("max", "mean"),
            median_ispu=("max", "median"),
            max_tertinggi=("max", "max"),
            persen_tidak_sehat_plus=("is_tidak_sehat_plus", lambda x: x.mean() * 100),
            pencemar_dominan=("critical_display", safe_mode),
            jumlah_observasi=("max", "size"),
        )
        .sort_values("rata_rata_ispu", ascending=False)
    )

    st.markdown("#### Ringkasan Metrik per Stasiun")
    st.dataframe(station_summary.round(2), use_container_width=True, hide_index=True)

    threshold_note()
    fig_station_avg = px.bar(
        station_summary,
        x="stasiun",
        y="rata_rata_ispu",
        title="Rata-rata ISPU per Stasiun dengan Ambang Kategori",
        text=station_summary["rata_rata_ispu"].round(1),
        labels={"rata_rata_ispu": "Rata-rata ISPU", "stasiun": "Stasiun"},
    )
    fig_station_avg.update_traces(marker_color="#B45309", textposition="outside")
    fig_station_avg = add_ispu_threshold_lines(fig_station_avg, station_summary["rata_rata_ispu"].max())
    st.plotly_chart(style_plotly(fig_station_avg, height=430), use_container_width=True)

    worst_station = station_summary.iloc[0]["stasiun"]
    best_station = station_summary.iloc[-1]["stasiun"]
    insight_box(
        "Analisis & insight overview",
        (
            f"Rata-rata ISPU pada filter aktif adalah <b>{avg_ispu:.1f}</b>. "
            f"Nilai ini perlu dibaca terhadap ambang 50 dan 100. Di atas 50, kondisi tidak lagi berada pada kategori BAIK; "
            f"di atas 100, observasi mulai masuk Tidak Sehat+. Proporsi Tidak Sehat+ adalah "
            f"<b>{pct_unhealthy:.1f}%</b>, dengan pencemar dominan <b>{dominant_pollutant}</b>. "
            f"Prioritas perhatian diarahkan ke <b>{worst_station}</b>, sedangkan <b>{best_station}</b> menjadi pembanding performa relatif terbaik."
        ),
        icon="✅",
    )


# =============================================================================
# TAB 2 — TEMPORAL
# =============================================================================
with tab2:
    st.subheader("Dashboard 2 — Tren Temporal Kualitas Udara")
    st.caption("Membaca arah perubahan kualitas udara dari waktu ke waktu dengan garis ambang interpretasi ISPU.")

    granularity = st.radio("Granularitas", ["Harian", "Bulanan", "Tahunan"], horizontal=True, index=1)
    compare_mode = st.radio("Mode perbandingan", ["Rata-rata Jakarta", "Per Stasiun"], horizontal=True, index=1)

    threshold_note()

    if compare_mode == "Rata-rata Jakarta":
        trend_df, x_col, x_title = period_trend(filtered_df, granularity)
        fig_trend = px.line(
            trend_df,
            x=x_col,
            y="rata_rata_ispu",
            markers=True,
            title=f"Tren Rata-rata ISPU Jakarta ({granularity})",
            labels={x_col: x_title, "rata_rata_ispu": "Rata-rata ISPU"},
        )
        fig_trend.update_traces(line=dict(width=3, color="#B45309"), marker=dict(size=7))
        y_hint = trend_df["rata_rata_ispu"].max()
    else:
        trend_df, x_col = station_period_trend(filtered_df, granularity)
        fig_trend = px.line(
            trend_df,
            x=x_col,
            y="rata_rata_ispu",
            color="stasiun",
            markers=True,
            title=f"Perbandingan Tren ISPU Antar Stasiun ({granularity})",
            labels={x_col: granularity, "rata_rata_ispu": "Rata-rata ISPU", "stasiun": "Stasiun"},
        )
        fig_trend.update_traces(line=dict(width=2.5), marker=dict(size=6))
        y_hint = trend_df["rata_rata_ispu"].max()

    fig_trend = add_ispu_threshold_lines(fig_trend, y_hint)
    st.plotly_chart(style_plotly(fig_trend, height=500), use_container_width=True)

    trend_overall, overall_x_col, _ = period_trend(filtered_df, granularity)
    trend_overall["perubahan_vs_periode_sebelumnya"] = trend_overall["rata_rata_ispu"].diff()
    significant_change = trend_overall.dropna(subset=["perubahan_vs_periode_sebelumnya"]).copy()

    col_a, col_b = st.columns([1.05, 1])
    with col_a:
        if not significant_change.empty:
            fig_change = px.bar(
                significant_change,
                x=overall_x_col,
                y="perubahan_vs_periode_sebelumnya",
                title="Perubahan ISPU vs Periode Sebelumnya",
                labels={overall_x_col: "Periode", "perubahan_vs_periode_sebelumnya": "Perubahan ISPU"},
            )
            fig_change.update_traces(
                marker_color=np.where(significant_change["perubahan_vs_periode_sebelumnya"] >= 0, "#DC2626", "#15803D")
            )
            st.plotly_chart(style_plotly(fig_change, height=360), use_container_width=True)

    with col_b:
        top_periods = trend_overall.nlargest(8, "rata_rata_ispu").copy()
        top_periods["rata_rata_ispu"] = top_periods["rata_rata_ispu"].round(2)
        st.markdown("#### Periode dengan ISPU Tertinggi")
        st.dataframe(top_periods, use_container_width=True, hide_index=True)

    first_value = trend_overall["rata_rata_ispu"].iloc[0]
    last_value = trend_overall["rata_rata_ispu"].iloc[-1]
    change = last_value - first_value
    direction = "memburuk" if change > 0 else "membaik" if change < 0 else "relatif stabil"
    worst_period = trend_overall.loc[trend_overall["rata_rata_ispu"].idxmax()]

    insight_box(
        "Analisis & insight tren temporal",
        (
            f"Tren pada granularitas <b>{granularity.lower()}</b> terlihat <b>{direction}</b> dari awal ke akhir periode "
            f"dengan perubahan <b>{change:+.1f}</b> poin. Periode terburuk adalah <b>{worst_period[overall_x_col]}</b> "
            f"({worst_period['rata_rata_ispu']:.1f}). Garis ambang 100 membantu mengidentifikasi periode ketika rata-rata ISPU "
            f"mulai memasuki zona Tidak Sehat+."
        ),
        icon="📈",
    )


# =============================================================================
# TAB 3 — STATION COMPARISON
# =============================================================================
with tab3:
    st.subheader("Dashboard 3 — Perbandingan Kualitas Udara Antar Stasiun")
    st.caption("Membandingkan beban kualitas udara antar SPKU dari distribusi kategori, rata-rata ISPU, dan persentase risiko.")
    category_legend_note()

    category_station = (
        filtered_df.groupby(["stasiun", "categori"], as_index=False)
        .size()
        .rename(columns={"size": "jumlah"})
    )
    category_station["categori"] = pd.Categorical(category_station["categori"], categories=CATEGORY_ORDER, ordered=True)
    category_station = category_station.sort_values(["stasiun", "categori"])

    # Mode visualisasi ditambahkan agar chart bisa dibaca dari dua sudut:
    # 1) jumlah absolut observasi, dan 2) komposisi/persentase kategori.
    category_viz_mode = st.radio(
        "Mode visualisasi kategori",
        [
            "Stacked jumlah observasi",
            "Disandingkan antar kategori",
            "Komposisi 100% per stasiun",
        ],
        horizontal=True,
        help=(
            "Stacked menunjukkan total jumlah observasi; Disandingkan memudahkan perbandingan kategori antar stasiun; "
            "Komposisi 100% menormalkan setiap stasiun menjadi 100% agar proporsi kategorinya mudah dibandingkan."
        ),
    )

    if category_viz_mode == "Komposisi 100% per stasiun":
        category_station_plot = category_station.copy()
        category_station_plot["total_stasiun"] = category_station_plot.groupby("stasiun")["jumlah"].transform("sum")
        category_station_plot["persentase"] = (
            category_station_plot["jumlah"] / category_station_plot["total_stasiun"] * 100
        )

        fig_cat_station = px.bar(
            category_station_plot,
            x="stasiun",
            y="persentase",
            color="categori",
            title="Komposisi Kategori ISPU per Stasiun (100%)",
            color_discrete_map=CATEGORY_COLORS,
            category_orders={"categori": CATEGORY_ORDER},
            labels={"persentase": "Komposisi (%)", "stasiun": "Stasiun", "categori": "Kategori"},
            text=category_station_plot["persentase"].round(1).astype(str) + "%",
            hover_data={"jumlah": True, "persentase": ":.2f", "total_stasiun": True},
        )
        fig_cat_station.update_layout(
            barmode="stack",
            yaxis=dict(range=[0, 100], ticksuffix="%"),
        )
        fig_cat_station.update_traces(textposition="inside", textfont_size=10)
        fig_cat_station.add_hline(
            y=20,
            line_dash="dot",
            line_color="#DC2626",
            line_width=2,
            annotation_text="Referensi komposisi 20%",
            annotation_position="top left",
            annotation_font=dict(color="#DC2626", size=11),
        )

    elif category_viz_mode == "Disandingkan antar kategori":
        fig_cat_station = px.bar(
            category_station,
            x="stasiun",
            y="jumlah",
            color="categori",
            title="Kategori ISPU per Stasiun — Mode Disandingkan",
            color_discrete_map=CATEGORY_COLORS,
            category_orders={"categori": CATEGORY_ORDER},
            labels={"jumlah": "Jumlah Observasi", "stasiun": "Stasiun", "categori": "Kategori"},
            text="jumlah",
        )
        fig_cat_station.update_layout(barmode="group")
        fig_cat_station.update_traces(textposition="outside")

    else:
        fig_cat_station = px.bar(
            category_station,
            x="stasiun",
            y="jumlah",
            color="categori",
            title="Distribusi Kategori ISPU per Stasiun — Stacked Jumlah Observasi",
            color_discrete_map=CATEGORY_COLORS,
            category_orders={"categori": CATEGORY_ORDER},
            labels={"jumlah": "Jumlah Observasi", "stasiun": "Stasiun", "categori": "Kategori"},
        )
        fig_cat_station.update_layout(barmode="stack")

    st.plotly_chart(style_plotly(fig_cat_station, height=500), use_container_width=True)

    if category_viz_mode == "Komposisi 100% per stasiun":
        insight_box(
            "Cara membaca chart komposisi",
            (
                "Mode komposisi 100% menormalkan setiap stasiun menjadi total 100%. "
                "Mode ini cocok untuk membandingkan proporsi kategori BAIK, SEDANG, dan Tidak Sehat+ antar stasiun, "
                "walaupun jumlah observasi masing-masing stasiun berbeda."
            ),
            icon="🧭",
        )
    elif category_viz_mode == "Disandingkan antar kategori":
        insight_box(
            "Cara membaca chart disandingkan",
            (
                "Mode disandingkan cocok untuk melihat kategori mana yang paling membedakan antar stasiun. "
                "Misalnya, kategori TIDAK SEHAT dapat dibandingkan langsung antar SPKU tanpa tertutup oleh total stacked."
            ),
            icon="🧭",
        )

    avg_station = (
        filtered_df.groupby("stasiun", as_index=False)
        .agg(
            rata_rata_ispu=("max", "mean"),
            median_ispu=("max", "median"),
            persentase_tidak_sehat_plus=("is_tidak_sehat_plus", lambda x: x.mean() * 100),
            jumlah_observasi=("max", "size"),
        )
        .sort_values("rata_rata_ispu", ascending=False)
    )

    col_avg, col_risk = st.columns([1, 1])
    with col_avg:
        threshold_note()
        fig_avg_station = px.bar(
            avg_station,
            x="stasiun",
            y="rata_rata_ispu",
            title="Rata-rata Nilai ISPU per Stasiun",
            labels={"rata_rata_ispu": "Rata-rata ISPU", "stasiun": "Stasiun"},
            text=avg_station["rata_rata_ispu"].round(1),
        )
        fig_avg_station.update_traces(marker_color="#B45309", textposition="outside")
        fig_avg_station = add_ispu_threshold_lines(fig_avg_station, avg_station["rata_rata_ispu"].max())
        st.plotly_chart(style_plotly(fig_avg_station, height=430), use_container_width=True)

    with col_risk:
        fig_risk_station = px.bar(
            avg_station.sort_values("persentase_tidak_sehat_plus", ascending=False),
            x="stasiun",
            y="persentase_tidak_sehat_plus",
            title="Persentase Tidak Sehat+ per Stasiun",
            labels={"persentase_tidak_sehat_plus": "% Tidak Sehat+", "stasiun": "Stasiun"},
            text=avg_station.sort_values("persentase_tidak_sehat_plus", ascending=False)["persentase_tidak_sehat_plus"].round(1).astype(str) + "%",
        )
        fig_risk_station.update_traces(marker_color="#DC2626", textposition="outside")
        fig_risk_station = add_unhealthy_rate_reference(fig_risk_station, target=20)
        fig_risk_station.update_yaxes(range=[0, max(25, avg_station["persentase_tidak_sehat_plus"].max() * 1.25)])
        st.plotly_chart(style_plotly(fig_risk_station, height=430), use_container_width=True)

    st.markdown("#### Ringkasan Komparatif SPKU")
    st.dataframe(avg_station.round(2), use_container_width=True, hide_index=True)

    worst_avg = avg_station.iloc[0]
    best_avg = avg_station.iloc[-1]
    worst_risk = avg_station.sort_values("persentase_tidak_sehat_plus", ascending=False).iloc[0]

    insight_box(
        "Analisis & insight antar stasiun",
        (
            f"Stasiun dengan rata-rata ISPU tertinggi adalah <b>{worst_avg['stasiun']}</b> "
            f"({worst_avg['rata_rata_ispu']:.1f}), sedangkan yang terendah adalah "
            f"<b>{best_avg['stasiun']}</b> ({best_avg['rata_rata_ispu']:.1f}). "
            f"Dari sisi proporsi risiko, <b>{worst_risk['stasiun']}</b> memiliki persentase Tidak Sehat+ tertinggi "
            f"({worst_risk['persentase_tidak_sehat_plus']:.1f}%)."
        ),
        icon="📍",
    )


# =============================================================================
# TAB 4 — CRITICAL POLLUTANT
# =============================================================================
with tab4:
    st.subheader("Dashboard 4 — Analisis Parameter Pencemar Kritis")
    st.caption("Membaca parameter yang paling sering menjadi pencemar dominan dari polutan aktif final.")
    critical_legend_note(pollutant_cols)

    critical_order = [c.upper() for c in pollutant_cols]
    critical_count = filtered_df["critical_display"].value_counts().reindex(critical_order).dropna().reset_index()
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
            color="critical",
            color_discrete_map=CRITICAL_COLORS,
            labels={"critical": "Parameter", "jumlah": "Jumlah Kemunculan"},
        )
        fig_critical_bar.update_traces(textposition="outside")
        st.plotly_chart(style_plotly(fig_critical_bar, height=410), use_container_width=True)

    with col_b:
        fig_critical_pie = px.pie(
            critical_count,
            names="critical",
            values="jumlah",
            title="Komposisi Parameter Pencemar Kritis",
            hole=0.55,
            color="critical",
            color_discrete_map=CRITICAL_COLORS,
        )
        fig_critical_pie.update_traces(textinfo="percent+label")
        st.plotly_chart(style_plotly(fig_critical_pie, height=410), use_container_width=True)

    critical_station = (
        filtered_df.groupby(["stasiun", "critical_display"], as_index=False)
        .size()
        .rename(columns={"size": "jumlah"})
    )

    critical_station["critical_display"] = pd.Categorical(
        critical_station["critical_display"],
        categories=[c.upper() for c in pollutant_cols],
        ordered=True,
    )
    critical_station = critical_station.sort_values(["stasiun", "critical_display"])

    critical_viz_mode = st.radio(
        "Mode visualisasi pencemar kritis antar stasiun",
        [
            "Stacked jumlah kemunculan",
            "Disandingkan antar pencemar",
            "Komposisi 100% per stasiun",
        ],
        horizontal=True,
        help=(
            "Stacked menunjukkan volume kemunculan pencemar kritis. "
            "Disandingkan memudahkan perbandingan satu pencemar antar SPKU. "
            "Komposisi 100% menunjukkan proporsi pencemar kritis di setiap stasiun."
        ),
    )

    if critical_viz_mode == "Komposisi 100% per stasiun":
        critical_station_plot = critical_station.copy()
        critical_station_plot["total_stasiun"] = critical_station_plot.groupby("stasiun")["jumlah"].transform("sum")
        critical_station_plot["persentase"] = (
            critical_station_plot["jumlah"] / critical_station_plot["total_stasiun"] * 100
        )

        fig_crit_station = px.bar(
            critical_station_plot,
            x="stasiun",
            y="persentase",
            color="critical_display",
            title="Komposisi Pencemar Kritis per Stasiun (100%)",
            labels={"stasiun": "Stasiun", "persentase": "Komposisi (%)", "critical_display": "Pencemar"},
            color_discrete_map=CRITICAL_COLORS,
            text=critical_station_plot["persentase"].round(1).astype(str) + "%",
            hover_data={"jumlah": True, "persentase": ":.2f", "total_stasiun": True},
        )
        fig_crit_station.update_layout(
            barmode="stack",
            yaxis=dict(range=[0, 100], ticksuffix="%"),
        )
        fig_crit_station.update_traces(textposition="inside", textfont_size=10)
        fig_crit_station.add_hline(
            y=50,
            line_dash="dot",
            line_color="#475569",
            line_width=1.8,
            annotation_text="Dominasi 50%",
            annotation_position="top left",
            annotation_font=dict(color="#475569", size=11),
        )

    elif critical_viz_mode == "Disandingkan antar pencemar":
        fig_crit_station = px.bar(
            critical_station,
            x="stasiun",
            y="jumlah",
            color="critical_display",
            title="Pencemar Kritis Antar Stasiun — Mode Disandingkan",
            labels={"stasiun": "Stasiun", "jumlah": "Jumlah Kemunculan", "critical_display": "Pencemar"},
            color_discrete_map=CRITICAL_COLORS,
            text="jumlah",
        )
        fig_crit_station.update_layout(barmode="group")
        fig_crit_station.update_traces(textposition="outside")

    else:
        fig_crit_station = px.bar(
            critical_station,
            x="stasiun",
            y="jumlah",
            color="critical_display",
            title="Perbandingan Pencemar Kritis Antar Stasiun — Stacked Jumlah Kemunculan",
            labels={"stasiun": "Stasiun", "jumlah": "Jumlah Kemunculan", "critical_display": "Pencemar"},
            color_discrete_map=CRITICAL_COLORS,
        )
        fig_crit_station.update_layout(barmode="stack")

    st.plotly_chart(style_plotly(fig_crit_station, height=455), use_container_width=True)

    if critical_viz_mode == "Komposisi 100% per stasiun":
        insight_box(
            "Cara membaca komposisi pencemar kritis",
            (
                "Mode komposisi 100% menormalkan total kemunculan setiap stasiun menjadi 100%. "
                "Mode ini membantu stakeholder melihat pencemar mana yang paling dominan secara proporsional pada masing-masing SPKU, "
                "tanpa bias dari perbedaan jumlah observasi antar stasiun."
            ),
            icon="🧭",
        )
    elif critical_viz_mode == "Disandingkan antar pencemar":
        insight_box(
            "Cara membaca mode disandingkan",
            (
                "Mode disandingkan memudahkan pembandingan satu parameter pencemar antar SPKU. "
                "Gunakan mode ini untuk melihat apakah O3, PM10, CO, SO2, atau NO2 lebih sering menjadi pencemar kritis di lokasi tertentu."
            ),
            icon="🧭",
        )

    trend_granularity = st.radio("Granularitas tren pencemar kritis", ["Bulanan", "Tahunan"], horizontal=True)
    if trend_granularity == "Bulanan":
        critical_trend = (
            filtered_df.groupby(["tahun_bulan", "critical_display"], as_index=False)
            .size()
            .rename(columns={"size": "jumlah"})
            .sort_values("tahun_bulan")
        )
        trend_x = "tahun_bulan"
    else:
        critical_trend = (
            filtered_df.groupby(["tahun", "critical_display"], as_index=False)
            .size()
            .rename(columns={"size": "jumlah"})
            .sort_values("tahun")
        )
        trend_x = "tahun"

    fig_critical_trend = px.line(
        critical_trend,
        x=trend_x,
        y="jumlah",
        color="critical_display",
        markers=True,
        title=f"Tren Kemunculan Pencemar Kritis ({trend_granularity})",
        labels={trend_x: "Periode", "jumlah": "Jumlah Kemunculan", "critical_display": "Pencemar"},
        color_discrete_map=CRITICAL_COLORS,
    )
    fig_critical_trend.update_traces(line=dict(width=2.5))
    st.plotly_chart(style_plotly(fig_critical_trend, height=470), use_container_width=True)

    dominant_pollutant = critical_count.iloc[0]["critical"]
    dominant_pct = critical_count.iloc[0]["persentase"]

    insight_box(
        "Analisis & insight pencemar kritis",
        (
            f"Parameter paling dominan sebagai pencemar kritis adalah <b>{dominant_pollutant}</b> "
            f"dengan proporsi <b>{dominant_pct:.1f}%</b>. Karena PM2.5 di-drop pada V5, interpretasi pencemar kritis "
            f"dibatasi pada polutan aktif final: <b>{', '.join([c.upper() for c in pollutant_cols])}</b>. "
            f"Dashboard ini tidak lagi menyimpulkan dominasi PM2.5 sebagai hasil final."
        ),
        icon="🏭",
    )


# =============================================================================
# TAB 5 — SEASONAL
# =============================================================================
with tab5:
    st.subheader("Dashboard 5 — Pola Musiman Kualitas Udara")
    st.caption("Mengidentifikasi bulan dan musim yang memiliki kualitas udara relatif lebih baik atau buruk.")
    season_mapping_note()
    category_legend_note()

    heatmap_df = (
        filtered_df.groupby(["stasiun", "bulan", "bulan_abbr"], as_index=False)
        .agg(rata_rata_ispu=("max", "mean"))
        .sort_values("bulan")
    )

    fig_heatmap = px.density_heatmap(
        heatmap_df,
        x="bulan_abbr",
        y="stasiun",
        z="rata_rata_ispu",
        title="Heatmap Rata-rata ISPU berdasarkan Bulan dan Stasiun",
        category_orders={"bulan_abbr": list(MONTH_ABBR.values())},
        color_continuous_scale=[[0, "#15803D"], [0.35, "#D97706"], [0.7, "#DC2626"], [1, "#7F1D1D"]],
        labels={"bulan_abbr": "Bulan", "stasiun": "Stasiun", "rata_rata_ispu": "Rata-rata ISPU"},
    )
    fig_heatmap.add_annotation(
        x=0.5,
        y=-0.18,
        xref="paper",
        yref="paper",
        text="Interpretasi warna: semakin merah berarti rata-rata ISPU semakin tinggi. Lihat chart bulanan/musiman untuk garis ambang 50 dan 100.",
        showarrow=False,
        font=dict(size=11, color="#475569"),
    )
    st.plotly_chart(style_plotly(fig_heatmap, height=520), use_container_width=True)

    col_month, col_season = st.columns([1, 1])
    with col_month:
        threshold_note()
        month_summary = (
            filtered_df.groupby(["bulan", "bulan_abbr"], as_index=False)
            .agg(rata_rata_ispu=("max", "mean"))
            .sort_values("bulan")
        )
        fig_month = px.bar(
            month_summary,
            x="bulan_abbr",
            y="rata_rata_ispu",
            title="Rata-rata ISPU per Bulan",
            category_orders={"bulan_abbr": list(MONTH_ABBR.values())},
            labels={"bulan_abbr": "Bulan", "rata_rata_ispu": "Rata-rata ISPU"},
            text=month_summary["rata_rata_ispu"].round(1),
        )
        fig_month.update_traces(marker_color="#B45309", textposition="outside")
        fig_month = add_ispu_threshold_lines(fig_month, month_summary["rata_rata_ispu"].max())
        st.plotly_chart(style_plotly(fig_month, height=430), use_container_width=True)

    with col_season:
        threshold_note()
        season_summary = (
            filtered_df.groupby("musim", as_index=False)
            .agg(rata_rata_ispu=("max", "mean"), jumlah_observasi=("max", "size"))
            .sort_values("rata_rata_ispu", ascending=False)
        )
        fig_season = px.bar(
            season_summary,
            x="musim",
            y="rata_rata_ispu",
            title="Rata-rata ISPU per Musim",
            labels={"musim": "Musim", "rata_rata_ispu": "Rata-rata ISPU"},
            text=season_summary["rata_rata_ispu"].round(1),
        )
        fig_season.update_traces(marker_color="#0F766E", textposition="outside")
        fig_season = add_ispu_threshold_lines(fig_season, season_summary["rata_rata_ispu"].max())
        st.plotly_chart(style_plotly(fig_season, height=430), use_container_width=True)

    worst_month = month_summary.loc[month_summary["rata_rata_ispu"].idxmax()]
    best_month = month_summary.loc[month_summary["rata_rata_ispu"].idxmin()]
    worst_season = season_summary.iloc[0]

    insight_box(
        "Analisis & insight pola musiman",
        (
            f"Bulan dengan rata-rata ISPU terburuk adalah <b>{worst_month['bulan_abbr']}</b> "
            f"({worst_month['rata_rata_ispu']:.1f}), sedangkan bulan terbaik adalah "
            f"<b>{best_month['bulan_abbr']}</b> ({best_month['rata_rata_ispu']:.1f}). "
            f"Musim terburuk adalah <b>{worst_season['musim']}</b>. Garis ambang memperjelas apakah rata-rata periode "
            f"masih berada pada zona BAIK/SEDANG atau mendekati Tidak Sehat+."
        ),
        icon="🗓️",
    )
