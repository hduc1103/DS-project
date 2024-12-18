import pandas as pd

df = pd.read_csv('dataset/wind_direction.csv', skip_blank_lines=True)

def convert_to_24_hour(time_str):
    try:
        return pd.to_datetime(time_str, format='%I:%M%p').time()
    except ValueError:
        return None  

df['converted_time'] = df['time'].apply(convert_to_24_hour)

df = df.dropna(subset=['converted_time'])

df['datetime'] = pd.to_datetime(df['date'].astype(str), errors='coerce') + pd.to_timedelta(df['converted_time'].astype(str))
df = df.dropna(subset=['datetime']) 


df = df.sort_values(by='datetime').drop(columns=['datetime', 'converted_time'])
df = df.reset_index(drop=True)

df.to_csv('tsorted_file.csv', index=False)


