import pytest
from fastapi.testclient import TestClient
from api.api import app

# Create a TestClient for the FastAPI app
client = TestClient(app)

# Sample payload for testing
valid_payload = {
    "trans_count": 10,
    "payment_method_id": 1,
    "payment_plan_days": 30,
    "plan_list_price": 99.99,
    "actual_amount_paid": 99.99,
    "is_auto_renew": 1,
    "transaction_date": 20230101,
    "membership_expire_date": 20231231,
    "is_cancel": 0,
    "logs_count": 50,
    "city": 1,
    "bd": 25,
    "gender": 1,
    "registered_via": 4,
    "registration_init_time": 20220101,
}

# Test cases
def test_predict_success():
    """Test the /predict endpoint with valid input."""
    response = client.post("/predict", json=valid_payload)
    assert response.status_code == 200
    response_data = response.json()
    assert "prediction" in response_data
    assert "probability" in response_data
    assert isinstance(response_data["prediction"], int)
    assert 0 <= response_data["probability"] <= 1

def test_predict_invalid_payload():
    """Test the /predict endpoint with missing or invalid input."""
    invalid_payload = valid_payload.copy()
    del invalid_payload["trans_count"]  # Remove a required field
    response = client.post("/predict", json=invalid_payload)
    assert response.status_code == 422  # Unprocessable Entity

def test_predict_extra_fields():
    """Test the /predict endpoint with extra fields in the input."""
    extra_payload = valid_payload.copy()
    extra_payload["extra_field"] = "unexpected"
    response = client.post("/predict", json=extra_payload)
    assert response.status_code == 200
    response_data = response.json()
    assert "prediction" in response_data
    assert "probability" in response_data

def test_predict_edge_cases():
    """Test the /predict endpoint with edge case values."""
    edge_payload = valid_payload.copy()
    edge_payload["bd"] = -1  # Set an edge value for bd (age)
    response = client.post("/predict", json=edge_payload)
    assert response.status_code == 200
    response_data = response.json()
    assert "prediction" in response_data
    assert "probability" in response_data

def test_predict_empty_payload():
    """Test the /predict endpoint with an empty payload."""
    response = client.post("/predict", json={})
    assert response.status_code == 422  # Unprocessable Entity
