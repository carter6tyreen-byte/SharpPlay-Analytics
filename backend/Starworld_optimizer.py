def calculate_kelly_size(row, bankroll=1000, fraction=0.25):
    """
    Calculates the suggested bet size using Fractional Kelly.
    """
    # p is your model's probability, b is the decimal odds
    p = row.get('confidence', 0)
    b = row.get('decimal_odds', 0)
    
    if b <= 1: return 0
    
    # Kelly Formula
    kelly_fraction = (p * b - 1) / (b - 1)
    
    # Apply fractional Kelly and ensure no negative bets
    suggested_size = max(0, kelly_fraction * fraction * bankroll)
    
    return round(suggested_size, 2)

# Update your get_optimal_bets to include sizing
def get_optimal_bets_with_sizing(predictions_df, market_odds):
    # ... (after your utility ranking)
    predictions_df['bet_size'] = predictions_df.apply(calculate_kelly_size, axis=1)
    return predictions_df
