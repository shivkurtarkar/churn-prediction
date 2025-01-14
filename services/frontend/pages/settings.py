import streamlit as st
import requests
import os

# Set API endpoint
API_URL = os.environ.get("API_URL", "http://localhost:8000")

# Streamlit app title
st.title("Churn Prediction")

# Add a settings page
st.header("Settings")

# Create a button to check API health
st.text_input("Churn Prediction API Endpoint", value=API_URL, disabled=True)
check_api_button = st.button("Check API Health")
# Function to check API health
def check_api_health():
    try:
        response = requests.get(f"{API_URL}/health")
        if response.status_code == 200:
            st.success("API is up and running!")
        else:
            st.error(f"API returned an error. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to API: {e}")

# When the button is pressed, check the API health
if check_api_button:
    check_api_health()
