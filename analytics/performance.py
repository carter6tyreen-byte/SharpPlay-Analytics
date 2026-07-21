name: Daily Sports Analytics Backtest

on:
  schedule:
    - cron: '0 9 * * *' # Runs every morning at 9:00 AM UTC
  workflow_dispatch:

jobs:
  run-backtest:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install Dependencies
        run: pip install pandas

      - name: Execute Backtest Verification
        run: python backtest_tracker.py

      - name: Commit Updated Audit Logs
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"
          git add backtest_results_log.csv
          git diff --quiet && git diff --staged --quiet || (git commit -m "Automated backtest log update [skip ci]" && git push)
