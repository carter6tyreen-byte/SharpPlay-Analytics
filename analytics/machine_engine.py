def get_position_name(code):
    mapping = {
        'P': 'Pitcher', 'C': 'Catcher', '1B': 'First Base', 
        '2B': 'Second Base', '3B': 'Third Base', 'SS': 'Shortstop', 
        'LF': 'Left Field', 'CF': 'Center Field', 'RF': 'Right Field',
        'DH': 'Designated Hitter', 'PH': 'Pinch Hitter', 'PR': 'Pinch Runner'
    }
    return mapping.get(code, code) # Returns the full name or the original code if not found

# Inside your loop in run_starworld_optimizer:
position_code = p.get('position', {}).get('abbreviation', 'N/A')
all_players.append({
    'Team': t['name'],
    'Side': t['side'],
    'Player': p.get('person', {}).get('fullName', 'Unknown'),
    'Position': get_position_name(position_code), # Map the code here
    'Status': p.get('status', {}).get('description', 'Active')
})
