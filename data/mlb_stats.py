def update_html(data):
    # 1. Safety Check: If data is None or empty, stop immediately
    if not data or "dates" not in data or not data["dates"]:
        print("No valid game data received. Preserving current index.html.")
        return

    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'index.html'))
    
    # 2. Extracting Data (Drilling down safely)
    try:
        game = data["dates"][0]["games"][0]
        away_team = game.get("teams", {}).get("away", {}).get("team", {}).get("name", "N/A")
        home_team = game.get("teams", {}).get("home", {}).get("team", {}).get("name", "N/A")
        status = game.get("status", {}).get("detailedState", "Scheduled")
        
        matchup = f"{away_team} @ {home_team}"
        result = status
    except (KeyError, IndexError) as e:
        print(f"Error parsing data: {e}")
        return # Don't update the HTML if parsing fails

    # 3. Generating HTML
    html_content = f"""
<html>
<body>
    <h1>Latest MLB Stats</h1>
    <table border="1">
        <tr><th>Matchup</th><th>Result</th></tr>
        <tr><td>{matchup}</td><td>{result}</td></tr>
    </table>
    <p>Last updated: 2026-07-15</p>
</body>
</html>
    """
    
    with open(output_path, "w") as f:
        f.write(html_content)
    print(f"Successfully wrote data to {output_path}")
