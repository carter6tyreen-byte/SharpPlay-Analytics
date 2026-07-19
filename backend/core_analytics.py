import json
import os

def main():
    # Keep directory creation consistent
    os.makedirs('data', exist_ok=True)
    
    # Logic for player distributions
    data = {
        "Aaron Judge": {"HR": 0.12, "SO": 0.25},
        "Shohei Ohtani": {"HR": 0.10, "SO": 0.20}
    }
    
    # Save to the root-level data/ folder
    output_path = os.path.join('data', 'player_distributions.json')
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)
        
    print(f"Analytics successfully saved to {output_path}")

if __name__ == "__main__":
    main()
