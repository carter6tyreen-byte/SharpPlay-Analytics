def check_alert_threshold(data_to_process):
    alerts = []
    if isinstance(data_to_process, list):
        for game in data_to_process:
            if game.get("analytics", {}).get("intensity", 0) > 80:
                alerts.append(game)
    return alerts
