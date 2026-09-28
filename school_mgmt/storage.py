"""Storage layer: loads and saves all school data in a single JSON file."""
import json
from pathlib import Path

database = "School_data.json"
data = {"Students": [], "Teachers": []}

if Path(database).exists():
    with open(database, "r") as f:
        content = f.read()
        if content:
            data = json.loads(content)

def save():
    with open(database, "w") as f:
        json.dump(data, f, indent=4)
