import streamlit as st
import pandas as pd
import os
import plotly.express as px

st.set_page_config(page_title="Dashboard Monitoring Mesin", layout="wide")
st.title("Dashboard Monitoring Mesin")

DATA_FILE = "data_mesin.csv"

# Inisialisasi file jika belum ada
if not os.path.exists(DATA_FILE):
    df_init = pd.DataFrame(columns=["Tanggal", "Jam", "Mesin", "Aktivitas", "Loading", "Keterlambatan", "Status"])
    df_init.to_csv(DATA_FILE, index=False)

# Fungsi untuk load dan simpan data
def load_data():
    return pd.read_csv(DATA_FILE)

def save_data(entry):
    df = load_data()
    df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

# Form Input
with st.form("input_form"):
    st.subheader("Input Data Harian Mesin")
    col1, col2, col3 = st.columns(3)
    tanggal = col1.date_input("Tanggal")
    jam = col2.selectbox("Jam", [f"{h:02d}:00" for h in range(24)])
    mesin = col3.text_input("Nama Mesin")
    
    col4, col5, col6 = st.columns(3)
    aktivitas = col4.number_input("Aktivitas (menit)", min_value=0, step=1)
    loading = col5.number_input("Loading (kali)", min_value=0, step=1)
    keterlambatan = col6.number_input("Keterlambatan (menit)", min_value=0, step=1)
    
    status = st.selectbox("Status", ["Aktif", "Idle", "Stop"])
    submitted = st.form_submit_button("Simpan Data")

    if submitted and mesin:
        save_data({
            "Tanggal": tanggal,
            "Jam": jam,
            "Mesin": mesin,
            "Aktivitas": aktivitas,
            "Loading": loading,
            "Keterlambatan": keterlambatan,
            "Status": status
        })
        st.success("✅ Data berhasil disimpan!")

# Load dan tampilkan data
st.subheader("Riwayat Data")
df = load_data()
st.dataframe(df.sort_values(by=["Tanggal", "Jam"], ascending=False), use_container_width=True)

# Grafik Monitoring (jika ada data)
if not df.empty:
    st.subheader("Grafik Aktivitas Mesin")
    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.bar(df, x="Jam", y="Aktivitas", color="Mesin", title="Aktivitas per Jam")
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        fig2 = px.bar(df, x="Jam", y="Loading", color="Mesin", title="Loading per Jam")
        st.plotly_chart(fig2, use_container_width=True)
    
    fig3 = px.line(df, x="Jam", y="Keterlambatan", color="Mesin", markers=True, title="Keterlambatan per Jam")
    st.plotly_chart(fig3, use_container_width=True)