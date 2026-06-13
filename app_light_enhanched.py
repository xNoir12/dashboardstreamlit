
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="Dashboard ISPU Jakarta",
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
@st.cache_data(show_spinner="Memuat dataset ISPU Jakarta hasil cleaning...")
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
    df["minggu_mulai"] = df["tanggal"].dt.to_period("W-MON").apply(lambda r: r.start_time)
    df["minggu_selesai"] = df["tanggal"].dt.to_period("W-MON").apply(lambda r: r.end_time)
    df["label_minggu"] = (
        df["minggu_mulai"].dt.strftime("%d %b %Y") + " – " + df["minggu_selesai"].dt.strftime("%d %b %Y")
    )
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


def month_start(year, month):
    return pd.Timestamp(year=int(year), month=int(month), day=1)


def month_end(year, month):
    return pd.Timestamp(year=int(year), month=int(month), day=1) + pd.offsets.MonthEnd(0)


def build_global_period_controls(df):
    """Filter periode global berbasis dropdown tahun/bulan dan date range agar semua tab sinkron."""
    min_date = df["tanggal"].min()
    max_date = df["tanggal"].max()

    available_years = sorted(df["tahun"].dropna().astype(int).unique().tolist())
    month_options = list(MONTH_ABBR.items())
    month_label_to_num = {label: num for num, label in month_options}
    month_labels = [label for _, label in month_options]

    st.markdown("### Filter Periode")
    period_mode = st.radio(
        "Mode periode",
        ["Seluruh periode", "Tahun tunggal", "Rentang tahun", "Rentang bulan", "Rentang tanggal"],
        horizontal=False,
        index=0,
        help=(
            "Filter periode ini berlaku global untuk seluruh dashboard. "
            "Gunakan Rentang tanggal untuk kebutuhan harian, mingguan, atau periode khusus."
        ),
    )

    start_date = min_date
    end_date = max_date
    period_label = f"{min_date.date()} s.d. {max_date.date()}"

    if period_mode == "Tahun tunggal":
        selected_year = st.selectbox(
            "Tahun",
            available_years,
            index=len(available_years) - 1,
            key="global_single_year",
        )
        start_date = pd.Timestamp(year=int(selected_year), month=1, day=1)
        end_date = pd.Timestamp(year=int(selected_year), month=12, day=31)
        start_date = max(start_date, min_date)
        end_date = min(end_date, max_date)
        period_label = f"Tahun {selected_year}"

    elif period_mode == "Rentang tahun":
        col_start, col_end = st.columns(2)
        with col_start:
            start_year = st.selectbox(
                "Tahun awal",
                available_years,
                index=0,
                key="global_start_year",
            )

        end_year_options = [year for year in available_years if year >= int(start_year)]
        with col_end:
            end_year = st.selectbox(
                "Tahun akhir",
                end_year_options,
                index=len(end_year_options) - 1,
                key="global_end_year",
            )

        start_date = pd.Timestamp(year=int(start_year), month=1, day=1)
        end_date = pd.Timestamp(year=int(end_year), month=12, day=31)
        start_date = max(start_date, min_date)
        end_date = min(end_date, max_date)
        period_label = f"Tahun {start_year}–{end_year}"

    elif period_mode == "Rentang bulan":
        st.caption("Pilih bulan dan tahun awal–akhir untuk analisis bulanan atau musiman.")

        col_y1, col_m1 = st.columns(2)
        with col_y1:
            start_year = st.selectbox(
                "Tahun awal",
                available_years,
                index=0,
                key="global_month_start_year",
            )
        with col_m1:
            start_month_label = st.selectbox(
                "Bulan awal",
                month_labels,
                index=0,
                key="global_start_month",
            )

        valid_end_years = [year for year in available_years if year >= int(start_year)]
        col_y2, col_m2 = st.columns(2)
        with col_y2:
            end_year = st.selectbox(
                "Tahun akhir",
                valid_end_years,
                index=len(valid_end_years) - 1,
                key="global_month_end_year",
            )

        start_month_num = month_label_to_num[start_month_label]
        if int(end_year) == int(start_year):
            valid_end_months = [label for num, label in month_options if num >= int(start_month_num)]
        else:
            valid_end_months = month_labels

        with col_m2:
            end_month_label = st.selectbox(
                "Bulan akhir",
                valid_end_months,
                index=len(valid_end_months) - 1,
                key="global_end_month",
            )

        end_month_num = month_label_to_num[end_month_label]
        start_date = month_start(start_year, start_month_num)
        end_date = month_end(end_year, end_month_num)

        start_date = max(start_date, min_date)
        end_date = min(end_date, max_date)
        period_label = f"{start_month_label} {start_year} – {end_month_label} {end_year}"

    elif period_mode == "Rentang tanggal":
        st.caption(
            "Gunakan mode ini untuk monitoring harian, mingguan, atau periode khusus. "
            "Contoh: pilih 7 hari untuk evaluasi mingguan."
        )

        date_range = st.date_input(
            "Rentang tanggal",
            value=(min_date.date(), max_date.date()),
            min_value=min_date.date(),
            max_value=max_date.date(),
            key="global_exact_date_range",
            help="Pilih tanggal awal dan akhir secara presisi.",
        )

        if isinstance(date_range, tuple) and len(date_range) == 2:
            start_date = pd.to_datetime(date_range[0])
            end_date = pd.to_datetime(date_range[1])
        else:
            start_date = min_date
            end_date = max_date

        period_days = max((end_date - start_date).days + 1, 1)
        period_label = f"{start_date.date()} s.d. {end_date.date()} ({period_days} hari)"

    return period_mode, pd.to_datetime(start_date), pd.to_datetime(end_date), period_label

