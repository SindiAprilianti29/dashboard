import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import streamlit as st
sns.set(style='dark')

# fungsi untuk menghitung total waktu penyewaan sepeda berdasarkan jam
def create_count_by_hour_df(df):
    hour_count_df = df.groupby(by="hour").agg({
        "count": "sum"
    }).reset_index()
    return hour_count_df

# fungsi untuk menghitung jumlah penyewa sepeda berdasarkan season
def create_count_by_season_df(df):
    return df.groupby(by="season").agg({
        "count": "sum"
    }).reset_index()

# fungsi untuk memfilter berdasarkan tanggal
def create_count_by_day_df(day_df):
    return day_df[(day_df['dateday'] >= "2011-01-01") & (day_df['dateday'] < "2012-12-31")]

# fungsi untuk menghitung jumlah penyewa sepeda berdasarkan tahun
def create_count_by_year_df(df):
    return df.groupby(by="year").agg({
        "count": "sum"
    }).reset_index()

# load dataset
day_df = pd.read_csv("dashboard/day_fix_df.csv")
hour_df = pd.read_csv("dashboard/hour_fix_df.csv")


min_date = day_df["dateday"].min()
max_date = day_df["dateday"].max()

with st.sidebar:
    # menambahkan logo
    st.image("https://raw.githubusercontent.com/SindiAprilianti29/dashboard/refs/heads/main/logo%20by%20pinterest.jpg")
    # mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

date_clear_df = day_df[(day_df["dateday"] >= str(start_date)) &
                (day_df["dateday"] <= str(end_date))]

count_by_hour_df = create_count_by_hour_df(hour_df)
count_by_season_df = create_count_by_season_df(date_clear_df)
count_by_day_df = create_count_by_day_df(date_clear_df)
count_by_year_df = create_count_by_year_df(date_clear_df)

st.header('Bike Rental Dashboard :sparkles:')
 # untuk jumlah penyewa sepeda berdasarkan musim
st.subheader("Jumlah penyewa sepeda berdasarkan musim")
fig, ax = plt.subplots(figsize=(10, 4))
colors = [ "#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    y="count",
    x="season",
    hue="season",
    data=count_by_season_df.sort_values(by="count", ascending=False),
    palette=colors,
    ax=ax
)

ax.set_ylabel("jumlah penyewa sepeda", fontsize=10)
ax.set_xlabel("season", fontsize=10)
ax.tick_params(axis='y', labelsize=15)
ax.tick_params(axis='x', labelsize=15)

ax = fig.gca() 
ax.set_ylim(0, count_by_season_df["count"].max()*1.1)
ax.yaxis.set_major_formatter(mticker.ScalarFormatter())
ax.ticklabel_format(style="plain", axis="y")
st.pyplot(fig)

# untuk jumlah penyewa sepeda berdasarkan jam
st.subheader("Jumlah penyewa sepeda berdasarkan jam")
fig, ax = plt.subplots(figsize=(16, 8))
max_index = count_by_hour_df["count"].idxmax()
colors = ["#D3D3D3"] * len(count_by_hour_df)
colors[max_index] = "#72BCD4"

sns.barplot(
    y="count",
    x="hour",
    data=count_by_hour_df.sort_values(by="count", ascending=False),
    palette=colors,
    ax=ax
)

ax.set_ylabel("jumlah penyewa sepeda", fontsize=10)
ax.set_xlabel("hour", fontsize=10)
ax.tick_params(axis='y', labelsize=15)
ax.tick_params(axis='x', labelsize=15)

ax = fig.gca()
ax.set_ylim(0, count_by_hour_df["count"].max()*1.1)
ax.yaxis.set_major_formatter(mticker.ScalarFormatter())
ax.ticklabel_format(style="plain", axis="y")
st.pyplot(fig)

# perbandingan jumlah penyewa sepeda pada 2011 dan 2012
st.subheader("Perbandingan jumlah penyewa sepeda di tahun 2011 dan 2012")
fig, ax = plt.subplots(figsize=(10, 4))
colors = ["#D3D3D3", "#72BCD4"]
sns.barplot(
    y="count",
    x="year",
    hue="year",
    data=count_by_year_df.sort_values(by="count", ascending=False),
    palette=colors,
    ax=ax
)

ax.set_ylabel("jumlah penyewa sepeda", fontsize=10)
ax.set_xlabel("season", fontsize=10)
ax.tick_params(axis='y', labelsize=15)
ax.tick_params(axis='x', labelsize=15)

ax = fig.gca() 
ax.set_ylim(0, count_by_year_df["count"].max()*1.1)
ax.yaxis.set_major_formatter(mticker.ScalarFormatter())
ax.ticklabel_format(style="plain", axis="y")
st.pyplot(fig)
