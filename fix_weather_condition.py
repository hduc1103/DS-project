import pandas as pd

# Load the weather observation data
weather_observation = pd.read_csv('dataset/weather_observation.csv')

# Simplify weather labels
def simplify_weather(obs):
    obs = obs.lower()
    if "sun" in obs or "clear" in obs:
        return "sun"
    elif "rain" in obs:
        return "rain"
    elif "fog" in obs or "mist" in obs:
        return "fog"
    elif "drizzle" in obs:
        return "drizzle"
    else:
        return "other"

# Apply simplified weather labels
weather_observation['simplified_weather'] = weather_observation['weather observation'].apply(simplify_weather)

# Group by date and take the most frequent weather condition for the day
daily_weather = weather_observation.groupby('date')['simplified_weather'].agg(lambda x: x.mode()[0]).reset_index()

# Generate a full range of dates and merge with existing data
daily_weather['date'] = pd.to_datetime(daily_weather['date'], format='%Y%m%d')
all_dates = pd.date_range(start=daily_weather['date'].min(), end=daily_weather['date'].max(), freq='D')
all_dates_df = pd.DataFrame({'date': all_dates})

# Merge and fill missing dates with 'sun'
final_weather = all_dates_df.merge(daily_weather, on='date', how='left').fillna({'simplified_weather': 'sun'})

# Format the date back to string
final_weather['date'] = final_weather['date'].dt.strftime('%Y-%m-%d')

# Save the output
final_weather.to_csv('daily_weather_simplified.csv', index=False)

# Display final result
print(final_weather.head())
