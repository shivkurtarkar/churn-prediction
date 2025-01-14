import requests
import pytest

# Set your API URL here
API_URL = "http://localhost:30007"  # Replace with your actual API URL

@pytest.mark.parametrize("endpoint", ["/health"])  # Replace "/" with your health check endpoint if necessary
def test_api_health_check(endpoint):
    """Test to ensure the API is reachable and responds as expected."""
    url = f"{API_URL}/{endpoint}"
    try:
        response = requests.get(url)
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        print("API is reachable. Response:", response.json())
    except requests.exceptions.RequestException as e:
        pytest.fail(f"API health check failed. Error: {e}")
