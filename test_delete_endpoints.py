import requests

base_url = "http://127.0.0.1:8000"

print("--- Logging in to get token ---")
resp = requests.post(f"{base_url}/login", data={"username": "test@test.com", "password": "password"})

if resp.status_code != 200:
    print("Failed to login. Please create the user first.")
    exit()
    
token = resp.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

def cleanup():
    print("\n--- Starting Deletion Verification ---")
    
    # 1. Get and delete workouts
    resp = requests.get(f"{base_url}/workouts/saved", headers=headers)
    if resp.status_code == 200:
        plans = resp.json()
        print(f"Found {len(plans)} workouts to delete.")
        for p in plans:
            del_resp = requests.delete(f"{base_url}/workouts/saved/{p['id']}", headers=headers)
            print(f"Deleting workout {p['id']}: {del_resp.status_code}")
    
    # 2. Get and delete workout history
    resp = requests.get(f"{base_url}/workouts/history", headers=headers)
    if resp.status_code == 200:
        sessions = resp.json()
        print(f"Found {len(sessions)} workout sessions to delete.")
        for s in sessions:
            del_resp = requests.delete(f"{base_url}/workouts/history/{s['id']}", headers=headers)
            print(f"Deleting session {s['id']}: {del_resp.status_code}")

    # 3. Get and delete diets
    resp = requests.get(f"{base_url}/diets/saved", headers=headers)
    if resp.status_code == 200:
        diets = resp.json()
        print(f"Found {len(diets)} diets to delete.")
        for d in diets:
            del_resp = requests.delete(f"{base_url}/diets/saved/{d['id']}", headers=headers)
            print(f"Deleting diet {d['id']}: {del_resp.status_code}")

    # 4. Get and delete diet history
    resp = requests.get(f"{base_url}/diets/history", headers=headers)
    if resp.status_code == 200:
        logs = resp.json()
        print(f"Found {len(logs)} meal logs to delete.")
        for l in logs:
            del_resp = requests.delete(f"{base_url}/diets/history/{l['id']}", headers=headers)
            print(f"Deleting log {l['id']}: {del_resp.status_code}")

    print("\n--- Final Verification (should all be 0 or empty) ---")
    print(f"Workouts: {len(requests.get(f'{base_url}/workouts/saved', headers=headers).json())}")
    print(f"Sessions: {len(requests.get(f'{base_url}/workouts/history', headers=headers).json())}")
    print(f"Diets: {len(requests.get(f'{base_url}/diets/saved', headers=headers).json())}")
    print(f"Logs: {len(requests.get(f'{base_url}/diets/history', headers=headers).json())}")

if __name__ == "__main__":
    cleanup()
