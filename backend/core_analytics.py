def run_ingestion():
    # ... after response = requests.get(...)
    data = response.json()
    
    # Check if the API returned an envelope (e.g., {"results": [], "errors": None})
    print(f"DEBUG: Full API response: {data}") 
    
    return data
