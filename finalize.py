import pandas as pd

# File paths
temp_file = 'dataset/temperature.csv'
wind_file = 'dataset/wind_speed.csv'
precip_file = 'dataset/precipitation.csv'
weather_file = 'dataset/daily_weather_simplified.csv'

# Load data
temp_df = pd.read_csv(temp_file)
wind_df = pd.read_csv(wind_file)
precip_df = pd.read_csv(precip_file)
weather_df = pd.read_csv(weather_file)

# Step 1: Clean and process temperature
temp_df['date'] = pd.to_datetime(temp_df['date'], format='%Y%m%d').dt.date
temp_daily = temp_df.groupby('date')['temperature'].agg(['max', 'min']).reset_index()
temp_daily.rename(columns={'max': 'max_temperature', 'min': 'min_temperature'}, inplace=True)

# Step 2: Clean and process wind speed
wind_df['date'] = pd.to_datetime(wind_df['date'], format='%Y%m%d').dt.date
wind_daily = wind_df.groupby('date')['wind speed'].mean().round(1).reset_index()
wind_daily.rename(columns={'wind speed': 'avg_wind_speed'}, inplace=True)

# Step 3: Clean and process precipitation
precip_df['date'] = pd.to_datetime(precip_df['date'], format='%Y%m%d').dt.date
precip_daily = precip_df.groupby('date')['precipitation'].mean().round(1).reset_index()
precip_daily.rename(columns={'precipitation': 'avg_precipitation'}, inplace=True)

# Step 4: Clean and process weather observation
weather_df['date'] = pd.to_datetime(weather_df['date']).dt.date
weather_df = weather_df.sort_values('date')

# Fill missing weather conditions using the previous day, default to 'sun'
def fill_weather_conditions(weather):
    last_weather = 'sun'
    filled_weather = []
    for condition in weather:
        if pd.isnull(condition):
            filled_weather.append(last_weather)
        else:
            filled_weather.append(condition)
            last_weather = condition
    return filled_weather

weather_df['weather'] = fill_weather_conditions(weather_df['weather'])

# Step 5: Merge all datasets
combined_df = temp_daily.merge(wind_daily, on='date', how='outer')
combined_df = combined_df.merge(precip_daily, on='date', how='outer')
combined_df = combined_df.merge(weather_df, on='date', how='outer')

# Fill remaining NaN values
combined_df['weather'].fillna('sun', inplace=True)
combined_df.fillna(0, inplace=True)  # Fill numerical missing values with 0

# Final result
combined_df.sort_values('date', inplace=True)
print(combined_df.head())

# Save to CSV
combined_df.to_csv('combined_weather_data.csv', index=False)
