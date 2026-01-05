import streamlit as st
import requests
import time
import numpy as np
import pandas as pd
import random

st.title('Solar Power Generation Prediction')

# Input fields for user data
st.write('Enter the values for prediction:')
input_values = []
for i in range(5):
    value = st.number_input(f'Value {i+1}', value=0.0)
    input_values.append(value)

if st.button('Predict'):
    api_url = 'http://127.0.0.1:8001/predict'  # Updated to match new Uvicorn port
    try:
        response = requests.post(api_url, json={'data': input_values})
        if response.status_code == 200:
            prediction = response.json()['prediction']
            st.write(f'Predicted Daily Yield: {prediction[0]:.2f} MW')
        else:
            st.error('Error in prediction. Check API.')
    except requests.exceptions.ConnectionError:
        st.error("Failed to connect to the prediction API. Ensure it's running.")

st.write("### Live Time Series Prediction")
if st.button("Start Live Prediction"):
    api_url = 'http://127.0.0.1:8001/predict'
    st.write("Fetching new inputs every second...")
    chart_placeholder = st.empty()
    time_series_data = []
    iteration = 0
    
    while True:
        # Generate or fetch input values
        # Use a stable baseline and small random noise, with occasional anomalies
        baseline = [3.0, 3.1, 3.2, 3.2, 3.0]
        noise = [random.uniform(-0.1, 0.1) for _ in range(5)]
        simulated_input = [b + n for b, n in zip(baseline, noise)]

        # Introduce a random anomaly in one of the five inputs (10% chance)
        if random.random() < 0.1:
            idx = random.randint(0, 4)
            simulated_input[idx] += random.uniform(1.0, 2.0)

        # Call the prediction API
        try:
            response = requests.post(api_url, json={"data": simulated_input})
            if response.status_code == 200:
                prediction_value = response.json()["prediction"][0]
                time_series_data.append((iteration, prediction_value))
            else:
                st.error("Error in prediction. Check API.")
                break
        except requests.exceptions.ConnectionError:
            st.error("Failed to connect to the prediction API. Ensure it's running.")
            break
        
        # Create a DataFrame and plot it
        df = pd.DataFrame(time_series_data, columns=["Time", "Predicted"])
        df.set_index("Time", inplace=True)
        chart_placeholder.line_chart(df["Predicted"])
        
        iteration += 1
        time.sleep(1)
