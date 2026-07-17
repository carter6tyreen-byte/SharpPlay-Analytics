class AnalyticsEngine:
    # ... existing methods ...

    def apply_environment_score(self, data):
        """
        Calculates ES and applies a tunable probability adjustment.
        """
        es = self.calculate_total_es(data)
        
        # Adjustment mapping (tunable via config/backtesting)
        if es >= 90: adjustment = 0.08
        elif es >= 80: adjustment = 0.05
        elif es >= 70: adjustment = 0.03
        elif es >= 45: adjustment = 0.00
        elif es >= 30: adjustment = -0.03
        elif es >= 15: adjustment = -0.06
        else: adjustment = -0.08
        
        # Apply adjustment to base probability
        data['p_adjusted'] = data['p_base'] * (1 + adjustment)
        return data
