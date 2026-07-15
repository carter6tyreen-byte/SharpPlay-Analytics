def fetch_mlb_data():
    # 1. Public API (No headers)
    url_public = "https://statsapi.mlb.com/api/v1/schedule/live?sportId=1"
    
    # 2. Private API (Requires headers)
    url_private = "YOUR_PRIVATE_API_ENDPOINT"
    private_headers = {"Authorization": f"Bearer {os.getenv('SPORTS_API_KEY')}"}
    
    results = {"public": None, "private": None}
    
    try:
        # Request for public API
        resp_public = requests.get(url_public)
        resp_public.raise_for_status()
        results["public"] = resp_public.json()
        
        # Request for private API
        resp_private = requests.get(url_private, headers=private_headers)
        resp_private.raise_for_status()
        results["private"] = resp_private.json()
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        
    return results