def apply_global_filters(df, stations, start_date, end_date):
    out = df.copy()
    if stations:
        out = out[out["stasiun"].isin(stations)]
    out = out[(out["tanggal"] >= pd.to_datetime(start_date)) & (out["tanggal"] <= pd.to_datetime(end_date))]
    return out.copy()


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


def stakeholder_action_from_ispu(avg_value, unhealthy_pct):
    """Narasi aksi singkat yang tetap dinamis mengikuti filter aktif."""
    if pd.isna(avg_value):
        return "Data pada filter aktif belum cukup untuk menyusun arahan tindak lanjut."

    if avg_value > 100 or unhealthy_pct >= 20:
        return (
            "Arah tindak lanjut: prioritaskan pemantauan intensif pada lokasi/periode dengan risiko tertinggi, "
            "gunakan komunikasi risiko untuk kelompok rentan, dan evaluasi sumber emisi dominan pada periode tersebut."
        )

    if avg_value > 50:
        return (
            "Arah tindak lanjut: kondisi masih perlu dipantau karena rata-rata sudah melewati batas BAIK. "
            "Pertahankan pemantauan rutin dan siapkan peringatan dini bila tren mendekati ambang Tidak Sehat+."
        )

    return (
        "Arah tindak lanjut: kondisi relatif terkendali pada filter aktif. "
        "Fokus pada pemeliharaan pemantauan dan deteksi dini jika terjadi kenaikan."
    )


def stakeholder_action_from_trend(direction, unhealthy_period_count, total_period_count):
    if total_period_count <= 0:
        return "Belum cukup periode untuk memberikan arahan tren."

    if unhealthy_period_count > 0:
        return (
            f"Terdapat {unhealthy_period_count} dari {total_period_count} periode agregat yang berada di atas ambang 100. "
            "Periode tersebut dapat dijadikan prioritas pengecekan operasional dan komunikasi risiko."
        )

    if direction == "memburuk":
        return (
            "Walaupun belum melewati ambang Tidak Sehat+, arah tren meningkat sehingga perlu dipantau sebagai early warning."
        )

    if direction == "membaik":
        return (
            "Arah tren membaik. Praktik atau kondisi pada periode yang lebih baik dapat dijadikan pembanding untuk evaluasi."
        )

    return "Tren relatif stabil. Fokus pemantauan diarahkan pada periode dengan nilai puncak."


