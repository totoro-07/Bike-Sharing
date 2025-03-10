import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Load dataset
def load_data():
    df = pd.read_csv("dashboard/all_data.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

all_df = load_data()

# Helper Functions
def create_user_count_df(df):
    return df[['date', 'casual', 'registered', 'total_count']].groupby('date').sum().reset_index()

def create_days_count_df(df):
    return df[['weekday', 'total_count']].groupby('weekday').sum().reset_index()

def create_season_df(df):
    return df[['musim', 'total_count']].groupby('musim').sum().reset_index()

def create_weather_df(df):
    return df[['cuaca', 'total_count']].groupby('cuaca').sum().reset_index()

def create_user_hour_df(df):
    return df[['hour', 'total_count']].groupby('hour').sum().reset_index()

# Sidebar Filters
st.sidebar.image("dashboard/sepeda.jpg", use_container_width=True)
st.sidebar.header("Filter Data")

# Add option for users to select which analysis to view
analysis_option = st.sidebar.selectbox(
    "Pilih Analisis",
    ["Tren penggunaan bike sharing setiap tahun", "Pengaruh Musim", "Pengaruh Cuaca", "Tren Pengguna per Jam"]
)


# Data Preparation
main_df = all_df
user_count = create_user_count_df(main_df)
days_count = create_days_count_df(main_df)
season = create_season_df(main_df)
weather = create_weather_df(main_df)
user_hour = create_user_hour_df(main_df)

# Dashboard Layout
st.title('Bike Sharing System Dashboard 🚴')

# Conditional Analysis Display
if analysis_option == "Tren penggunaan bike sharing setiap tahun":
    st.subheader("Bagaimana tren penggunaan bike sharing setiap tahun?")
    
    all_df["year"] = all_df["year"].map({0: 2011, 1: 2012})
    trend_df = all_df[all_df["year"].isin([2011, 2012])].groupby(["year", "month"])['total_count'].sum().reset_index()

    fig_trend = px.line(
        trend_df, 
        x="month", 
        y="total_count", 
        color="year", 
        markers=True, 
        labels={"month": "Bulan", "total_count": "Jumlah Pengguna", "year": "Tahun"},
        title="Tren Penggunaan Bike Sharing"
    )
    
    st.plotly_chart(fig_trend, use_container_width=True)


elif analysis_option == "Pengaruh Cuaca":
    st.subheader("Bagaimana pengaruh kondisi cuaca terhadap persentase jumlah pengguna bike sharing?")
    fig_weather = px.pie(weather, names='cuaca', values='total_count', title='Users by Weather Condition')
    st.plotly_chart(fig_weather, use_container_width=True)

elif analysis_option == "Pengaruh Musim":
    st.subheader("Bagaimana pengaruh musim terhadap persentase jumlah pengguna bike sharing?")
    fig_season = px.pie(season, names='musim', values='total_count', title='Users by Season')
    st.plotly_chart(fig_season, use_container_width=True)

elif analysis_option == "Tren Pengguna per Jam":
    st.subheader("Pada jam berapa jumlah peminjaman sepeda paling tinggi?")
    fig_hour = px.line(user_hour, x="hour", y="total_count", markers=True, title="Users Per Hour")
    st.plotly_chart(fig_hour, use_container_width=True)

# Final message
st.write("Dashboard ini membantu menganalisis tren penggunaan bike-sharing berdasarkan waktu, musim, dan cuaca.")
st.caption('Copyright (c) Ahmad Radesta')
