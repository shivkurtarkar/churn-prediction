from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

# Load the model
OUTPUT_DIR='models'
MODEL_FILE = f"{OUTPUT_DIR}/FeedforwardNN_model.joblib"

model = joblib.load(MODEL_FILE)

# Define the FastAPI app
app = FastAPI()

# Input schema
class PredictionRequest(BaseModel):
    trans_count: int
    payment_method_id: int
    payment_plan_days: int
    plan_list_price: float
    actual_amount_paid: float
    is_auto_renew: int
    transaction_date: int
    membership_expire_date: int
    is_cancel: int
    logs_count: int
    city: int
    bd: int
    gender: int
    registered_via: int
    registration_init_time: int

@app.post("/predict")
def predict(data: PredictionRequest):
    # Convert input data to NumPy array
    features = np.array([[
        data.trans_count, data.payment_method_id, data.payment_plan_days,
        data.plan_list_price, data.actual_amount_paid, data.is_auto_renew,
        data.transaction_date, data.membership_expire_date, data.is_cancel,
        data.logs_count, data.city, data.bd, data.gender, data.registered_via,
        data.registration_init_time
    ]])
    
    # Make prediction
    prediction = model.predict(features)
    probability = model.predict_proba(features).max()  # Assuming binary classification
    
    return {"prediction": int(prediction[0]), "probability": probability}
