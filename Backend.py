from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import tensorflow as tf
import numpy as np
import pandas as pd
from datetime import datetime as dt
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')

app = FastAPI(title="AI Model API", description="Weather App", version="1.0")

# MODEL_PATH = "my_model.h5"
# try:
#     model = tf.keras.models.load_model(MODEL_PATH)
#     print("Model loaded successfully!")
# except Exception as e:
#     print(f"Error loading model: {e}")
#     model = None

class ModelInput(BaseModel):
    input_data: list

class ModelOutput(BaseModel):
    predictions: list

@app.get("/current")
def get_current_data():
    from urllib.parse import urlparse
    
    base_url = "https://meteologix.com/vn/observations/vietnam/{}/{}-{}z.html"
    station_ids = ["488200", "488250"]
    now = datetime.now()
    utc_time = now - timedelta(hours=7)
    
    today_str = utc_time.strftime('%Y%m%d')
    current_hour = f"{utc_time.hour:02d}00"
    
    fields = ["wind-direction", "humidity", "temperature", "wind-speed"]
    urls = [base_url.format(field, today_str, current_hour) for field in fields]
    
    data = {
        "temperature: ": "",
        "humidity: ": "",
        "precipitation: ": "",
        "weather observation: ": "",
        "wind direction: ": "",
        "wind speed: ": ""
    }

    driver = webdriver.Chrome(options=chrome_options)
    try:
        for url in urls:
            print(url)
            driver.get(url)
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f"[data-station-id='{station_ids[0]}']"))
            )
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            element = None
            for station_id in station_ids:
                element = soup.find(attrs={"data-station-id": station_id})
                if element:
                    break

            if element:
                title = element.get("title")
                if title:
                    parts = title.split('|')
                    new_data = parts[0].strip()
                    path_parts = urlparse(url).path.split('/')
                    field_name = path_parts[4]
                    if field_name == "temperature":
                        data["temperature: "] = new_data
                    elif field_name == "humidity":
                        data["humidity: "] = new_data
                    elif field_name == "precipitation-total-12h":
                        data["precipitation: "] = new_data
                    elif field_name == "weather-observation":
                        data["weather observation: "] = new_data
                    elif field_name == "wind-direction":
                        data["wind direction: "] = new_data
                    elif field_name == "wind-speed":
                        data["wind speed: "] = new_data
    finally:
        driver.quit()

    print(data)
    return data

        
# def get_data():
    
@app.post("/predict", response_model=ModelInput)

# @app.post("/predict", response_model=ModelOutput)
# def predict(input_data: ModelInput):
#     if model is None:
#         raise HTTPException(status_code=500, detail="Model not loaded")
#     try:
#         data = np.array(input_data.input_data)
#         predictions = model.predict(data).tolist()

#         return ModelOutput(predictions=predictions)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