def stakeholder_action_from_station(gap_value, worst_risk_pct):
    if worst_risk_pct >= 20:
        return (
            "Prioritas intervensi spasial sebaiknya diarahkan pada stasiun dengan persentase Tidak Sehat+ tertinggi, "
            "karena risiko paparan relatif lebih sering muncul pada lokasi tersebut."
        )

    if gap_value >= 15:
        return (
            "Terdapat gap kualitas udara yang cukup nyata antar stasiun. "
            "Perlu ditinjau faktor lokal yang membedakan stasiun dengan nilai tertinggi dan terendah."
        )

    return (
        "Perbedaan antar stasiun relatif tidak terlalu lebar pada filter aktif. "
        "Pemantauan dapat difokuskan pada perubahan temporal dan pencemar dominan."
    )


def stakeholder_action_from_season(worst_month_value):
    if pd.isna(worst_month_value):
        return "Belum cukup data untuk menyusun arahan musiman."

    if worst_month_value > 100:
        return (
            "Bulan dengan nilai tertinggi sudah melewati ambang Tidak Sehat+, sehingga periode tersebut layak menjadi prioritas pengawasan musiman."
        )

    if worst_month_value > 50:
        return (
            "Bulan dengan nilai tertinggi berada di atas batas BAIK. "
            "Gunakan pola ini untuk menyusun jadwal pemantauan dan komunikasi risiko secara preventif."
        )

    return (
        "Secara musiman nilai tertinggi masih berada pada level relatif terkendali, tetapi pemantauan berkala tetap diperlukan."
    )


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
            <span class="threshold-pill">Polutan aktif: {pollutant_text}</span>
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


def period_trend(df, granularity, monthly_x_mode="Jan–Des"):
    if granularity == "Harian":
        return (
            df.groupby("tanggal", as_index=False)
            .agg(rata_rata_ispu=("max", "mean"))
            .sort_values("tanggal"),
            "tanggal",
            "Tanggal",
        )

    if granularity == "Mingguan":
        trend = (
            df.groupby(["minggu_mulai", "label_minggu"], as_index=False)
            .agg(rata_rata_ispu=("max", "mean"))
            .sort_values("minggu_mulai")
        )
        return trend, "label_minggu", "Minggu"

    if granularity == "Bulanan":
        working = df.copy()
        if monthly_x_mode == "Jan–Des":
            trend = (
                working.groupby(["bulan", "bulan_abbr"], as_index=False)
                .agg(rata_rata_ispu=("max", "mean"))
                .sort_values("bulan")
            )
            return trend, "bulan_abbr", "Bulan"

        trend = (
            working.groupby("tahun_bulan", as_index=False)
            .agg(rata_rata_ispu=("max", "mean"))
            .sort_values("tahun_bulan")
        )
        return trend, "tahun_bulan", "Bulan"

    return (
        df.groupby("tahun", as_index=False)
        .agg(rata_rata_ispu=("max", "mean"))
        .sort_values("tahun"),
        "tahun",
        "Tahun",
    )


