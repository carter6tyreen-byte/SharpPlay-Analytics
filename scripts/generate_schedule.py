import requests
from datetime import datetime, timedelta

def get_games_for_week():
    all_rows = []
    for i in range(7):
        target_date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
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
                            all_rows.append(f"<tr><td>{target_date}</td><td>{away} @ {home} ({status})</td></tr>")
        except Exception:
            continue
    return all_rows

def update_html():
    rows = get_games_for_week()
    table_content = "".join(rows) if rows else "<tr><td colspan='2'>No upcoming games found.</td></tr>"

    html_content = f"""<html>
<head><title>MLB Schedule</title></head>
<body>
    <h1>MLB Schedule (Next 7 Days)</h1>
    <table border="1">
        <tr><th>Date</th><th>Matchup</th></tr>
        {table_content}
    </table>
    <p>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')} UTC</p>
</body>
</html>"""

    # This saves the file in your repository root
    with open("index.html", "w") as f:
        f.write(html_content)
    print("Successfully updated index.html.")

if __name__ == "__main__":
    update_html()
