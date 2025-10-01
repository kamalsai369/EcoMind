"""
Vercel API endpoint: /api/trends
Get trend data for locations
"""

from ._utils import get_trends_data, json_response

def handler(request):
    """Handle GET request for trends data"""
    try:
        # Extract parameters
        location = getattr(request, 'args', {}).get('location', 'Seattle')
        days = int(getattr(request, 'args', {}).get('days', '30'))
        
        # Generate trends data
        trends = get_trends_data(location, days)
        
        return json_response({
            'location': location,
            'trends': trends,
            'period_days': days
        })
        
    except Exception as e:
        return json_response({'error': str(e)}, 500)