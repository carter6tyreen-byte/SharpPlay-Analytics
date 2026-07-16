# In backend/data_collector.py
response = requests.get(endpoint, headers=headers)
print(f"DEBUG: Status Code: {response.status_code}")
print(f"DEBUG: Response Preview: {response.text[:200]}") # Shows first 200 chars

