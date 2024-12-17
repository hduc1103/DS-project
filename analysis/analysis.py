import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

temp_df = pd.read_csv('dataset/temperature.csv')
humidity_df = pd.read_csv('dataset/humidity.csv')
precipitation_df = pd.read_csv('dataset/precipitation.csv')
wind_speed_df = pd.read_csv('dataset/wind_speed.csv')
wind_direction_df = pd.read_csv('dataset/wind_direction.csv')
weather_obs_df = pd.read_csv('dataset/weather_observation.csv')

combined_df = temp_df.merge(humidity_df, on=['date', 'station_id', 'time'], suffixes=('_temp', '_hum'))
combined_df = combined_df.merge(precipitation_df, on=['date', 'station_id', 'time'])
combined_df = combined_df.merge(wind_speed_df, on=['date', 'station_id', 'time'])
combined_df = combined_df.merge(wind_direction_df, on=['date', 'station_id', 'time'])

print("Combined Data Overview:\n", combined_df.describe())

combined_df['time'] = pd.Categorical(combined_df['time'], ordered=True)

plt.figure(figsize=(10, 8))
sns.heatmap(combined_df.corr(numeric_only=True), annot=True, cmap="coolwarm")
plt.title("Correlation Matrix of Weather Parameters")
plt.savefig('correlation_matrix.png')
plt.close()

plt.figure(figsize=(12, 6))
temp_trend = combined_df.groupby('time')['temperature'].mean()
temp_trend.plot(kind='line', marker='o', linestyle='-')
plt.title("Average Temperature Trend Over Time")
plt.xlabel("Time of Day")
plt.ylabel("Temperature (°C)")
plt.xticks(rotation=45)
plt.savefig('temperature_trend.png')
plt.close()

parameters = ['temperature', 'humidity', 'precipitation', 'wind speed']
for param in parameters:
    plt.figure(figsize=(8, 5))
    sns.histplot(combined_df[param], bins=30, kde=True)
    plt.title(f"Distribution of {param.capitalize()}")
    plt.xlabel(param.capitalize())
    plt.ylabel("Frequency")
    plt.savefig(f"{param}_distribution.png")
    plt.close()

plt.figure(figsize=(10, 6))
sns.countplot(x='wind direction', data=combined_df, order=combined_df['wind direction'].value_counts().index)
plt.title("Wind Direction Frequency")
plt.xlabel("Wind Direction")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.savefig("wind_direction_frequency.png")
plt.close()


