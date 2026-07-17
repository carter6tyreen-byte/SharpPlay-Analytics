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
        # Your logic here
        pass

    def run_starworld_optimizer(self, game_id):
        # ... use self.get_position_name(code)
        pass
