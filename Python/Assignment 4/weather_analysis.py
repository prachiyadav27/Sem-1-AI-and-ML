# Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Task 1: Load and Inspect
df = pd.read_csv('farrukhnagar_visualcrossing_2023-2024.csv')  # Your downloaded file
print("Dataset shape:", df.shape)
print(df.head())
print(df.info())
print(df.describe())

# Convert datetime to datetime (Visual Crossing uses 'datetime' column)
df['datetime'] = pd.to_datetime(df['datetime'])
df = df[(df['datetime'] >= '2023-01-01') & (df['datetime'] <= '2024-12-31')]

# Rename columns for simplicity (match assignment: temperature, rainfall, humidity)
df = df.rename(columns={
    'temp': 'temperature',      # Mean temp
    'precip': 'rainfall',       # Daily precip total
    'humidity': 'humidity'      # Already matches
})

# Task 2: Cleaning
# Handle missing values (rare in Visual Crossing, but fill if any)
numeric_cols = ['temperature', 'rainfall', 'humidity']
for col in numeric_cols:
    if col in df.columns:
        df[col].fillna(df[col].mean(), inplace=True)
df['rainfall'] = df['rainfall'].fillna(0)  # No negative rain
df = df.dropna(subset=['temperature', 'rainfall', 'humidity'])  # Drop incomplete rows

# Select relevant columns
df = df[['datetime', 'temperature', 'rainfall', 'humidity', 'tempmax', 'tempmin']]  # Add max/min if needed
df.set_index('datetime', inplace=True)

print("Cleaned data shape:", df.shape)
print(df.head())

# Task 3: Statistical Analysis with NumPy
# Daily stats
daily_mean_temp = np.mean(df['temperature'])
daily_min_temp = np.min(df['tempmin'])
daily_max_temp = np.max(df['tempmax'])
daily_std_temp = np.std(df['temperature'])

print(f"Daily Stats (2023-2024): Mean Temp: {daily_mean_temp:.2f}°C, Min: {daily_min_temp:.2f}°C, Max: {daily_max_temp:.2f}°C, Std: {daily_std_temp:.2f}°C")

# Monthly stats (resample)
monthly_temp = df['temperature'].resample('M').agg(['mean', 'min', 'max', 'std'])
monthly_rain = df['rainfall'].resample('M').sum()  # Total rain
print("Monthly Temperature Stats:\n", monthly_temp.head())

# Task 5: Grouping and Aggregation
# Group by month
df['month'] = df.index.month
monthly_agg = df.groupby('month').agg({
    'temperature': ['mean', 'min', 'max'],
    'rainfall': 'sum',
    'humidity': 'mean'
}).round(2)
print("Monthly Aggregates:\n", monthly_agg)

# Seasons (Haryana-specific: Winter Dec-Feb, Summer Mar-May, Monsoon Jun-Sep, Post-Monsoon Oct-Nov)
season_map = {12: 'Winter', 1: 'Winter', 2: 'Winter',
              3: 'Summer', 4: 'Summer', 5: 'Summer',
              6: 'Monsoon', 7: 'Monsoon', 8: 'Monsoon', 9: 'Monsoon',
              10: 'Post-Monsoon', 11: 'Post-Monsoon'}
df['season'] = df.index.month.map(season_map)
seasonal_stats = df.groupby('season').agg({
    'temperature': ['mean', 'max'],
    'rainfall': 'sum',
    'humidity': 'mean'
}).round(2)
print("Seasonal Stats:\n", seasonal_stats)

# Task 4: Visualizations with Matplotlib
plt.style.use('default')

# Line chart: Daily temperature trends (using mean temp)
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['temperature'], label='Mean Temperature (°C)', color='orange')
plt.title('Daily Temperature Trends in Farrukhnagar (2023-2024) - Visual Crossing Data')
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.legend()
plt.grid(True)
plt.savefig('daily_temp_trends_vc.png', dpi=300, bbox_inches='tight')
plt.show()

# Bar chart: Monthly rainfall totals
plt.figure(figsize=(10, 6))
monthly_rain.plot(kind='bar', color='blue', ax=plt.gca())
plt.title('Monthly Rainfall Totals in Farrukhnagar (2023-2024)')
plt.xlabel('Month')
plt.ylabel('Rainfall (mm)')
plt.xticks(rotation=45)
plt.savefig('monthly_rainfall_bar_vc.png', dpi=300, bbox_inches='tight')
plt.show()

# Scatter plot: Humidity vs. Temperature
plt.figure(figsize=(8, 6))
plt.scatter(df['temperature'], df['humidity'], alpha=0.6, color='green')
plt.title('Humidity vs. Temperature in Farrukhnagar (2023-2024)')
plt.xlabel('Temperature (°C)')
plt.ylabel('Humidity (%)')
plt.grid(True)
plt.savefig('humidity_vs_temp_scatter_vc.png', dpi=300, bbox_inches='tight')
plt.show()

# Combined subplots: Temp line + Rain bar
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
df['temperature'].plot(ax=ax1, title='Temperature and Rainfall Trends in Farrukhnagar (2023-2024)', color='red')
ax1.set_ylabel('Temperature (°C)')
ax1.grid(True)
monthly_rain.plot(kind='bar', ax=ax2, color='blue')
ax2.set_ylabel('Rainfall (mm)')
ax2.set_xlabel('Month')
ax2.grid(True)
plt.tight_layout()
plt.savefig('combined_temp_rain_vc.png', dpi=300, bbox_inches='tight')
plt.show()

# Task 6: Export
df.to_csv('cleaned_farrukhnagar_visualcrossing_2023-2024.csv')
print("Exported cleaned CSV and PNG plots.")

# Sample Insights for Report
print("\nSample Insights (Update with your stats):")
print("- Average annual temp: ~26-28°C, with summer peaks >42°C (May-June).")
print("- Monsoon rainfall: ~500-700mm total (Jul-Aug), vital for Haryana agriculture.")
print("- Trend: Slightly rising max temps in 2024, possible heatwave indicator.")
print("- Anomaly: Dry spells in early 2023 winter, low humidity <40%.")