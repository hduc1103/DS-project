import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

station_ids = ["488250", "488200"]  
input_file = "DS-project/weather_observation/failed_urls.txt"
output_file = "DS-project/weather_observation/workingurl.txt"

def check_and_write_url(url):
    print(f"Checking URL: {url}")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(2)  

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    element = next((soup.find(attrs={"data-station-id": sid}) for sid in station_ids if soup.find(attrs={"data-station-id": sid})), None)
    
    if element:
        print(f"Station ID found in URL: {url}")
        with open(output_file, 'a') as outfile:
            outfile.write(url + "\n")  
    else:
        print(f"No matching station ID found in URL: {url}")

    driver.quit()

with open(input_file, 'r') as file:
    urls = file.readlines()
    for url in urls:
        url = url.strip()
        if url:
            check_and_write_url(url)
