import pandas as pd
import numpy as np
import logging

def get_optimal_bets_with_sizing(predictions, market_odds):
    """
    Applies utility-based optimization, penalty logic, and Kelly Criterion sizing.
    """
    try:
        logging.info("Starting Starworld optimization...")
        
        # 1. Merge predictions with market odds
        # Ensure your dataframes have a common 'player_id' or 'game_id'
        df = pd.merge(predictions, market_odds, on='player_id', how='inner')
        
        # 2. Calculate Edge (Model probability - Market implied probability)
        # Assuming 'prob' from predictions and 'decimal_odds' from market
        df['implied_prob'] = 1 / df['decimal_odds']
        df['edge'] = df['prob'] - df['implied_prob']
        
        # 3. Apply Starworld Utility Filter (Correlation/Volatility penalty)
        # Example: Reduce edge by a volatility factor
        df['utility_score'] = df['edge'] * (1 - df['volatility'])
        
        # 4. Kelly Criterion Sizing
        # Formula: f* = (bp - q) / b 
        # Where b = odds - 1, p = prob, q = 1-p
        df['b'] = df['decimal_odds'] - 1
        df['kelly_fraction'] = (df['b'] * df['prob'] - (1 - df['prob'])) / df['b']
        
        # Constrain sizing (e.g., max 5% of bankroll)
        df['bet_size'] = df['kelly_fraction'].clip(0, 0.05)
        
        # Filter for positive expected value only
        optimal_bets = df[df['utility_score'] > 0].copy()
        
        logging.info(f"Optimization complete. {len(optimal_bets)} bets identified.")
        return optimal_bets

    except Exception as e:
        logging.error(f"Error in starworld_optimizer: {e}")
        return pd.DataFrame()
