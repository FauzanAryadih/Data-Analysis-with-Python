# Import library
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Fungsi untuk memuat data
@st.cache_data  # Menggunakan st.cache_data, karena kita cache data (bukan resource)
def load_data(file_path):
    data = pd.read_csv(file_path)
    data.drop_duplicates(inplace=True)  # Menghapus duplikasi
    return data

# Menentukan path file secara otomatis
file_path = 'customers_dataset.csv'  # Path ke file dataset

# Judul Dashboard
st.title("Dashboard Analisis Pelanggan")
st.markdown("Dashboard ini memberikan gambaran tentang data pelanggan, termasuk distribusi geografis dan pola data lainnya.")
st.subheader('by Fauzan Ayadih')
# Menambahkan Logo Bintang di atas Kalender menggunakan st.sidebar
with st.sidebar:
    st.image("bintang.jpg", width=150)

    # Menambahkan Kalender
    st.header("Pilih Tanggal")
    selected_date = st.date_input("Pilih tanggal", datetime.today())  # Menampilkan kalender di sidebar
    st.write(f"Tanggal yang dipilih: {selected_date}")

# Memuat dataset tanpa perlu upload
try:
    df = load_data(file_path)

    # Statistik Dasar
    st.header("Statistik Customers")
    
    # Menampilkan Kolom Metrics dengan style dan warna latar belakang
    unique_customers = df['customer_id'].nunique()
    total_rows = len(df)
    
    # Membuat kolom yang stylish dengan warna latar belakang dan ukuran seragam
    col1, col2 = st.columns(2)
    
    # Warna latar belakang, ukuran teks, dan padding seragam
    style = """
        <div style="background-color: {bg_color}; color: white; padding: 10px; border-radius: 10px; text-align: center; font-size: 20px;">
            <h3>{label}</h3>
            <h2>{value}</h2>
        </div>
    """
    
    # Kolom pertama (Jumlah Pelanggan Unik)
    with col1:
        st.markdown(
            style.format(bg_color="#4CAF50", label="Jumlah Pelanggan", value=unique_customers), 
            unsafe_allow_html=True
        )
    

    # Distribusi Pelanggan Berdasarkan Negara Bagian
    st.header("Distribusi Pelanggan Berdasarkan Negara Bagian")
    state_distribution = df['customer_state'].value_counts()
    st.bar_chart(state_distribution)

    # Distribusi Pelanggan Berdasarkan Kota
    st.header("Top 10 Kota dengan Jumlah Pelanggan Terbanyak")
    top_cities = df['customer_city'].value_counts().head(10)
    st.bar_chart(top_cities)

    # Visualisasi Interaktif: Pilih Negara Bagian
    st.header("Visualisasi Berdasarkan Negara Bagian")
    selected_state = st.selectbox("Pilih negara bagian untuk melihat distribusi kota:", df['customer_state'].unique())
    state_city_distribution = df[df['customer_state'] == selected_state]['customer_city'].value_counts().head(10)

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=state_city_distribution.values, y=state_city_distribution.index, ax=ax)
    ax.set_title(f"Distribusi Kota di {selected_state}")
    ax.set_xlabel("Jumlah Pelanggan")
    ax.set_ylabel("Kota")
    st.pyplot(fig)

    # Statistik Tambahan
    st.header("Informasi Tambahan")
    missing_values = df.isnull().sum()
    st.write("Jumlah nilai yang hilang di setiap kolom:")
    st.write(missing_values)

except FileNotFoundError:
    st.error("File 'customers_dataset.csv' tidak ditemukan. Pastikan file berada di direktori yang benar.")
    
st.caption('Copyright (c) Fauzan Aryadih 2025')