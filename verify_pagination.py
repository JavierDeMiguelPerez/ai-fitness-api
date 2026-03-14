import requests

base_url = "http://127.0.0.1:8000"

print("--- Logging in to get token ---")
resp = requests.post(f"{base_url}/login", data={"username": "test@test.com", "password": "password"})

if resp.status_code != 200:
    print("Failed to login. Please create the user first.")
    exit()
    
token = resp.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

def verify_pagination():
    print("\n--- Testing Pagination on Workout History ---")
    
    # 1. Log 3 sessions
    for i in range(3):
        session_data = {
            "day_name": f"Test Day {i+1}",
            "exercises": [
                {
                    "exercise_name": "Test Exercise",
                    "sets": [{"set_number": 1, "reps": 10, "weight_kg": 50.0}]
                }
            ]
        }
        requests.post(f"{base_url}/workouts/log", headers=headers, json=session_data)
    
    # 2. Fetch with limit=2
    resp = requests.get(f"{base_url}/workouts/history?limit=2", headers=headers)
    history = resp.json()
    print(f"Limit 2: Found {len(history)} items (Expected 2)")
    
    # 3. Fetch with skip=2, limit=1
    resp = requests.get(f"{base_url}/workouts/history?skip=2&limit=1", headers=headers)
    history = resp.json()
    print(f"Skip 2, Limit 1: Found {len(history)} items (Expected 1)")

if __name__ == "__main__":
    verify_pagination()
