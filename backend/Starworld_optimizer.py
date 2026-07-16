def calculate_utility(row, risk_aversion=1.5):
    """
    Calculates the utility score for a single bet entry.
    """
    ev = row['expected_value']
    confidence = row['confidence']
    volatility = row['volatility']
    
    # Portfolio Utility Formula
    utility = (ev * confidence) - (risk_aversion * volatility)
    
    return utility

def rank_bets(df, risk_aversion=1.5):
    """
    Ranks bets based on calculated utility.
    """
    df['utility'] = df.apply(lambda row: calculate_utility(row, risk_aversion), axis=1)
    
    # Sort by utility descending to prioritize best bets
    return df.sort_values(by='utility', ascending=False)

