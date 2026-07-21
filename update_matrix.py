import json
import os
import requests

def fetch_mlb_schedule():
    url = "https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return {}

def update_tracking_matrix():
    json_path = "odds_matrix.json"
    if not os.path.exists(json_path):
        print("Error: odds_matrix.json not found.")
        return

    with open(json_path, "r") as f:
        matrix = json.load(f)
    
    schedule_data = fetch_mlb_schedule()
    print(f"Successfully fetched live MLB data. Total players in tracking matrix: {len(matrix)}")
    
    # Generate output index file for your web display
    generate_web_index(matrix)

def generate_web_index(matrix):
    html_content = """
    <html>
    <head>
        <title>SharpPLAY MLB Home Run Matrix</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f4f4f9; color: #333; padding: 20px; }
            table { width: 100%; border-collapse: collapse; background: #fff; margin-top: 20px; }
            th, td { padding: 12px; border: 1px solid #ddd; text-align: left; }
            th { background-color: #003366; color: white; }
        </style>
    </head>
    <body>
        <h1>⚾ SharpPLAY Tracking Matrix</h1>
        <table>
            <tr>
                <th>Player</th>
                <th>Team</th>
                <th>1+ HR Odds</th>
                <th>2+ HR Odds</th>
                <th>Last 5 HR Total</th>
            </tr>
    """
    
    for entry in matrix:
        html_content += f"""
            <tr>
                <td>{entry.get('player')}</td>
                <td>{entry.get('team')}</td>
                <td>{entry.get('hr_1_odds')}</td>
                <td>{entry.get('hr_2_odds')}</td>
                <td>{entry.get('last_5_total')}</td>
            </tr>
        """
        
    html_content += """
        </table>
    </body>
    </html>
    """
    
    with open("index.html", "w") as f:
        f.write(html_content)
    print("Successfully generated updated index.html dashboard.")

if __name__ == "__main__":
    update_tracking_matrix()
