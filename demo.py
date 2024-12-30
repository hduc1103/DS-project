import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import streamlit as st

TEMP_MODEL_PATH = 'temp_model.keras'
HUMIDITY_MODEL_PATH = 'humid_model.keras'
temp_model = load_model(TEMP_MODEL_PATH)
humidity_model = load_model(HUMIDITY_MODEL_PATH)

st.set_page_config(page_title="Weather Prediction", page_icon="🌡️", layout="wide")

st.markdown(
    """
    <style>
    body {
        background-color: #1e1e1e;
        font-family: Arial, sans-serif;
        color: #ffffff;
    }
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
        color: #ff6347;
        margin-top: 1rem;
    }
    .subheader-title {
        text-align: center;
        font-size: 1.5rem;
        color: #ffffff;
        margin-bottom: 1.5rem;
    }
    .data-list {
        margin: 0 auto;
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1rem;
    }
    .data-item {
        background: #333333;
        border-radius: 8px;
        padding: 1rem;
        text-align: left;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
        font-size: 1rem;
        color: #ffffff;
    }
    .predict-button {
        display: flex;
        justify-content: center;
        margin-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='main-title'>Weather Prediction using LSTM</div>", unsafe_allow_html=True)

def preprocess_data(file_path):
    df = pd.read_csv(file_path)

    df['temperature'] = df['temperature'].str.replace('°C', '').astype(float)
    df['humidity'] = df['humidity'].str.replace('%', '').astype(float)

    temp_scaler = MinMaxScaler(feature_range=(0, 1))
    humid_scaler = MinMaxScaler(feature_range=(0, 1))

    temp_scaled = temp_scaler.fit_transform(df['temperature'].values.reshape(-1, 1))
    humid_scaled = humid_scaler.fit_transform(df['humidity'].values.reshape(-1, 1))

    return df, temp_scaled, temp_scaler, humid_scaled, humid_scaler

def create_sequences(data, lookback):
    X, Y = [], []
    for i in range(len(data) - lookback):
        X.append(data[i:i + lookback, 0])
        Y.append(data[i + lookback, 0])
    return np.array(X), np.array(Y)

csv_file = "weather.csv"  
try:
    df, temp_scaled, temp_scaler, humid_scaled, humid_scaler = preprocess_data(csv_file)
except Exception as e:
    st.error(f"Error reading the file: {e}")
    df, temp_scaled, temp_scaler, humid_scaled, humid_scaler = None, None, None, None, None

if df is not None:
    st.markdown("<div class='subheader-title'>Latest 24-Hour Weather Data</div>", unsafe_allow_html=True)
    st.markdown("<div class='data-list'>", unsafe_allow_html=True)
    for index, row in df.iterrows():
        st.markdown(
            f"<div class='data-item'><strong>Time:</strong> {row['time']}<br><strong>Humidity:</strong> {row['humidity']}%<br><strong>Temperature:</strong> {row['temperature']}°C</div>",
            unsafe_allow_html=True
        )
    st.markdown("</div>", unsafe_allow_html=True)

if temp_scaled is not None and len(temp_scaled) >= 24:
    st.markdown("<div class='subheader-title'>Temperature Prediction</div>", unsafe_allow_html=True)
    st.markdown("<div class='predict-button'>", unsafe_allow_html=True)
    if st.button("Predict Next Hour (Temperature)", key="temp_predict_button", help="Click to predict the next hour's temperature"):
        temp_array = temp_scaled[-24:].reshape(1, 24, 1)  
        next_hour_temp_prediction = temp_model.predict(temp_array)
        
        next_hour_temperature = temp_scaler.inverse_transform(next_hour_temp_prediction)[0, 0]

        st.success(f"The predicted temperature for the next hour is: {next_hour_temperature:.2f}°C", icon="🌡️")
    st.markdown("</div>", unsafe_allow_html=True)

if humid_scaled is not None and len(humid_scaled) >= 10:
    st.markdown("<div class='subheader-title'>Humidity Prediction</div>", unsafe_allow_html=True)
    st.markdown("<div class='predict-button'>", unsafe_allow_html=True)
    if st.button("Predict Next Hour (Humidity)", key="humid_predict_button", help="Click to predict the next hour's humidity"):
        humid_array = humid_scaled[-10:].reshape(1, 10, 1)  
        next_hour_humid_prediction = humidity_model.predict(humid_array)
        
        next_hour_humidity = humid_scaler.inverse_transform(next_hour_humid_prediction)[0, 0]

        st.success(f"The predicted humidity for the next hour is: {next_hour_humidity:.2f}%", icon="💧")
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.error("The CSV file must contain at least 10 rows of humidity data.")
