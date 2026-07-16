import sys
import os

# Get the directory where main.py resides
root_dir = os.path.dirname(os.path.abspath(__file__))
# Add the 'backend' folder to the path
backend_dir = os.path.join(root_dir, 'backend')

if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Now your import will work
from starworld_optimizer import get_optimal_bets_with_sizing
