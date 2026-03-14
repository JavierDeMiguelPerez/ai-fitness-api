import requests

base_url = "http://127.0.0.1:8000"

print("1. Creating user...")
resp = requests.post(f"{base_url}/users/", json={"email": "test@test.com", "password": "password"})
print(resp.status_code, resp.json())

print("2. Logging in...")
resp = requests.post(f"{base_url}/login", data={"username": "test@test.com", "password": "password"})
print(resp.status_code, resp.json())
if resp.status_code == 200:
    token = resp.json()["access_token"]
    
    print("3. Getting profile...")
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(f"{base_url}/users/me", headers=headers)
    print(resp.status_code, resp.json())
    
    print("4. Updating profile...")
    profile_data = {
        "age": 30,
        "weight_kg": 80.0,
        "height_cm": 180.0,
        "gender": "male",
        "experience_level": "intermediate",
        "primary_goal": "build_muscle"
    }
    resp = requests.put(f"{base_url}/users/me", headers=headers, json=profile_data)
    print(resp.status_code, resp.json())
