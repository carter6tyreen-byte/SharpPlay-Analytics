def fetch_mlb_data():
    url = "https://statsapi.mlb.com/api/v1/schedule/live?sportId=1"
    # REMOVE THE HEADERS for this specific public endpoint
    try:
        response = requests.get(url) 
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None
