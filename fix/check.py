import pandas as pd

df = pd.read_csv('wind_direction/HaNoi_wind_direction_2023.csv')
df['datetime'] = pd.to_datetime(df['date'].astype(str) + ' ' + df['time'], format='%Y%m%d %I:%M%p')

full_range = pd.date_range(start="2023-01-01 00:00:00", end="2023-12-31 23:00:00", freq="H")

missing_datetimes = full_range.difference(df['datetime'])

if not missing_datetimes.empty:
    print("Missing hours:")
    print(missing_datetimes)
else:
    print("No hours are missing.")
