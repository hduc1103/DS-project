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

station_id = "488250"
input_file = "DS-project/weather_observation/failed_urls.txt"
output_file = "DS-project/weather_observation/HaNoi_weather_observation_2023.csv"
batch_size = 100

def initialize_csv():
    if not os.path.exists(output_file):
        df = pd.DataFrame(columns=["date", "station_id", "time", "humidity"])
        df.to_csv(output_file, index=False, mode='w')

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
                    humidity = parts[0].strip()
                    station_data.update({"time": time_value, "humidity": humidity})
                else:
                    station_data.update({"time": None, "humidity": None})
            else:
                station_data.update({"time": None, "humidity": None})
            data.append(station_data)
    except (TimeoutException, WebDriverException) as e:
        print(f"Error fetching data for URL {url}: {e}")
        time.sleep(10)  
    finally:
        driver.quit()
    return data

def save_batch_to_csv(batch_data):
    df = pd.DataFrame(batch_data)
    df.to_csv(output_file, index=False, mode='a', header=False)  

initialize_csv() 

batch_data = []
with open(input_file, 'r') as file:
    urls = file.readlines()
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for i, result in enumerate(executor.map(fetch_data, urls), start=1):
            batch_data.extend(result)
            
            if i % batch_size == 0 and batch_data:
                save_batch_to_csv(batch_data)
                batch_data.clear()

if batch_data:
    save_batch_to_csv(batch_data)
