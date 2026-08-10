import requests
import json

base_url = "http://127.0.0.1:8000"

tests = [
    ("/predict/crop-recommendation", {"location": "Hyderabad"}),
    ("/predict/climate-risk", {"location": "Hyderabad", "crop": "Rice"}),
    ("/predict/yield", {"location": "Guntur", "crop": "Cotton", "area": 1.0}),
    ("/predict/irrigation", {"location": "Warangal", "crop": "Maize", "growth_stage": "Development"}),
    ("/predict/market-price", {"location": "Krishna", "commodity": "Banana", "arrival_quantity": 100.0})
]

for endpoint, payload in tests:
    print(f"Testing {endpoint}...")
    try:
        r = requests.post(base_url + endpoint, json=payload)
        if r.status_code == 200:
            print(f"SUCCESS")
            # print first 100 chars to avoid huge output
            out = json.dumps(r.json())
            print(f"Response: {out[:100]}...")
        else:
            print(f"FAILED ({r.status_code})")
            print(f"Error: {r.text}")
    except Exception as e:
        print(f"ERROR: {e}")
    print("-" * 40)
