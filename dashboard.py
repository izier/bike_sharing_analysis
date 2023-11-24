import streamlit as st
import pandas as pd
import plotly.express as px

# Membaca file CSV ke dalam DataFrame
daily_df = pd.read_csv('day.csv')
hourly_df = pd.read_csv('hour.csv')\

# Konversi kolom tanggal ke format datetime
daily_df['dteday'] = pd.to_datetime(daily_df['dteday'])
hourly_df['dteday'] = pd.to_datetime(hourly_df['dteday'])

# Menghapus kolom instant dan yr
daily_df = daily_df.drop(columns = ["instant", "yr"])
hourly_df = hourly_df.drop(columns = ["instant", "yr"])

# Mengubah nama kolom
daily_df = daily_df.rename(columns={"dteday": "date",
                                    "weathersit": "weather",
                                    "mnth": "month",
                                    "hum": "humidity",
                                    "cnt": "count"})
hourly_df = hourly_df.rename(columns={"dteday": "date",
                                      "hr": "hour",
                                      "weathersit": "weather",
                                      "mnth": "month",
                                      "hum": "humidity",
                                      "cnt": "count"})

# Judul dashboard
st.title('Kesimpulan Analisis Bike Sharing')
tab1, tab2, tab3 = st.tabs(["Grafik", "Statistik", "Korelasi"])
with tab1:
    # Korelasi antara musim dan jumlah penyewaan sepeda
    st.subheader('Jumlah Penyewaan Sepeda Berdasarkan Musim')
    fig_season = px.bar(daily_df, x='season', y='count', title='Jumlah Penyewaan Sepeda Berdasarkan Musim')
    st.plotly_chart(fig_season)
    with st.expander("Lihat Keterangan"):
        st.write(
            """
                - 1: Musim Semi (Spring)
                - 2: Musim Panas (Summer)
                - 3: Musim Gugur (Fall)
                - 4: Musim Dingin (Winter)
            """
        )
    
    # Korelasi antara cuaca dan jumlah penyewaan seped
    st.subheader('Jumlah Penyewaan Sepeda Berdasarkan Cuaca')
    fig_weather = px.bar(hourly_df, x='weather', y='count', title='Jumlah Penyewaan Sepeda Berdasarkan Cuaca')
    st.plotly_chart(fig_weather)
    with st.expander("Lihat Keterangan"):
        st.write(
            """
                - 1: Cerah, Berawan
                - 2: Kabut + Berawan, Kabut
                - 3: Hujan salju singan, Hujan singan + Badai, Hujan ringan + Berawan
                - 4: Hujan berat + Hujan es + Badai + Kabut, Hujan salju + Kabut
            """
        )
    

    # Pola korelasi hari kerja, hari raya, akhir pekan, dan jam dengan jumlah penyewaan
    st.subheader('Jumlah Penyewaan Sepeda Berdasarkan Hari')
    fig_pattern = px.bar(daily_df, x='weekday', y='count', title='Pola Korelasi Hari dengan Jumlah Penyewaan Total')
    st.plotly_chart(fig_pattern)
    fig_pattern = px.bar(daily_df, x='weekday', y='casual', title='Pola Korelasi Hari dengan Jumlah Penyewaan Pengguna Santai')
    st.plotly_chart(fig_pattern)
    fig_pattern = px.bar(daily_df, x='weekday', y='registered', title='Pola Korelasi Hari dengan Jumlah Penyewaan Pengguna Terdaftar')
    st.plotly_chart(fig_pattern)
    with st.expander("Lihat Keterangan"):
        st.write(
            """
                - 0: Minggu
                - 1: Senin
                - 2: Selasa
                - 3: Rabu
                - 4: Kamis
                - 5: Jum'at
                - 6: Sabtu
            """
        )
    st.subheader('Jumlah Penyewaan Sepeda Berdasarkan Jam')
    fig_pattern = px.line(hourly_df, x='hour', y='count', title='Pola Korelasi Jam dengan Jumlah Penyewaan Total')
    st.plotly_chart(fig_pattern)
    fig_pattern = px.line(hourly_df, x='hour', y='casual', title='Pola Korelasi Jam dengan Jumlah Penyewaan Pengguna Santai')
    st.plotly_chart(fig_pattern)
    fig_pattern = px.line(hourly_df, x='hour', y='registered', title='Pola Korelasi Jam dengan Jumlah Penyewaan Pengguna Terdaftar')
    st.plotly_chart(fig_pattern)

with tab2:
    # Statistik Jumlah Pengguna Berdasarkan Musim
    st.subheader('Statistik Jumlah Pengguna Berdasarkan Musim')
    seasonal_stats = hourly_df.groupby(by='season').agg({
        'registered': ['mean','max'],
        'casual': ['mean','max'],
        'count': ['mean', 'max']
    }).sort_values(by=('count', 'mean'), ascending=False)
    st.write(seasonal_stats)

    # Statistik Jumlah Pengguna Berdasarkan Cuaca
    st.subheader('Statistik Jumlah Pengguna Berdasarkan Cuaca')
    weather_stats = hourly_df.groupby(by='weather').agg({
        'registered': ['mean','max'],
        'casual': ['mean','max'],
        'count': ['mean', 'max']
    }).sort_values(by=('count', 'mean'), ascending=False)
    st.write(weather_stats)

    # Statistik Jumlah Pengguna Berdasarkan Hari
    st.subheader('Statistik Jumlah Pengguna Berdasarkan Hari')
    day_stats = hourly_df.groupby(by='weekday').agg({
        'registered': ['mean','max'],
        'casual': ['mean','max'],
        'count': ['mean', 'max']
    }).sort_values(by=('count', 'mean'), ascending=False)
    st.write(day_stats)

    # Statistik Jumlah Pengguna Berdasarkan Jam
    st.subheader('Statistik Jumlah Pengguna Berdasarkan Jam')
    hour_stats = hourly_df.groupby(by='hour').agg({
        'registered': ['mean','max'],
        'casual': ['mean','max'],
        'count': ['mean', 'max']
    }).sort_values(by=('count', 'mean'), ascending=False)
    st.write(hour_stats)

with tab3:
    # Korelasi
    st.subheader('Korelasi Antar Variabel')
    correlation_matrix = hourly_df[['season', 'weather', 'weekday', 'holiday', 'casual', 'registered', 'count']].corr()
    st.write(correlation_matrix)