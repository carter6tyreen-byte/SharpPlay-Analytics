def run_ingestion():
    # Temporarily return dummy data to test the rest of the pipeline
    return [
        {"match_id": "test_001", "team_a": "Team A", "team_b": "Team B", "intensity": 88},
        {"match_id": "test_002", "team_a": "Team C", "team_b": "Team D", "intensity": 95}
    ]
