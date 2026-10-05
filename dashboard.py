# ============================================
# LANGKAH 1 - MEMBACA FILE EXCEL
# ============================================

import pandas as pd

file_name = "Prod_Terkoreksi_WellTest (1).xlsx"

df = pd.read_excel(
    file_name,
    sheet_name="Koreksi_Data",
    header=5
)

print("File berhasil dibaca!")
print("Nama file :", file_name)
print("Jumlah baris :", len(df))
print("Jumlah kolom :", len(df.columns))

# Tampilkan 5 baris pertama
df.head()
# ============================================
# LANGKAH 2 - MERAPIKAN DATA
# ============================================

# Buat nama kolom yang lebih mudah dipahami
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

# Pastikan kolom Bulan benar-benar bertipe tanggal
df["Bulan"] = pd.to_datetime(df["Bulan"])

# Urutkan berdasarkan Well dan Bulan
df = df.sort_values(
    by=["Well", "Bulan"]
).reset_index(drop=True)

# Tampilkan informasi data
print("Data berhasil dirapikan!")
print()
print("Jumlah Well :", df["Well"].nunique())
print("Daftar Well :")
print(df["Well"].unique())

print()
print("Periode data :")
print(df["Bulan"].min(), "sampai", df["Bulan"].max())

print()
print("Ukuran DataFrame :", df.shape)

# Tampilkan 5 baris pertama
df.head()

# ============================================
# LANGKAH 3 - GRAFIK INTERAKTIF DENGAN PLOTLY
# ============================================

import plotly.graph_objects as go

# Pilih Well
selected_well = "KKA-1"

# Ambil data untuk Well yang dipilih
df_well = df[df["Well"] == selected_well].copy()

# Buat grafik
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
            ["Oil_WT", "Oil_Multiplier", "Oil_Prod_Koreksi"]
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

# --------------------------------------------
# Pengaturan tampilan
# --------------------------------------------
fig.update_layout(
    title=f"Oil Production - {selected_well}",
    xaxis_title="Bulan",
    yaxis_title="Oil Rate",
    hovermode="x unified",
    template="plotly_white",
    height=600
)

# Tampilkan grafik
fig.show()
