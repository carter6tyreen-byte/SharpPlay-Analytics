def run_ingestion():
    # 1. DEFINE the variable first
    endpoint = "YOUR_ACTUAL_API_URL_HERE" 
    
    # 2. THEN print it
    print(f"DEBUG: Constructing Request to URL: {endpoint}")
    
    # 3. THEN use it
    response = requests.get(endpoint, headers=headers)
    # ... rest of your code

