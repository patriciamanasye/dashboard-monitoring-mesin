
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Dashboard Monitoring Mesin", layout="wide")
st.title("Dashboard Monitoring Mesin")

# File CSV untuk menyimpan data
DATA_FILE = "data_mesin.csv"

# Inisialisasi data jika file belum ada
if not os.path.exists(DATA_FILE):
    df_init = pd.DataFrame(columns=["Tanggal", "Nama Mesin", "Status", "Keterangan"])
    df_init.to_csv(DATA_FILE, index=False)

# Fungsi untuk load dan simpan data
def load_data():
    return pd.read_csv(DATA_FILE)

def save_data(new_data):
    df = load_data()
    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

# Form input
with st.form("form_input"):
    st.subheader("Input Data Mesin")
    col1, col2 = st.columns(2)
    tanggal = col1.date_input("Tanggal")
    nama_mesin = col2.text_input("Nama Mesin")
    status = st.selectbox("Status", ["Beroperasi", "Idle", "Rusak", "Maintenance"])
    keterangan = st.text_area("Keterangan")
    submitted = st.form_submit_button("Simpan")
    if submitted and nama_mesin:
        save_data({
            "Tanggal": tanggal,
            "Nama Mesin": nama_mesin,
            "Status": status,
            "Keterangan": keterangan
        })
        st.success("Data berhasil disimpan.")

# Tampilkan data
st.subheader("Data Monitoring Mesin")
df = load_data()
st.dataframe(df, use_container_width=True)
