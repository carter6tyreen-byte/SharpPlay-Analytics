def run_ingestion():
    # HARDCODED TEST: This bypasses the API to prove your pipeline works
    return [
        {"match_id": "test_001", "team_a": "Team A", "team_b": "Team B", "intensity": 88},
        {"match_id": "test_002", "team_a": "Team C", "team_b": "Team D", "intensity": 95}
    ]

