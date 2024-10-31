from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import chromedriver_autoinstaller
import pandas as pd
import time as t

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

chromedriver_autoinstaller.install()

url = "https://www.accuweather.com/vi/vn/hanoi/353412/health-activities/353412"

driver = webdriver.Chrome(options=chrome_options)

driver.get(url)
t.sleep(5)  
soup = BeautifulSoup(driver.page_source, 'html.parser')

cards = soup.find_all("a", class_="index-list-card")

data = []
for card in cards:
    name_container = card.find("div", class_="index-name-container")
    name = name_container.find("div", class_="index-name").get_text()
    status = card.find("div", class_="index-status-text").get_text()
    print(f"Index Name: {name}, Index Status: {status}")
    if name and status:  
        data.append({"index_name": name, "index_status": status})

driver.quit()
output_file = "health_activities.csv"
df = pd.DataFrame(data)
df.to_csv(output_file, index=False)
print(f"Data saved to {output_file}")
