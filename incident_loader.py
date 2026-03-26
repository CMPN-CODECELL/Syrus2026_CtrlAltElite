import json

def load_incident(file_path):
    with open(file_path, "r", encoding="utf8") as f:
        data = json.load(f)
    return data