def station_period_trend(df, granularity, monthly_x_mode="Jan–Des"):
    if granularity == "Harian":
        return (
            df.groupby(["tanggal", "stasiun"], as_index=False)
            .agg(rata_rata_ispu=("max", "mean"))
            .sort_values("tanggal"),
            "tanggal",
        )

    if granularity == "Mingguan":
        trend = (
            df.groupby(["minggu_mulai", "label_minggu", "stasiun"], as_index=False)
            .agg(rata_rata_ispu=("max", "mean"))
            .sort_values("minggu_mulai")
        )
        return trend, "label_minggu"

    if granularity == "Bulanan":
        working = df.copy()
        if monthly_x_mode == "Jan–Des":
            trend = (
                working.groupby(["bulan", "bulan_abbr", "stasiun"], as_index=False)
                .agg(rata_rata_ispu=("max", "mean"))
                .sort_values("bulan")
            )
            return trend, "bulan_abbr"

        trend = (
            working.groupby(["tahun_bulan", "stasiun"], as_index=False)
            .agg(rata_rata_ispu=("max", "mean"))
            .sort_values("tahun_bulan")
        )
        return trend, "tahun_bulan"

    return (
        df.groupby(["tahun", "stasiun"], as_index=False)
        .agg(rata_rata_ispu=("max", "mean"))
        .sort_values("tahun"),
        "tahun",
    )


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
            Dashboard analisis ISPU Jakarta ini sudah mengikuti feedback asesor dan menambahkan mode chart kategori:
            Visualisasi ditingkatkan agar tidak hanya menampilkan data, tetapi juga informasi melalui garis ambang ISPU. Seluruh periode analisis dikendalikan melalui filter global di sidebar.
        </div>
        <span class="source-pill">Sumber dataset: D00_ispu_jakarta_final_sot_v5_drop_over50.csv</span>
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
    selected_stations = st.multiselect(
        "Stasiun SPKU",
        all_stations,
        default=all_stations,
        help="Filter stasiun ini berlaku untuk seluruh tab dashboard.",
    )

    period_mode, global_start_date, global_end_date, global_period_label = build_global_period_controls(df)

    st.markdown("---")
    st.markdown("### Catatan Dataset")
    st.caption("PM2.5 di-drop karena missing value lebih dari 50%.")
    st.caption(f"Polutan aktif: {', '.join([c.upper() for c in pollutant_cols])}.")
    st.caption("Ambang informasi: ISPU 50 = batas BAIK; ISPU 100 = mulai Tidak Sehat+.")

filtered_df = apply_global_filters(df, selected_stations, global_start_date, global_end_date)

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
        f'<div class="small-muted">Periode aktif</div><h3>{global_period_label}</h3>',
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
    overview_action = stakeholder_action_from_ispu(avg_ispu, pct_unhealthy)

    insight_box(
        "Analisis & insight overview",
        (
            f"Pada filter aktif, rata-rata ISPU adalah <b>{avg_ispu:.1f}</b> dengan kelas <b>{avg_category}</b>. "
            f"Proporsi observasi Tidak Sehat+ mencapai <b>{pct_unhealthy:.1f}%</b>, sehingga perlu dibaca sebagai indikator frekuensi risiko, "
            f"bukan hanya nilai rata-rata. Pencemar yang paling sering menjadi critical adalah <b>{dominant_pollutant}</b>. "
            f"Lokasi prioritas berdasarkan rata-rata ISPU adalah <b>{worst_station}</b>, sedangkan <b>{best_station}</b> dapat menjadi pembanding kondisi relatif lebih baik. "
            f"<br><br><b>{overview_action}</b>"
        ),
        icon="✅",
    )


