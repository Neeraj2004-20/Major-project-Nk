import requests

BASE_URL = "http://localhost:8000"

def test_predict():
    print("1. Registering dummy user...")
    r = requests.post(f"{BASE_URL}/api/auth/register", json={"username": "debuguser", "password": "password123"})
    print("Register response:", r.status_code, r.text)
    
    print("2. Logging in to get token...")
    # Typically auth is form data for OAuth2PasswordRequestForm
    r = requests.post(f"{BASE_URL}/api/auth/token", data={"username": "debuguser", "password": "password123"})
    print("Login response:", r.status_code, r.text)
    if r.status_code != 200:
        return
        
    token = r.json().get("access_token")
    
    print("3. Testing /predict endpoint...")
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"symbol": "AAPL", "sequence": [[1.0, 2.0, 3.0]]}
    
    r = requests.post(f"{BASE_URL}/predict", json=payload, headers=headers)
    print("Predict response:", r.status_code, r.text)

if __name__ == "__main__":
    test_predict()
