import requests
from datetime import datetime, timedelta

def get_games_for_week():
    all_rows = []
    # Loop 7 days
    for i in range(7):
        target_date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
        # Ensure the API call is clean
        url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={target_date}"
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("dates"):
                    for date_entry in data["dates"]:
                        for game in date_entry.get("games", []):
                            away = game["teams"]["away"]["team"]["name"]
                            home = game["teams"]["home"]["team"]["name"]
                            status = game["status"]["detailedState"]
                            # Display status to help you debug on your board
                            all_rows.append(f"<tr><td>{target_date}</td><td>{away} @ {home} ({status})</td></tr>")
        except Exception:
            continue
    return all_rows

# update_html() remains the same as your previous version...
