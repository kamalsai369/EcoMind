"""
Vercel API endpoint: /api/carbon
Get carbon sequestration data
"""

import random
from ._utils import generate_synthetic_data_for_city, json_response

def handler(request):
    """Handle GET request for carbon data"""
    try:
        location = getattr(request, 'args', {}).get('location', 'Seattle')
        
        # Generate location data
        location_data = generate_synthetic_data_for_city(location)
        
        # Calculate carbon metrics
        annual_sequestration = location_data['carbon_tons']
        monthly_sequestration = annual_sequestration / 12
        daily_sequestration = annual_sequestration / 365
        
        # Generate historical carbon data
        historical_data = []
        for i in range(12):  # 12 months of data
            month_variation = random.uniform(0.8, 1.2)
            historical_data.append({
                'month': f'2024-{i+1:02d}',
                'sequestration': round(monthly_sequestration * month_variation, 2),
                'offset_tons': round(monthly_sequestration * month_variation * 1.1, 2)
            })
        
        carbon_data = {
            'location': location,
            'annual_sequestration_tons': round(annual_sequestration, 2),
            'monthly_average_tons': round(monthly_sequestration, 2),
            'daily_average_tons': round(daily_sequestration, 3),
            'trees_monitored': location_data['tree_count'],
            'carbon_per_tree': round(annual_sequestration / location_data['tree_count'], 4),
            'co2_equivalent_offset': round(annual_sequestration * 3.67, 2),  # CO2 to carbon conversion
            'historical_data': historical_data,
            'timestamp': location_data['timestamp']
        }
        
        return json_response(carbon_data)
        
    except Exception as e:
        return json_response({'error': str(e)}, 500)