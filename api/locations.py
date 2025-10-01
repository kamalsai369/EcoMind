"""
Vercel API endpoint: /api/locations
Get all forest monitoring locations
"""

from ._utils import get_mock_locations_data, json_response

def handler(request):
    """Handle GET request for locations"""
    try:
        locations_data = get_mock_locations_data()
        
        # Format data for frontend
        formatted_data = []
        for location in locations_data:
            formatted_data.append({
                'total_trees': location['tree_count'],
                'healthy_count': location['healthy_count'],
                'moderate_count': location['moderate_count'],
                'stressed_count': location['stressed_count'],
                'unhealthy_count': location['unhealthy_count'],
                'carbon_tons': location['carbon_tons'],
                'location': location['location'],
                'timestamp': location['timestamp'],
                'health_percentage': location['health_percentage'],
                'air_quality': location['air_quality'],
                'biodiversity_index': location['biodiversity_index']
            })
        
        return json_response(formatted_data)
        
    except Exception as e:
        return json_response({'error': str(e)}, 500)