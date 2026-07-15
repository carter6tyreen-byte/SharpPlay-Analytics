import requests
import os
import json

def fetch_mlb_data():
    API_KEY = os.getenv("MLB_API_KEY")
    API_URL = "https://api.sportsdata.io/v3/mlb/scores/json/GamesByDate/2026-07-15"
    headers = {"Ocp-Apim-Subscription-Key": API_KEY}
    
    try:
        response = requests.get(API_URL, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print(f"Ingestion Error: {e}")
        return []
