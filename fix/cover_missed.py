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
import time

missing_hours = [
    "2023-01-07 03:00:00", "2023-01-27 18:00:00",
    "2023-01-31 21:00:00", "2023-02-02 08:00:00",
    "2023-02-14 06:00:00", "2023-02-16 15:00:00",
    "2023-02-20 00:00:00", "2023-02-20 23:00:00",
    "2023-03-11 11:00:00", "2023-03-12 11:00:00",
    "2023-03-13 15:00:00", "2023-03-15 02:00:00",
    "2023-03-15 14:00:00", "2023-03-15 15:00:00",
    "2023-03-15 17:00:00", "2023-03-15 20:00:00",
    "2023-03-15 21:00:00", "2023-03-16 08:00:00",
    "2023-03-16 09:00:00", "2023-04-02 15:00:00",
    "2023-04-27 11:00:00", "2023-06-12 11:00:00",
    "2023-06-14 14:00:00", "2023-06-17 15:00:00",
    "2023-06-23 20:00:00", "2023-07-02 23:00:00",
    "2023-07-09 02:00:00", "2023-07-29 08:00:00",
    "2023-08-01 15:00:00", "2023-08-02 20:00:00",
    "2023-08-03 11:00:00", "2023-08-04 23:00:00",
    "2023-08-05 20:00:00", "2023-08-07 09:00:00",
    "2023-08-10 18:00:00", "2023-08-12 00:00:00",
    "2023-08-13 06:00:00", "2023-08-14 03:00:00",
    "2023-08-15 02:00:00", "2023-08-16 02:00:00",
    "2023-08-18 08:00:00", "2023-08-19 08:00:00",
    "2023-08-19 14:00:00", "2023-08-20 05:00:00",
    "2023-08-25 08:00:00", "2023-08-25 23:00:00",
    "2023-08-28 05:00:00", "2023-08-28 09:00:00",
    "2023-08-29 17:00:00", "2023-09-02 00:00:00",
    "2023-09-02 21:00:00", "2023-09-05 05:00:00",
    "2023-09-10 23:00:00", "2023-09-13 00:00:00",
    "2023-09-14 09:00:00", "2023-09-15 03:00:00",
    "2023-09-15 05:00:00", "2023-09-15 18:00:00",
    "2023-09-17 09:00:00", "2023-09-18 17:00:00",
    "2023-10-05 18:00:00", "2023-10-29 03:00:00",
    "2023-10-29 23:00:00", "2023-10-30 02:00:00",
    "2023-11-08 00:00:00", "2023-11-17 05:00:00",
    "2023-12-03 02:00:00", "2023-12-03 12:00:00",
    "2023-12-03 15:00:00", "2023-12-27 20:00:00"
]


missing_hours = [dt.strptime(hour, "%Y-%m-%d %H:%M:%S") for hour in missing_hours]

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')

station_id = "488200"
base_url = "https://meteologix.com/vn/observations/vietnam/wind-direction/{}-{}z.html"

urls = [
    base_url.format(date.strftime('%Y%m%d'), f"{date.hour:02d}00")
    for date in missing_hours
]

output_file = "wind_direction/HaDongretry.csv"
error_log_file = "wind_direction/failed_missed_url.txt"
batch_size = 100

def initialize_csv():
    if not os.path.exists(output_file):
        df = pd.DataFrame(columns=["date", "station_id", "time", "wind direction"])
        df.to_csv(output_file, index=False, mode='w')

def log_error(url):
    with open(error_log_file, 'a') as f:
        f.write(f"{url}\n")

def fetch_data(url):
    """
    Fetches data from a given URL and returns a list of dictionaries containing the date, station id, time, and temperature.
    """
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
                    temperature = parts[0].strip()
                    station_data.update({"time": time_value, "wind direction": temperature})
                else:
                    station_data.update({"time": None, "wind direction": None})
            else:
                station_data.update({"time": None, "wind direction": None})
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
