import json
import os
from datetime import datetime, timedelta
import random

def load_environmental_data():
    """Load the environmental data from JSON file"""
    data_file = os.path.join(os.path.dirname(__file__), 'data', 'environmental_data.json')
    with open(data_file, 'r') as f:
        return json.load(f)

def get_simulated_data():
    """Generate simulated data based on the dataset patterns"""
    data = load_environmental_data()
    data_points = data['data_points']
    
    # Get the last data point
    last_point = data_points[-1]
    
    # Create a new data point with slight variations
    new_point = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'air_quality': max(50, min(100, last_point['air_quality'] + random.uniform(-2, 2))),
        'co2_level': max(400, min(600, last_point['co2_level'] + random.uniform(-5, 5))),
        'temperature': max(20, min(30, last_point['temperature'] + random.uniform(-0.5, 0.5))),
        'noise_level': max(60, min(80, last_point['noise_level'] + random.uniform(-2, 2))),
        'humidity': max(40, min(60, last_point['humidity'] + random.uniform(-1, 1))),
        'particulate_matter': max(10, min(30, last_point['particulate_matter'] + random.uniform(-1, 1)))
    }
    
    return new_point

def get_thresholds():
    """Get the threshold values for different metrics"""
    data = load_environmental_data()
    return data['metadata']['thresholds'] 