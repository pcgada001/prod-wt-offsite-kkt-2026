# ============================================
# DASHBOARD PRODUCTION & WELL TEST
# ============================================

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path


# ============================================
# 1. PENGATURAN HALAMAN
# ============================================

st.set_page_config(
    page_title="Production & Well Test Dashboard",
    page_icon="📊",
    layout="wide"
)


# ============================================
# 2. CARI FILE EXCEL
# ============================================

excel_files = list(Path(".").glob("*.xlsx"))

if len(excel_files) == 0:
    st.error("File Excel (.xlsx) tidak ditemukan di repository GitHub.")
    st.stop()

# Ambil file Excel pertama
file_name = excel_files[0]


# ============================================
# 3. BACA EXCEL
# ============================================

try:
    df = pd.read_excel(
        file_name,
        sheet_name="Koreksi_Data",
        header=5
    )

except Exception as e:
    st.error("Gagal membaca sheet 'Koreksi_Data'.")
    st.exception(e)
    st.stop()


# ============================================
# 4. RAPIKAN NAMA KOLOM
# ============================================

df = df.rename(columns={
    "Prod": "Oil_Prod",
    "WT": "Oil_WT",
    "Multiplier": "Oil_Multiplier",
    "Prod Koreksi": "Oil_Prod_Koreksi",

    "Prod.1": "Gas_Prod",
    "WT.1": "Gas_WT",
    "Multiplier.1": "Gas_Multiplier",
    "Prod Koreksi.1": "Gas_Prod_Koreksi",

    "Prod.2": "Water_Prod",
    "WT.2": "Water_WT",
    "Multiplier.2": "Water_Multiplier",
    "Prod Koreksi.2": "Water_Prod_Koreksi",

    "Prod.3": "Fluid_Prod",
    "WT.3": "Fluid_WT",
    "Multiplier.3": "Fluid_Multiplier",
    "Prod Koreksi.3": "Fluid_Prod_Koreksi",

    "Hari/bulan": "Hari_Bulan"
})


# ============================================
# 5. RAPIIKAN DATA TANGGAL
# ============================================

df["Bulan"] = pd.to_datetime(
    df["Bulan"],
    errors="coerce"
)

df = df.sort_values(
    by=["Well", "Bulan"]
).reset_index(drop=True)


# ============================================
# 6. JUDUL DASHBOARD
# ============================================

st.title("📊 Production & Well Test Dashboard")

st.write(
    "Dashboard interaktif Production, Well Test, "
    "dan Production Koreksi."
)


# ============================================
# 7. PILIH WELL
# ============================================

well_list = sorted(
    df["Well"].dropna().unique()
)

selected_well = st.selectbox(
    "Pilih Well",
    well_list
)


# ============================================
# 8. AMBIL DATA WELL
# ============================================

df_well = df[
    df["Well"] == selected_well
].copy()


# ============================================
# 9. BUAT GRAFIK
# ============================================

fig = go.Figure()


# --------------------------------------------
# Production
# --------------------------------------------

fig.add_trace(
    go.Scatter(
        x=df_well["Bulan"],
        y=df_well["Oil_Prod"],
        mode="lines+markers",
        name="Production",

        customdata=df_well[
            [
                "Oil_WT",
                "Oil_Multiplier",
                "Oil_Prod_Koreksi"
            ]
        ],

        hovertemplate=
            "<b>Tanggal:</b> %{x|%b-%Y}<br>"
            "<b>Production:</b> %{y:.2f}<br>"
            "<b>Well Test:</b> %{customdata[0]:.2f}<br>"
            "<b>Multiplier:</b> %{customdata[1]:.4f}<br>"
            "<b>Production Koreksi:</b> %{customdata[2]:.2f}"
            "<extra></extra>"
    )
)


# --------------------------------------------
# Well Test
# --------------------------------------------

fig.add_trace(
    go.Scatter(
        x=df_well["Bulan"],
        y=df_well["Oil_WT"],
        mode="lines+markers",
        name="Well Test",

        hovertemplate=
            "<b>Tanggal:</b> %{x|%b-%Y}<br>"
            "<b>Well Test:</b> %{y:.2f}"
            "<extra></extra>"
    )
)


# --------------------------------------------
# Production Koreksi
# --------------------------------------------

fig.add_trace(
    go.Scatter(
        x=df_well["Bulan"],
        y=df_well["Oil_Prod_Koreksi"],
        mode="lines+markers",
        name="Production Koreksi",

        hovertemplate=
            "<b>Tanggal:</b> %{x|%b-%Y}<br>"
            "<b>Production Koreksi:</b> %{y:.2f}"
            "<extra></extra>"
    )
)


# ============================================
# 10. PENGATURAN GRAFIK
# ============================================

fig.update_layout(
    title=f"Oil Production - {selected_well}",

    xaxis_title="Bulan",

    yaxis_title="Oil Rate",

    hovermode="x unified",

    template="plotly_white",

    height=600
)


# ============================================
# 11. TAMPILKAN GRAFIK DI STREAMLIT
# ============================================

st.plotly_chart(
    fig,
    use_container_width=True
)
