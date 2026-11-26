import json
import os
from datetime import datetime

# <project root>/data/app_statistics.json
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")
STATS_FILE = os.path.join(DATA_DIR, "app_statistics.json")

def _load_stats() -> list:
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def log_event(feature: str, duration_sec: float, details: dict):
    os.makedirs(DATA_DIR, exist_ok=True)
    stats = _load_stats()
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "feature": feature,
        "duration_sec": round(duration_sec, 2),
        "details": details,
    }
    stats.append(entry)
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, indent=2)

def get_stats() -> list:
    return _load_stats()

def clear_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "w") as f:
            json.dump([], f)
