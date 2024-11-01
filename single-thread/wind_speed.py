#Ha Noi wind speed from 2011 to 2023
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time as t
import chromedriver_autoinstaller
import pandas as pd
from datetime import datetime
import os

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

chromedriver_autoinstaller.install()

base_url = "https://meteologix.com/vn/observations/vietnam/wind-average-10min/{}-{}z.html"
start_date = datetime(2011, 1, 2)
end_date = datetime(2011, 1, 2)

urls = [
    base_url.format(date.strftime('%Y%m%d'), f"{hour:02d}00")
    for date in pd.date_range(start_date, end_date)
    for hour in range(24)
]

station_id = "488200"
data = []

driver = webdriver.Chrome(options=chrome_options)
for url in urls:
    print(url)
    driver.get(url)
    t.sleep(5)  
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    element = soup.find(attrs={"data-station-id": station_id})
    
    if element:
        title = element.get("title")
        date = url.split('/')[-1].split('-')[0]
        station_data = {"date": date, "station_id": station_id}

        if title:
            parts = title.split('|')
            if len(parts) >= 3:
                time = parts[2].strip()  
                wind_speed = parts[0].strip()
                station_data.update({"time": time, "wind speed": wind_speed})
            else:
                station_data.update({"time": None, "wind speed": None})
        else:
            station_data.update({"time": None, "wind speed": None})
        data.append(station_data)
driver.quit()
output_file = "DS-project/HaNoi_wind_speed_2011_2023.csv"
file_exists = os.path.exists(output_file)

df = pd.DataFrame(data)
df.to_csv(output_file, index=False, mode='a', header=not file_exists)