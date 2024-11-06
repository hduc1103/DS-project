import time
import pandas as pd
from datetime import datetime as dt
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException, WebDriverException
import os

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

start_date = dt(2023, 8, 16)
end_date = dt(2023, 12, 31)
station_id = "488200"
base_url = "https://meteologix.com/vn/observations/vietnam/wind-average-10min/{}-{}z.html"

urls = [
    base_url.format(date.strftime('%Y%m%d'), f"{hour:02d}00")
    for date in pd.date_range(start_date, end_date)
    for hour in range(24)
]

output_file = "DS-project/wind_speed/HaNoi_wind_speed_2023.csv"
error_log_file = "DS-project/wind_speed/failed_urls.txt"
batch_size = 100

def initialize_csv():
    if not os.path.exists(output_file):
        df = pd.DataFrame(columns=["date", "station_id", "time", "wind speed"])
        df.to_csv(output_file, index=False, mode='w')

def log_error(url):
    with open(error_log_file, 'a') as f:
        f.write(f"{url}\n")

def fetch_data(url):
    print(url)
    data = []
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f"[data-station-id='{station_id}']"))
        )
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        element = soup.find(attrs={"data-station-id": station_id})
        
        if element:
            title = element.get("title")
            date = url.split('/')[-1].split('-')[0]
            station_data = {"date": date, "station_id": station_id}

            if title:
                parts = title.split('|')
                if len(parts) >= 3:
                    time_value = parts[2].strip()
                    wind_speed = parts[0].strip()
                    station_data.update({"time": time_value, "wind speed": wind_speed})
                else:
                    station_data.update({"time": None, "wind speed": None})
            else:
                station_data.update({"time": None, "wind speed": None})
            data.append(station_data)
    except (TimeoutException, WebDriverException) as e:
        print(f"Error fetching data for URL {url}: {e}")
        log_error(url)  
        time.sleep(10)  
    finally:
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
