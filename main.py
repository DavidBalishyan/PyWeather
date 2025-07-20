import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import date

DATA_DIR = "data"
PLOTS_DIR = "target"

def ensure_dirs():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(PLOTS_DIR, exist_ok=True)

def save_plot(filename):
    plt.savefig(os.path.join(PLOTS_DIR, filename))
    plt.close()

def download_weather_data():
    # Coordinates for Yerevan, Armenia
    latitude = 40.1811
    longitude = 44.5136

    today = date.today()
    start_date = "2025-01-01"
    end_date = today.isoformat()

    url = (
        "https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={latitude}&longitude={longitude}"
        f"&start_date={start_date}&end_date={end_date}"
        "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
        "&timezone=Asia/Yerevan"
    )

    print("Downloading weather data from Open-Meteo API...")
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    if 'daily' not in data:
        raise ValueError("No daily data found in API response")

    df = pd.DataFrame(data['daily'])
    df['temperature'] = (df['temperature_2m_max'] + df['temperature_2m_min']) / 2
    df = df.rename(columns={'time': 'date', 'precipitation_sum': 'rainfall'})
    df = df[['date', 'temperature', 'rainfall']]

    csv_path = os.path.join(DATA_DIR, 'weather_data.csv')
    df.to_csv(csv_path, index=False)
    print(f"Saved weather data to {csv_path}")

def analyze_weather_data():
    csv_path = os.path.join(DATA_DIR, 'weather_data.csv')
    print(f"Loading {csv_path}...")
    df = pd.read_csv(csv_path)

    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df.ffill(inplace=True)

    monthly_avg = df.resample('ME').mean()
    df['temp_7d_avg'] = df['temperature'].rolling(window=7).mean()

    df['month'] = df.index.month
    monthly_mean_temp = df.groupby('month')['temperature'].transform('mean')
    df['temp_anomaly'] = df['temperature'] - monthly_mean_temp

    # Plot 1: Daily Temp + Rolling Average
    plt.figure(figsize=(12,6))
    plt.plot(df.index, df['temperature'], label='Daily Temp')
    plt.plot(df.index, df['temp_7d_avg'], label='7-Day Rolling Avg', linewidth=3)
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.title('Daily Temperature and 7-Day Rolling Average')
    plt.legend()
    save_plot('daily_temperature.png')

    # Plot 2: Monthly Rainfall
    plt.figure(figsize=(10,5))
    monthly_avg['rainfall'].plot(kind='bar', color='skyblue')
    plt.xlabel('Month')
    plt.ylabel('Average Rainfall (mm)')
    plt.title('Monthly Average Rainfall')
    save_plot('monthly_rainfall.png')

    # Plot 3: Histogram
    plt.figure(figsize=(8,5))
    plt.hist(df['temperature'], bins=20, color='coral', edgecolor='black')
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Frequency')
    plt.title('Temperature Distribution')
    save_plot('temperature_distribution.png')

    # Plot 4: Heatmap
    df['day'] = df.index.day
    pivot = df.pivot_table(index='month', columns='day', values='temp_anomaly', aggfunc='mean')
    plt.figure(figsize=(15,6))
    sns.heatmap(pivot, cmap='coolwarm', center=0, cbar_kws={'label': 'Temp Anomaly (°C)'})
    plt.title('Heatmap of Temperature Anomalies by Month and Day')
    plt.xlabel('Day of Month')
    plt.ylabel('Month')
    save_plot('temperature_anomaly_heatmap.png')

    # Stats
    print("\nWeather Statistics:")
    print(f"Average Temperature: {df['temperature'].mean():.2f} °C")
    print(f"Max Temperature: {df['temperature'].max():.2f} °C")
    print(f"Min Temperature: {df['temperature'].min():.2f} °C")
    print(f"Total Rainfall: {df['rainfall'].sum():.2f} mm")

def main():
    ensure_dirs()
    csv_path = os.path.join(DATA_DIR, 'weather_data.csv')
    if not os.path.isfile(csv_path):
        download_weather_data()
    else:
        print(f"{csv_path} already exists. Skipping download.")
    analyze_weather_data()

if __name__ == "__main__":
    main()
