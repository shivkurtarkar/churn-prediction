import streamlit as st
import requests
import os

# Set API endpoint
API_URL = os.environ.get("API_URL", "http://localhost:8000")

# Streamlit app title
st.title("Churn Prediction")

# Collect user input
st.header("Customer Information")
trans_count = st.number_input("Transaction Count", min_value=0, step=1)
payment_method_id = st.number_input("Payment Method ID", min_value=0, step=1)
payment_plan_days = st.number_input("Payment Plan Days", min_value=0, step=1)
plan_list_price = st.number_input("Plan List Price", min_value=0.0, step=0.01)
actual_amount_paid = st.number_input("Actual Amount Paid", min_value=0.0, step=0.01)
is_auto_renew = st.selectbox("Is Auto Renew?", [0, 1])
transaction_date = st.number_input("Transaction Date (YYYYMMDD)", min_value=0, step=1)
membership_expire_date = st.number_input("Membership Expire Date (YYYYMMDD)", min_value=0, step=1)
is_cancel = st.selectbox("Is Cancelled?", [0, 1])
logs_count = st.number_input("Logs Count", min_value=0, step=1)
city = st.number_input("City", min_value=0, step=1)
bd = st.number_input("Birthdate (BD)", min_value=0, step=1)
gender = st.selectbox("Gender (0: Female, 1: Male)", [0, 1])
registered_via = st.number_input("Registered Via", min_value=0, step=1)
registration_init_time = st.number_input("Registration Init Time (YYYYMMDD)", min_value=0, step=1)

# Prediction button
if st.button("Predict Churn"):
    # Prepare payload for API
    payload = {
        "trans_count": trans_count,
        "payment_method_id": payment_method_id,
        "payment_plan_days": payment_plan_days,
        "plan_list_price": plan_list_price,
        "actual_amount_paid": actual_amount_paid,
        "is_auto_renew": is_auto_renew,
        "transaction_date": transaction_date,
        "membership_expire_date": membership_expire_date,
        "is_cancel": is_cancel,
        "logs_count": logs_count,
        "city": city,
        "bd": bd,
        "gender": gender,
        "registered_via": registered_via,
        "registration_init_time": registration_init_time,
    }
    
    # Make API request
    try:
        response = requests.post(f"{API_URL}/predict", json=payload)
        response_data = response.json()
        
        # Display prediction result
        prediction = response_data["prediction"]
        probability = response_data["probability"]
        
        st.subheader("Prediction Result")
        st.write(f"Churn Prediction: {'Yes' if prediction == 1 else 'No'}")
        st.write(f"Probability: {probability:.2f}")
    except Exception as e:
        st.error(f"Error: {e}")
