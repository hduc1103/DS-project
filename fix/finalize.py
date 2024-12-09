import pandas as pd
import glob
import os
import re

csv_folder = 'final(sorted)/wind_direction' 

# Get list of all CSV files in the folder
csv_files = glob.glob(os.path.join(csv_folder, '*.csv'))

dataframes = []

for file in csv_files:
    df = pd.read_csv(file)
    
    # Replace specific string with -1
    df['wind direction'] = df['wind direction'].replace(
        to_replace='low winds from changing directions', value='-1'
    )
    
    # Process rows that are not '-1' or 'calm'
    df['wind direction'] = df['wind direction'].apply(
        lambda x: int(re.search(r'\d+', x).group()) if pd.notnull(x) and re.search(r'\d+', x) else x
    )
    
    # Append processed DataFrame to the list
    dataframes.append(df)

# Combine all DataFrames into one
combined_df = pd.concat(dataframes, ignore_index=True)

# Save the combined DataFrame to a CSV file
output_file = 'dataset/wind_direction.csv'
combined_df.to_csv(output_file, index=False)

print(f"Combined data saved to {output_file}")
