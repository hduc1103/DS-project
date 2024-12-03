import time
import pandas as pd
from datetime import datetime as dt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

station_id = "488250"
input_file = "wind_speed/failed_urls.txt"
output_file = "wind_speed/HaNoi_wind_speed_2023.csv"

def initialize_csv():
    if not os.path.exists(output_file):
        df = pd.DataFrame(columns=["date", "station_id", "time", "humidity"])
        df.to_csv(output_file, index=False, mode='w')

def fetch_data(url):
    print(f"Fetching data for URL: {url}")
    data = []
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(5)  

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

    driver.quit()
    return data

def save_to_csv(data):
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False, mode='a', header=not os.path.exists(output_file))

initialize_csv()
data_to_save = []
with open(input_file, 'r') as file:
    urls = file.readlines()
    for url in urls:
        url = url.strip()
        if url:
            result = fetch_data(url)
            data_to_save.extend(result)
            save_to_csv(data_to_save)
            data_to_save.clear()
