# database/recorder.py
import json
import datetime
import os

def archive_prediction(data):
    os.makedirs('archive', exist_ok=True)
    filename = f"archive/history_{datetime.datetime.now().strftime('%Y-%m-%d')}.json"
    with open(filename, 'a') as f:
        json.dump(data, f)
        f.write('\n')
