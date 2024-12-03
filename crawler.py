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

start_date = dt(2023, 7, 1)
end_date = dt(2023, 12, 31)
base_url = "https://www.accuweather.com/vi/vn/hanoi/353412/health-activities/353412"

urls = [
    base_url.format(date.strftime('%Y%m%d'), f"{hour:02d}00")
    for date in pd.date_range(start_date, end_date)
    for hour in range(24)
]

output_file = "HaNoi_2023.csv"
error_log_file = "failed_urls.txt"
batch_size = 100

def initialize_csv():
    if not os.path.exists(output_file):
        df = pd.DataFrame(columns=["date", "station_id", "time", "humidity"])
        df.to_csv(output_file, index=False, mode='w')
def log_error(url):
    with open(error_log_file, 'a') as f:
        f.write(f"{url}\n")

def fetch_data(url):
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        print(soup)
    except TimeoutException:
        print(f"Timeout for URL: {url}")
        log_error(url)
    except WebDriverException as e:
        print(f"WebDriverException for URL: {url} | Error: {str(e)}")
        log_error(url)
    finally:
        driver.quit()
    return None

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
