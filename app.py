import csv
import datetime
import os


def log_model_predictions_and_results(slate_date, matchup_data):
  """Appends model projections and actual outcomes to a CSV file

  to build a historical learning loop dataset.
  """
  directory = "data/learning_loop"
  os.makedirs(directory, exist_ok=True)
  file_path = os.path.join(directory, f"evaluation_log_{slate_date}.csv")

  file_exists = os.path.exists(file_path)

  headers = [
      "date",
      "matchup",
      "pitcher",
      "sharpplay_proj",
      "propalytics_proj",
      "line",
      "actual_stats",
      "result",
  ]

  with open(file_path, mode="a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    # Write header if file is newly created
    if not file_exists:
      writer.writerow(headers)

    for item in matchup_data:
      writer.writerow([
          slate_date,
          item["matchup"],
          item["pitcher"],
          item["sharpplay_proj"],
          item["propalytics_proj"],
          item["line"],
          item.get("actual_stats", "Pending"),
          item.get("result", "Pending"),
      ])


# Example usage for today's slate (July 22, 2026)
today_data = [{
    "matchup": "PIT @ NYY",
    "pitcher": "Gerrit Cole",
    "sharpplay_proj": 8.1,
    "propalytics_proj": 8.0,
    "line": 6.5,
    "actual_stats": 9,  # Populated post-game via MLB API
    "result": "HIT",  # Automatically graded: Over hit
}]

log_model_predictions_and_results("2026-07-22", today_data)
