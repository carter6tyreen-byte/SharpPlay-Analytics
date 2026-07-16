import sys
import os
import pandas as pd

# Setup path to import project modules
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from processor import filter_starworld_criteria
from Starworld_optimizer import get_optimal_bets_with_sizing

def run_backtest(data_path, initial_bankroll=1000):
    # 1. Load historical dataset
    df = pd.read_csv(data_path)
    df['date'] = pd.to_datetime(df['date'])
    
    results = []
    current_bankroll = initial_bankroll
    
    # 2. Iterate through historical dates
    for date in sorted(df['date'].unique()):
        daily_data = df[df['date'] == date].copy()
        
        # Apply Starworld Filter
        validated_data = filter_starworld_criteria(daily_data)
        
        if validated_data.empty:
            continue
            
        # Optimize bets (using your logic from main.py)
        # Note: Ensure daily_data contains market_odds and volatility
        optimal_bets = get_optimal_bets_with_sizing(validated_data, daily_data)
        
        if not optimal_bets.empty:
            # 3. Calculate P&L: (Size * Odds) if HR occurred, else -Size
            # Assuming 'actual_hr' (1/0) is in your CSV
            pnl = optimal_bets.apply(
                lambda x: (x['bet_size'] * (x['decimal_odds'] - 1)) if x['actual_hr'] == 1 
                else -x['bet_size'], axis=1
            ).sum()
            
            current_bankroll += pnl
            results.append({'date': date, 'bankroll': current_bankroll})
            
    return pd.DataFrame(results)

if __name__ == "__main__":
    # Point this to your prepared CSV file
    report = run_backtest('data/historical_mlb_data.csv')
    print(report)

def run_backtest(data_path, initial_bankroll=1000):
    df = pd.read_csv(data_path)
    df['date'] = pd.to_datetime(df['date'])
    
    bankroll = initial_bankroll
    portfolio_history = []
    
    for date in sorted(df['date'].unique()):
        daily_data = df[df['date'] == date]
        
        # 1. Strategy execution
        bets = get_optimal_bets_with_sizing(daily_data, daily_data)
        
        # 2. Performance Tracking
        pnl = calculate_daily_pnl(bets)
        bankroll += pnl
        
        portfolio_history.append({'date': date, 'bankroll': bankroll})

    # 3. Calculate Performance Metrics
    results = pd.DataFrame(portfolio_history)
    total_roi = ((results['bankroll'].iloc[-1] - initial_bankroll) / initial_bankroll) * 100
    max_drawdown = calculate_max_drawdown(results['bankroll'])
    
    print(f"Total ROI: {total_roi:.2f}%")
    print(f"Max Drawdown: {max_drawdown:.2f}%")
    
    return results

def calculate_max_drawdown(series):
    return ((series.cummax() - series) / series.cummax()).max() * 100

def run_backtest(data_path, initial_bankroll=1000):
    df = pd.read_csv(data_path)
    df['date'] = pd.to_datetime(df['date'])
    
    bankroll = initial_bankroll
    portfolio_history = []
    
    for date in sorted(df['date'].unique()):
        daily_data = df[df['date'] == date]
        
        # 1. Strategy execution
        bets = get_optimal_bets_with_sizing(daily_data, daily_data)
        
        # 2. Performance Tracking
        pnl = calculate_daily_pnl(bets)
        bankroll += pnl
        
        portfolio_history.append({'date': date, 'bankroll': bankroll})

    # 3. Calculate Performance Metrics
    results = pd.DataFrame(portfolio_history)
    total_roi = ((results['bankroll'].iloc[-1] - initial_bankroll) / initial_bankroll) * 100
    max_drawdown = calculate_max_drawdown(results['bankroll'])
    
    print(f"Total ROI: {total_roi:.2f}%")
    print(f"Max Drawdown: {max_drawdown:.2f}%")
    
    return results

def calculate_max_drawdown(series):
    return ((series.cummax() - series) / series.cummax()).max() * 100
