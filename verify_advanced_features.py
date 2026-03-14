import requests

BASE_URL = "http://127.0.0.1:8000"
EMAIL = "test@test.com"
PASSWORD = "password"
NEW_PASSWORD = "newpassword456"

def test_advanced_features():
    print("--- Logging in ---")
    login_data = {"username": EMAIL, "password": PASSWORD}
    response = requests.post(f"{BASE_URL}/login", data=login_data)
    if response.status_code != 200:
        print("Login failed, attempting to create user...")
        signup_resp = requests.post(f"{BASE_URL}/users/", json={"email": EMAIL, "password": PASSWORD})
        if signup_resp.status_code in [200, 201, 400]: # 400 if already exists but login failed for some reason
            print("User created or already exists, logging in again...")
            response = requests.post(f"{BASE_URL}/login", data=login_data)
        else:
            print(f"Signup failed: {signup_resp.text}")
            return
            
    if response.status_code != 200:
        print(f"Login failed even after signup attempt: {response.text}")
        return

    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Test Workout Editing
    print("\n--- Testing Workout Editing ---")
    session_data = {
        "day_name": "Monday Edit Test",
        "exercises": [
            {
                "exercise_name": "Squats",
                "sets": [{"set_number": 1, "reps": 10, "weight_kg": 60}]
            }
        ]
    }
    log_resp = requests.post(f"{BASE_URL}/workouts/log", json=session_data, headers=headers)
    session_id = log_resp.json()["session_id"]
    print(f"Logged session {session_id}")

    update_data = {
        "day_name": "Monday Updated",
        "exercises": [
            {
                "exercise_name": "Squats",
                "sets": [{"set_number": 1, "reps": 12, "weight_kg": 65}] # Changed reps and weight
            }
        ]
    }
    update_resp = requests.put(f"{BASE_URL}/workouts/history/{session_id}", json=update_data, headers=headers)
    print(f"Update response: {update_resp.json()}")

    history_resp = requests.get(f"{BASE_URL}/workouts/history", headers=headers)
    latest = history_resp.json()[0]
    if latest["day_name"] == "Monday Updated" and latest["exercises"][0]["sets"][0]["reps"] == 12:
        print("Workout Update SUCCESSFUL")
    else:
        print("Workout Update FAILED")

    # 2. Test Password Recovery
    print("\n--- Testing Password Recovery ---")
    forgot_resp = requests.post(f"{BASE_URL}/forgot-password", json={"email": EMAIL})
    reset_token = forgot_resp.json().get("token")
    print(f"Reset token received: {reset_token}")

    reset_resp = requests.post(f"{BASE_URL}/reset-password", json={
        "token": reset_token,
        "new_password": NEW_PASSWORD
    })
    print(f"Reset response: {reset_resp.json()}")

    print("--- Verifying login with new password ---")
    new_login_resp = requests.post(f"{BASE_URL}/login", data={"username": EMAIL, "password": NEW_PASSWORD})
    if new_login_resp.status_code == 200:
        print("Password Reset SUCCESSFUL")
    else:
        print("Password Reset FAILED")
        
    # Revert password for future tests if needed
    requests.post(f"{BASE_URL}/forgot-password", json={"email": EMAIL}) # get new token
    # (Simplified revert for the test script)

if __name__ == "__main__":
    test_advanced_features()
