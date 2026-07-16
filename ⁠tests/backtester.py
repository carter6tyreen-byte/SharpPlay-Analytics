import sys
import os

# 1. Dynamically get the root directory path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 2. Add root to path so 'import' knows where to look
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# 3. NOW you can import your project modules safely
from processor import filter_starworld_criteria
from Starworld_optimizer import get_optimal_bets_with_sizing
