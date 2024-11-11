import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import concurrent.futures
from selenium.common.exceptions import TimeoutException, WebDriverException
import threading

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

station_ids = ["488250", "488200"]
input_file = "weather_observation/failed_urls.txt"
output_file = "weather_observation/workingurl.txt"

write_lock = threading.Lock()

def log_error(url):
    with write_lock:
        with open(input_file, 'a') as f:
            f.write(f"{url}\n")

def check_and_write_url(url):
    print(f"Checking URL: {url}")
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get(url)
        time.sleep(2)  
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        found = any(soup.find(attrs={"data-station-id": sid}) for sid in station_ids)
        
        if found:
            print(f"Station ID found in URL: {url}")
            with write_lock:
                with open(output_file, 'a') as outfile:
                    outfile.write(url + "\n")
        else:
            print(f"No matching station ID found in URL: {url}")
    except (TimeoutException, WebDriverException) as e:
        print(f"Error fetching data for URL {url}: {e}")
        log_error(url) 
    finally:
        driver.quit()

urls = []
with open(input_file, 'r') as file:
    urls = [url.strip() for url in file if url.strip()]

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(check_and_write_url, urls)
