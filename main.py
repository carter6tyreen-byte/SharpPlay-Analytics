from src.optimizer import get_optimal_bets

# ... inside your main() function ...
# 1. Prediction
predictions = run_hr_prediction_model(clean_data)

# 2. Optimization
# You will need to fetch market_odds from your API alongside your clean_data
market_odds = fetch_market_odds() 
final_plays = get_optimal_bets(predictions, market_odds)

print("--- SharpPLAY Optimized Plays ---")
for play in final_plays:
    print(f"Player: {play['player']} | Edge: {play['ev']*100}%")
