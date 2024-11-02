import pandas as pd

# Load the CSV file
df = pd.read_csv('wind_direction/HaNoi_wind_direction_2023.csv', skip_blank_lines=True)

# Define a function to convert 'time' column to 24-hour format
def convert_to_24_hour(time_str):
    try:
        return pd.to_datetime(time_str, format='%I:%M%p').time()
    except ValueError:
        return None  

df['converted_time'] = df['time'].apply(convert_to_24_hour)

df = df.dropna(subset=['converted_time'])

df['datetime'] = pd.to_datetime(df['date'].astype(str)) + pd.to_timedelta(df['converted_time'].astype(str))
df = df.sort_values(by='datetime').drop(columns=['datetime', 'converted_time'])
df = df.reset_index(drop=True)
df.to_csv('sorted_file.csv', index=False)
