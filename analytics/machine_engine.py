import pandas as pd
import numpy as np
import logging
import streamlit as st
from data.data_collector import load_matchup_data
from data.mlb_stats import fetch_roster_data

class AnalyticsEngine:
    @staticmethod
    def get_position_name(code):
        mapping = {
            'P': 'Pitcher', 'C': 'Catcher', '1B': 'First Base', 
            '2B': 'Second Base', '3B': 'Third Base', 'SS': 'Shortstop', 
            'LF': 'Left Field', 'CF': 'Center Field', 'RF': 'Right Field',
            'DH': 'Designated Hitter'
        }
        return mapping.get(code, code)

    def get_all_games(self):
        matchup_data = load_matchup_data() 
        data = matchup_data.get('dates', [])
        
        if data is None or not data:
            return pd.DataFrame() 
        
        return pd.DataFrame(data)

    def run_starworld_optimizer(self, game_id):
        raw_data = fetch_roster_data(game_id) 
        all_players = []
        
        for team in raw_data.get('teams', []):
            team_name = team.get('name', 'Unknown')
            team_side = team.get('side', 'N/A')
            
            for player in team.get('roster', []):
                position_code = player.get('position', {}).get('abbreviation', 'N/A')
                all_players.append({
                    'Team': team_name,
                    'Side': team_side,
                    'Player': player.get('person', {}).get('fullName', 'Unknown'),
                    'Position': self.get_position_name(position_code),
                    'Status': player.get('status', {}).get('description', 'Active')
                })
        return pd.DataFrame(all_players)

    def get_optimal_bets_with_sizing(self, predictions, market_odds):
        try:
            logging.info("Starting Starworld optimization...")
            df = pd.merge(predictions, market_odds, on='player_id', how='inner')
            
            df['implied_prob'] = 1 / df['decimal_odds']
            df['edge'] = df['prob'] - df['implied_prob']
            df['utility_score'] = df['edge'] * (1 - df['volatility'])
            
            df['b'] = df['decimal_odds'] - 1
            df['kelly_fraction'] = np.where(df['b'] > 0, (df['b'] * df['prob'] - (1 - df['prob'])) / df['b'], 0)
            df['bet_size'] = df['kelly_fraction'].clip(0, 0.05)
            
            return df[df['utility_score'] > 0].copy()
        except Exception as e:
            logging.error(f"Error in starworld_optimizer: {e}")
            return pd.DataFrame()
import sys
print(sys.path)
