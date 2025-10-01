"""
Vercel API endpoint: /api/health/[location]
Get health data for a specific location
"""

import json
from ._utils import generate_synthetic_data_for_city, json_response

def handler(request):
    """Handle GET request for location health data"""
    try:
        # Extract location from query parameters or path
        location = None
        
        # Try to get location from query parameters
        if hasattr(request, 'args') and 'location' in request.args:
            location = request.args['location']
        
        # Try to get from request body if POST
        if not location and hasattr(request, 'get_json'):
            try:
                data = request.get_json()
                if data and 'location' in data:
                    location = data['location']
            except:
                pass
        
        # Default location if not provided
        if not location:
            location = 'Seattle'
        
        # Generate health data for the location
        location_data = generate_synthetic_data_for_city(location)
        
        # Format for health response
        health_data = {
            'location': location_data['location'],
            'health_score': location_data['health_percentage'],
            'air_quality': location_data['air_quality'],
            'carbon_sequestration': location_data['carbon_tons'],
            'biodiversity_index': location_data['biodiversity_index'],
            'temperature': location_data['temperature'],
            'humidity': location_data['humidity'],
            'rainfall': location_data['rainfall'],
            'soil_ph': location_data['soil_ph'],
            'tree_distribution': {
                'healthy': location_data['healthy_count'],
                'moderate': location_data['moderate_count'],
                'stressed': location_data['stressed_count'],
                'unhealthy': location_data['unhealthy_count'],
                'total': location_data['tree_count']
            },
            'timestamp': location_data['timestamp']
        }
        
        return json_response(health_data)
        
    except Exception as e:
        return json_response({'error': str(e)}, 500)