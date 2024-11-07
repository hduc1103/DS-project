import time
import pandas as pd
from datetime import datetime as dt
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')

start_date = dt(2023, 10, 13)
end_date = dt(2023, 12, 31)
station_ids = ["488200", "488250"]
base_url = "https://meteologix.com/vn/observations/vietnam/weather-observation/{}-{}z.html"

allowed_hours = [22, 19, 16, 13, 10, 7, 4, 1] 
urls = [
    base_url.format(date.strftime('%Y%m%d'), f"{hour:02d}00")
    for date in pd.date_range(start_date, end_date)
    for hour in allowed_hours
]

output_file = "weather_observation/HaNoi_weather_observation_2023.csv"
batch_size = 100

def initialize_csv():
    if not os.path.exists(output_file):
        df = pd.DataFrame(columns=["date", "station_id", "time", "weather observation"])
        df.to_csv(output_file, index=False, mode='w')
    
def fetch_data(url):
    print(url)
    data = []
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    for station_id in station_ids:
        element = soup.find(attrs={"data-station-id": station_id})
        
        if element:
            title = element.get("title")
            date = url.split('/')[-1].split('-')[0]
            station_data = {"date": date, "station_id": station_id}
            
            if title:
                parts = title.split('|')
                if len(parts) >= 3:
                    time_value = parts[2].strip()
                    weather_observation = parts[0].strip()
                    station_data.update({"time": time_value, "weather observation": weather_observation})
                else:
                    station_data.update({"time": None, "weather observation": None})
            
            data.append(station_data)
            break  
    driver.quit()
    return data

def save_batch_to_csv(batch_data):
    df = pd.DataFrame(batch_data)
    df.to_csv(output_file, index=False, mode='a', header=False)

initialize_csv()

batch_data = []
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    for i, result in enumerate(executor.map(fetch_data, urls), start=1):
        batch_data.extend(result)
        
        if i % batch_size == 0 and batch_data:
            save_batch_to_csv(batch_data)
            batch_data.clear()

if batch_data:
    save_batch_to_csv(batch_data)
