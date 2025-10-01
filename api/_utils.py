"""
Shared utilities for Vercel API functions
"""

import json
import random
import numpy as np
from datetime import datetime
from typing import Dict, Any
import os

# For Vercel deployment, we'll use environment variables or in-memory data
# since SQLite files don't persist in serverless environments

def generate_synthetic_data_for_city(city_name: str) -> Dict[str, Any]:
    """Generate synthetic forest data for a new city"""
    # Set seed based on city name for consistency
    random.seed(hash(city_name) % 1000000)
    np.random.seed(hash(city_name) % 1000000)
    
    # Base parameters for cities
    population_factors = {
        'mumbai': 1.0, 'delhi': 0.9, 'bangalore': 0.7, 'chennai': 0.6,
        'kolkata': 0.8, 'hyderabad': 0.65, 'pune': 0.5, 'ahmedabad': 0.4,
        'jaipur': 0.3, 'lucknow': 0.25, 'kanpur': 0.2, 'nagpur': 0.15,
        'seattle': 0.8, 'portland': 0.6, 'vancouver': 0.7, 'tokyo': 0.9,
        'stockholm': 0.5, 'munich': 0.6, 'sao_paulo': 0.8
    }
    
    # Determine city size factor
    city_lower = city_name.lower().replace(' ', '_')
    size_factor = population_factors.get(city_lower, random.uniform(0.1, 0.8))
    
    # Generate base forest metrics
    base_tree_count = int(random.uniform(50000, 500000) * size_factor)
    
    # Health distribution (influenced by urbanization)
    urban_stress = 1 - size_factor  # More urbanization = more stress
    
    healthy_pct = max(0.4, 0.8 - urban_stress * 0.3 + random.uniform(-0.1, 0.1))
    moderate_pct = max(0.1, 0.15 + urban_stress * 0.1 + random.uniform(-0.05, 0.05))
    stressed_pct = max(0.05, 0.03 + urban_stress * 0.15 + random.uniform(-0.02, 0.02))
    unhealthy_pct = max(0.01, 1 - healthy_pct - moderate_pct - stressed_pct)
    
    # Normalize percentages
    total_pct = healthy_pct + moderate_pct + stressed_pct + unhealthy_pct
    healthy_pct /= total_pct
    moderate_pct /= total_pct
    stressed_pct /= total_pct
    unhealthy_pct /= total_pct
    
    # Calculate tree counts
    healthy_count = int(base_tree_count * healthy_pct)
    moderate_count = int(base_tree_count * moderate_pct)
    stressed_count = int(base_tree_count * stressed_pct)
    unhealthy_count = base_tree_count - healthy_count - moderate_count - stressed_count
    
    # Carbon sequestration (influenced by tree health)
    carbon_per_tree = 0.05 + random.uniform(-0.01, 0.01)  # tons per tree per year
    health_factor = (healthy_count * 1.0 + moderate_count * 0.7 + 
                    stressed_count * 0.4 + unhealthy_count * 0.1) / base_tree_count
    carbon_tons = base_tree_count * carbon_per_tree * health_factor
    
    return {
        'location': city_name,
        'timestamp': datetime.now().isoformat(),
        'tree_count': base_tree_count,
        'healthy_count': healthy_count,
        'moderate_count': moderate_count,
        'stressed_count': stressed_count,
        'unhealthy_count': unhealthy_count,
        'carbon_tons': round(carbon_tons, 2),
        'health_percentage': round(healthy_pct * 100, 1),
        'air_quality': random.randint(50, 200),
        'biodiversity_index': random.randint(60, 95),
        'temperature': round(random.uniform(15, 35), 1),
        'humidity': random.randint(40, 80),
        'rainfall': random.randint(800, 2500),
        'soil_ph': round(random.uniform(5.5, 7.5), 1)
    }

def get_mock_locations_data():
    """Get mock data for multiple locations"""
    cities = [
        'Seattle', 'Portland', 'Vancouver', 'Tokyo', 'Stockholm', 
        'Munich', 'São Paulo', 'Mumbai', 'Delhi', 'Bangalore',
        'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad',
        'Jaipur', 'Lucknow', 'Kanpur', 'Nagpur', 'Surat',
        'Coimbatore', 'Kochi', 'Thiruvananthapuram', 'Mysore', 'Mangalore'
    ]
    
    return [generate_synthetic_data_for_city(city) for city in cities]

def get_trends_data(location: str, days: int = 30):
    """Generate trend data for a location"""
    random.seed(hash(location) % 1000000)
    trends = []
    
    for i in range(days):
        date = datetime.now().replace(day=1).replace(hour=0, minute=0, second=0, microsecond=0)
        date = date.replace(day=min(date.day + i, 28))
        
        base_health = 70 + random.uniform(-10, 15)
        health_score = max(30, min(95, base_health + random.uniform(-5, 5)))
        
        trends.append({
            'date': date.isoformat(),
            'health_score': round(health_score, 1),
            'air_quality': random.randint(50, 150),
            'carbon_sequestration': round(random.uniform(2.5, 8.5), 2),
            'biodiversity_index': random.randint(65, 90)
        })
    
    return trends

def cors_headers():
    """Return CORS headers for API responses"""
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    }

def json_response(data, status_code=200):
    """Create a JSON response with CORS headers"""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            **cors_headers()
        },
        'body': json.dumps(data)
    }