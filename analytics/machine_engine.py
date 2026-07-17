class AnalyticsEngine:
    # 1. Add this method to your class
    @staticmethod
    def get_position_name(code):
        mapping = {
            'P': 'Pitcher', 'C': 'Catcher', '1B': 'First Base', 
            '2B': 'Second Base', '3B': 'Third Base', 'SS': 'Shortstop', 
            'LF': 'Left Field', 'CF': 'Center Field', 'RF': 'Right Field',
            'DH': 'Designated Hitter', 'PH': 'Pinch Hitter', 'PR': 'Pinch Runner'
        }
        return mapping.get(code, code)

    def run_starworld_optimizer(self, game_id):
        # ... (rest of your existing code)
        
        # 2. Update your loop to call it using 'self' or the class name
        position_code = p.get('position', {}).get('abbreviation', 'N/A')
        all_players.append({
            'Team': t['name'],
            'Side': t['side'],
            'Player': p.get('person', {}).get('fullName', 'Unknown'),
            'Position': self.get_position_name(position_code), # Use self.get_position_name
            'Status': p.get('status', {}).get('description', 'Active')
        })
