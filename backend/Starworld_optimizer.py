import pandas as pd
import numpy as np
import logging

def calculate_utility(row, risk_aversion=1.5):
    """
    Calculates the utility score: Utility = (EV * Confidence) - (RiskAversion * Volatility)
    """
    ev = row.get('expected_value', 0)
    confidence = row.get('confidence', 0)
    volatility = row.get('volatility', 0)
    
    return (ev * confidence) - (risk_aversion * volatility)

def apply_correlation_penalty(selection_df, correlation_matrix, penalty_lambda=0.5):
    """
    Calculates total penalty for a selection based on internal correlations.
    """
    total_penalty = 0
    players = selection_df['player_id'].tolist()
    
    for i in range(len(players)):
        for j in range(i + 1, len(players)):
            # Look up correlation between pair (i, j)
            pair = tuple(sorted((players[i], players[j])))
            corr = correlation_matrix.get(pair, 0)
            total_penalty += (corr * penalty_lambda)
            
    return total_penalty

def get_optimal_bets(predictions_df, market_odds, correlation_matrix=None):
    """
    Core Optimizer: Ranks candidates by Utility and enforces Portfolio constraints.
    """
    if predictions_df.empty:
        return pd.DataFrame()

    # 1. Calculate base utility for candidates
    predictions_df['utility'] = predictions_df.apply(calculate_utility, axis=1)
    
    # 2. Sort candidates by utility (Greedy approach)
    sorted_candidates = predictions_df.sort_values(by='utility', ascending=False)
    
    # 3. Final Portfolio Selection
    final_portfolio = []
    correlation_matrix = correlation_matrix or {}
    
    for _, bet in sorted_candidates.iterrows():
        # Heuristic: Check if adding this bet increases correlation penalty significantly
        temp_portfolio = final_portfolio + [bet]
        
        # Calculate marginal penalty
        penalty = apply_correlation_penalty(pd.DataFrame(temp_portfolio), correlation_matrix)
        
        # Accept if utility gain > penalty cost
        if bet['utility'] > penalty:
            final_portfolio.append(bet)
            
        # 4. Limit to top N for portfolio construction
        if len(final_portfolio) >= 5: # Example limit
            break
            
    logging.info(f"Optimizer: Selected {len(final_portfolio)} optimal bets.")
    return pd.DataFrame(final_portfolio)
