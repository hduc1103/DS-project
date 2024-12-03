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
    base_url = "https://meteologix.com/vn/observations/vietnam/{}/{}-{}z.html"
    station_ids = ["488200", "488250"]
    now = datetime.now()
    utc_time = now - timedelta(hours=7) 
    
    today_str = utc_time.strftime('%Y%m%d')  
    current_hour = f"{utc_time.hour:02d}00"
    
    fields= ["wind-direction", "humidity", "temperature", "wind-speed", "weather-observation", "precipitation-total-12h"]
    urls = [
        base_url.format(field, today_str,current_hour)
        for field in fields
    ]   
    
    data = {"temperature: ": "",
            "humidity: ": "",
            "precipitation: ": "",
            "weather observation: ": "",
            "wind direction: ": "",
            "wind speed: ": ""}
    driver = webdriver.Chrome(options=chrome_options)
    for url in urls:
        driver.get(url)
        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, f"[data-station-id]" in station_ids))
        )
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        element = soup.find(attrs={"data-station-id": station_ids[0]})
        if element is None:
            element = soup.find(attrs={"data-station-id": station_ids[1]})
        if element:
            title = element.get("title")
            parts = title.split('|')
            new_data= parts[0].strip()
            cur_url = url.split('/')
            if cur_url[4]=="temperature":
                data.update({"temperature: ": {new_data}})
            elif cur_url[4]=="humidity":
                data.update({"humidity: ": {new_data}})
            elif cur_url[4]=="precipitation":
                data.update({"precipitation: ": {new_data}})
            elif cur_url[4] =="weather-observation":
                data.update({"weather observation: ": {new_data}})
            elif cur_url[4] =="wind-direction":
                data.update({"wind direction: ": {new_data}})
            elif cur_url[4] =="wind-average-10min":
                data.update({"wind speed: ": {new_data}})
    print(data)
        
def get_data():
    
    

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

