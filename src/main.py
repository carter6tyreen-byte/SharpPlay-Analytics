import requests
# Other imports like pandas go here
# 1. First, fetch the data
response = requests.get(API_URL)
data = response.json()

# 2. Iterate through the games list
# 'data['dates'][0]['games']' is typically the path for MLB API
for game in data['dates'][0]['games']: 
    
    # 3. NOW you can safely extract names because 'game' is defined
    away_name = game['teams']['away']['team']['name']
    home_name = game['teams']['home']['team']['name']
    
    # 4. Process the rest of your data here...
    print(f"Processing: {away_name} vs {home_name}")