# =============================================================================
# TAB 2 — TEMPORAL
# =============================================================================
with tab2:
    st.subheader("Dashboard 2 — Tren Temporal Kualitas Udara")
    st.caption("Membaca arah perubahan kualitas udara dari waktu ke waktu dengan garis ambang interpretasi ISPU.")

    granularity = st.radio("Granularitas", ["Harian", "Mingguan", "Bulanan", "Tahunan"], horizontal=True, index=2)
    compare_mode = st.radio("Mode perbandingan", ["Rata-rata Jakarta", "Per Stasiun"], horizontal=True, index=1)

    temporal_df = filtered_df.copy()
    temporal_scope_label = global_period_label

    monthly_x_mode = "Jan–Des"
    if granularity == "Bulanan":
        monthly_x_mode = st.radio(
            "Mode sumbu X bulanan",
            ["Jan–Des", "Bulan lintas tahun"],
            horizontal=True,
            index=0,
            key="temporal_monthly_x_mode",
            help=(
                "Jan–Des menampilkan rata-rata per bulan pada periode global aktif. "
                "Bulan lintas tahun menampilkan urutan YYYY-MM secara kronologis."
            ),
        )
        st.caption(
            f"Periode global aktif: {global_period_label}. "
            "Mode Jan–Des cocok untuk melihat rata-rata bulanan dalam periode tersebut."
        )

    if granularity in ["Harian", "Mingguan"]:
        st.caption(
            f"Periode global aktif: {global_period_label}. "
            "Untuk melihat periode harian/mingguan tertentu, gunakan Mode periode 'Rentang tanggal' di sidebar."
        )

    threshold_note()

    if compare_mode == "Rata-rata Jakarta":
        trend_df, x_col, x_title = period_trend(temporal_df, granularity, monthly_x_mode)
        fig_trend = px.line(
            trend_df,
            x=x_col,
            y="rata_rata_ispu",
            markers=True,
            title=f"Tren Rata-rata ISPU Jakarta ({granularity}) — {temporal_scope_label}",
            labels={x_col: x_title, "rata_rata_ispu": "Rata-rata ISPU"},
            category_orders={
                "bulan_abbr": list(MONTH_ABBR.values()),
                "label_minggu": trend_df["label_minggu"].tolist() if "label_minggu" in trend_df.columns else [],
            },
        )
        fig_trend.update_traces(line=dict(width=3, color="#B45309"), marker=dict(size=7))
        y_hint = trend_df["rata_rata_ispu"].max()
    else:
        trend_df, x_col = station_period_trend(temporal_df, granularity, monthly_x_mode)
        fig_trend = px.line(
            trend_df,
            x=x_col,
            y="rata_rata_ispu",
            color="stasiun",
            markers=True,
            title=f"Perbandingan Tren ISPU Antar Stasiun ({granularity}) — {temporal_scope_label}",
            labels={x_col: granularity, "rata_rata_ispu": "Rata-rata ISPU", "stasiun": "Stasiun"},
            category_orders={
                "bulan_abbr": list(MONTH_ABBR.values()),
                "label_minggu": trend_df["label_minggu"].tolist() if "label_minggu" in trend_df.columns else [],
            },
        )
        fig_trend.update_traces(line=dict(width=2.5), marker=dict(size=6))
        y_hint = trend_df["rata_rata_ispu"].max()

    fig_trend = add_ispu_threshold_lines(fig_trend, y_hint)
    st.plotly_chart(style_plotly(fig_trend, height=500), use_container_width=True)

    trend_overall, overall_x_col, _ = period_trend(temporal_df, granularity, monthly_x_mode)
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
    best_period = trend_overall.loc[trend_overall["rata_rata_ispu"].idxmin()]
    unhealthy_period_count = int((trend_overall["rata_rata_ispu"] > 100).sum())
    total_period_count = int(len(trend_overall))
    temporal_action = stakeholder_action_from_trend(direction, unhealthy_period_count, total_period_count)

    insight_box(
        "Analisis & insight tren temporal",
        (
            f"Tren pada granularitas <b>{granularity.lower()}</b> untuk periode <b>{temporal_scope_label}</b> terlihat <b>{direction}</b> "
            f"dengan perubahan <b>{change:+.1f}</b> poin dari awal ke akhir periode. "
            f"Periode terburuk adalah <b>{worst_period[overall_x_col]}</b> ({worst_period['rata_rata_ispu']:.1f}), "
            f"sedangkan periode terbaik adalah <b>{best_period[overall_x_col]}</b> ({best_period['rata_rata_ispu']:.1f}). "
            f"Terdapat <b>{unhealthy_period_count}</b> dari <b>{total_period_count}</b> periode agregat yang melewati ambang 100. "
            f"<br><br><b>{temporal_action}</b>"
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
    station_gap = float(worst_avg["rata_rata_ispu"] - best_avg["rata_rata_ispu"])
    station_action = stakeholder_action_from_station(station_gap, float(worst_risk["persentase_tidak_sehat_plus"]))

    insight_box(
        "Analisis & insight antar stasiun",
        (
            f"Stasiun dengan rata-rata ISPU tertinggi adalah <b>{worst_avg['stasiun']}</b> "
            f"({worst_avg['rata_rata_ispu']:.1f}), sedangkan yang terendah adalah "
            f"<b>{best_avg['stasiun']}</b> ({best_avg['rata_rata_ispu']:.1f}). "
            f"Gap antar keduanya sebesar <b>{station_gap:.1f}</b> poin, yang membantu membaca ketimpangan kondisi antar lokasi. "
            f"Dari sisi proporsi risiko, <b>{worst_risk['stasiun']}</b> memiliki persentase Tidak Sehat+ tertinggi "
            f"(<b>{worst_risk['persentase_tidak_sehat_plus']:.1f}%</b>). "
            f"<br><br><b>{station_action}</b>"
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

    trend_granularity = st.radio("Granularitas tren pencemar kritis", ["Harian", "Mingguan", "Bulanan", "Tahunan"], horizontal=True, index=2)

    critical_scope_df = filtered_df.copy()
    critical_scope_label = global_period_label

    critical_monthly_x_mode = "Jan–Des"
    if trend_granularity == "Bulanan":
        critical_monthly_x_mode = st.radio(
            "Mode sumbu X pencemar bulanan",
            ["Jan–Des", "Bulan lintas tahun"],
            horizontal=True,
            index=0,
            key="critical_monthly_x_mode",
            help=(
                "Jan–Des menampilkan akumulasi per bulan pada periode global aktif. "
                "Bulan lintas tahun menampilkan urutan YYYY-MM secara kronologis."
            ),
        )
        st.caption(f"Periode global aktif: {global_period_label}.")

    if trend_granularity == "Harian":
        critical_trend = (
            critical_scope_df.groupby(["tanggal", "critical_display"], as_index=False)
            .size()
            .rename(columns={"size": "jumlah"})
            .sort_values("tanggal")
        )
        trend_x = "tanggal"

    elif trend_granularity == "Mingguan":
        critical_trend = (
            critical_scope_df.groupby(["minggu_mulai", "label_minggu", "critical_display"], as_index=False)
            .size()
            .rename(columns={"size": "jumlah"})
            .sort_values("minggu_mulai")
        )
        trend_x = "label_minggu"

    elif trend_granularity == "Bulanan":
        if critical_monthly_x_mode == "Jan–Des":
            critical_trend = (
                critical_scope_df.groupby(["bulan", "bulan_abbr", "critical_display"], as_index=False)
                .size()
                .rename(columns={"size": "jumlah"})
                .sort_values("bulan")
            )
            trend_x = "bulan_abbr"
        else:
            critical_trend = (
                critical_scope_df.groupby(["tahun_bulan", "critical_display"], as_index=False)
                .size()
                .rename(columns={"size": "jumlah"})
                .sort_values("tahun_bulan")
            )
            trend_x = "tahun_bulan"
    else:
        critical_trend = (
            critical_scope_df.groupby(["tahun", "critical_display"], as_index=False)
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
        title=f"Tren Kemunculan Pencemar Kritis ({trend_granularity}) — {critical_scope_label}",
        labels={trend_x: "Bulan" if trend_x == "bulan_abbr" else "Periode", "jumlah": "Jumlah Kemunculan", "critical_display": "Pencemar"},
        color_discrete_map=CRITICAL_COLORS,
        category_orders={
            "bulan_abbr": list(MONTH_ABBR.values()),
            "label_minggu": critical_trend["label_minggu"].tolist() if "label_minggu" in critical_trend.columns else [],
        },
    )
    fig_critical_trend.update_traces(line=dict(width=2.5))
    st.plotly_chart(style_plotly(fig_critical_trend, height=470), use_container_width=True)

    dominant_pollutant = critical_count.iloc[0]["critical"]
    dominant_pct = critical_count.iloc[0]["persentase"]

    station_top_pollutant = (
        critical_station.sort_values(["stasiun", "jumlah"], ascending=[True, False])
        .groupby("stasiun")
        .head(1)
    )
    pollutant_pattern = "; ".join(
        [f"{row['stasiun']}: {row['critical_display']}" for _, row in station_top_pollutant.iterrows()]
    )
    dominant_action = (
        "Arah tindak lanjut: gunakan parameter dominan ini sebagai fokus awal evaluasi sumber emisi dan strategi pengendalian pada periode aktif."
        if dominant_pct >= 50
        else "Arah tindak lanjut: karena dominasi pencemar relatif tersebar, evaluasi perlu dilakukan per stasiun dan per periode, bukan hanya pada satu parameter."
    )

    insight_box(
        "Analisis & insight pencemar kritis",
        (
            f"Pada filter aktif, parameter yang paling sering menjadi pencemar kritis adalah <b>{dominant_pollutant}</b> "
            f"dengan proporsi <b>{dominant_pct:.1f}%</b>. Pola dominan per stasiun adalah: <b>{pollutant_pattern}</b>. "
            f"Informasi ini membantu stakeholder menentukan parameter mana yang perlu menjadi prioritas pemantauan, "
            f"terutama ketika pola pencemar berbeda antar lokasi. "
            f"<br><br><b>{dominant_action}</b>"
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

    seasonal_df = filtered_df.copy()
    seasonal_scope_label = global_period_label

    st.caption(
        f"Seluruh visualisasi musiman di tab ini menggunakan periode global aktif: {seasonal_scope_label}. "
        "Dengan demikian, stakeholder dapat melihat pola rata-rata sesuai periode yang dipilih di sidebar."
    )

    heatmap_df = (
        seasonal_df.groupby(["stasiun", "bulan", "bulan_abbr"], as_index=False)
        .agg(rata_rata_ispu=("max", "mean"))
        .sort_values("bulan")
    )

    fig_heatmap = px.density_heatmap(
        heatmap_df,
        x="bulan_abbr",
        y="stasiun",
        z="rata_rata_ispu",
        title=f"Heatmap Rata-rata ISPU berdasarkan Bulan dan Stasiun — {seasonal_scope_label}",
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
            seasonal_df.groupby(["bulan", "bulan_abbr"], as_index=False)
            .agg(rata_rata_ispu=("max", "mean"))
            .sort_values("bulan")
        )
        fig_month = px.bar(
            month_summary,
            x="bulan_abbr",
            y="rata_rata_ispu",
            title=f"Rata-rata ISPU per Bulan — {seasonal_scope_label}",
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
            seasonal_df.groupby("musim", as_index=False)
            .agg(rata_rata_ispu=("max", "mean"), jumlah_observasi=("max", "size"))
            .sort_values("rata_rata_ispu", ascending=False)
        )
        fig_season = px.bar(
            season_summary,
            x="musim",
            y="rata_rata_ispu",
            title=f"Rata-rata ISPU per Musim — {seasonal_scope_label}",
            labels={"musim": "Musim", "rata_rata_ispu": "Rata-rata ISPU"},
            text=season_summary["rata_rata_ispu"].round(1),
        )
        fig_season.update_traces(marker_color="#0F766E", textposition="outside")
        fig_season = add_ispu_threshold_lines(fig_season, season_summary["rata_rata_ispu"].max())
        st.plotly_chart(style_plotly(fig_season, height=430), use_container_width=True)

    worst_month = month_summary.loc[month_summary["rata_rata_ispu"].idxmax()]
    best_month = month_summary.loc[month_summary["rata_rata_ispu"].idxmin()]
    worst_season = season_summary.iloc[0]
    best_season = season_summary.iloc[-1]
    seasonal_action = stakeholder_action_from_season(float(worst_month["rata_rata_ispu"]))

    insight_box(
        "Analisis & insight pola musiman",
        (
            f"Pada periode <b>{seasonal_scope_label}</b>, bulan dengan rata-rata ISPU terburuk adalah <b>{worst_month['bulan_abbr']}</b> "
            f"({worst_month['rata_rata_ispu']:.1f}), sedangkan bulan terbaik adalah "
            f"<b>{best_month['bulan_abbr']}</b> ({best_month['rata_rata_ispu']:.1f}). "
            f"Musim dengan rata-rata tertinggi adalah <b>{worst_season['musim']}</b> "
            f"({worst_season['rata_rata_ispu']:.1f}), sedangkan musim terendah adalah <b>{best_season['musim']}</b> "
            f"({best_season['rata_rata_ispu']:.1f}). "
            f"<br><br><b>{seasonal_action}</b>"
        ),
        icon="🗓️",
    )
