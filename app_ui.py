import streamlit as st
import requests

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
