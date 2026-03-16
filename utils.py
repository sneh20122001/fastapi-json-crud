import json
from typing import List
from models import ItemResponse

DATA_FILE = 'data.json'

def read_data():
    with open(DATA_FILE, 'r') as file:
        return json.load(file)
    
def write_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def get_next_id(data):
    if not data:
        return 1
    return max(item['id'] for item in data) + 1