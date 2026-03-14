import requests

base_url = "http://127.0.0.1:8000"

print("--- Logging in to get token ---")
resp = requests.post(f"{base_url}/login", data={"username": "test@test.com", "password": "password"})

if resp.status_code != 200:
    print("Failed to login. Please create the user first.")
    exit()
    
token = resp.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}


# Add some mock data
workout_plan = {
    "plan": {
        "plan_name": "Test Workout Plan",
        "goal": "Get stronger",
        "days": [
            {
                "day_name": "Monday",
                "exercises": [
                    {"name": "Squats", "sets": 3, "reps": "10", "rest_seconds": 60}
                ]
            }
        ]
    }
}

diet_plan = {
    "plan": {
        "plan_name": "Test Diet Plan",
        "goal": "Lose weight",
        "days": [
            {
                "day_name": "Monday",
                "total_calories": 2000,
                "meals": [
                    {
                        "meal_name": "Breakfast",
                        "description": "Eggs and toast",
                        "calories": 500,
                        "protein_g": 30,
                        "carbs_g": 40,
                        "fats_g": 20
                    }
                ]
            }
        ]
    }
}


print("\n--- 0. Creating mock data ---")
resp1 = requests.post(f"{base_url}/workouts/save", headers=headers, json=workout_plan)
print(f"Workout save: {resp1.status_code}")

resp2 = requests.post(f"{base_url}/diets/save", headers=headers, json=diet_plan)
print(f"Diet save: {resp2.status_code}")


print("\n--- 1. Testing GET /workouts/saved ---")
resp = requests.get(f"{base_url}/workouts/saved", headers=headers)
print(f"Status: {resp.status_code}")
if resp.status_code == 200:
    workouts = resp.json()
    print(f"Found {len(workouts)} saved workouts.")
    if len(workouts) > 0:
        print(f"First workout name: {workouts[0]['name']}")
else:
    print(resp.json())

print("\n--- 2. Testing GET /diets/saved ---")
resp = requests.get(f"{base_url}/diets/saved", headers=headers)
print(f"Status: {resp.status_code}")
if resp.status_code == 200:
    diets = resp.json()
    print(f"Found {len(diets)} saved diets.")
    if len(diets) > 0:
        print(f"First diet name: {diets[0]['name']}")
else:
    print(resp.json())

print("\n--- 3. Testing GET /diets/history ---")
resp = requests.get(f"{base_url}/diets/history", headers=headers)
print(f"Status: {resp.status_code}")
if resp.status_code == 200:
    history = resp.json()
    print(f"Found {len(history)} meal logs.")
    if len(history) > 0:
        print(f"Most recent meal: {history[0]['food_recognized']} - Calories: {history[0]['calories']}")
else:
    print(resp.json())
