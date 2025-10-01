"""
Vercel API endpoint: /api/changes
Get change detection data for environmental monitoring
"""

import random
from datetime import datetime, timedelta
from ._utils import generate_synthetic_data_for_city, json_response

def handler(request):
    """Handle GET request for changes data"""
    try:
        location = getattr(request, 'args', {}).get('location', 'Seattle')
        
        # Generate current and historical data
        current_data = generate_synthetic_data_for_city(location)
        
        # Simulate changes over time
        changes = []
        for i in range(10):  # Last 10 detected changes
            change_date = datetime.now() - timedelta(days=random.randint(1, 90))
            change_type = random.choice(['health_decline', 'air_quality_change', 'deforestation', 'recovery', 'seasonal_change'])
            
            severity = random.choice(['low', 'medium', 'high'])
            severity_scores = {'low': random.uniform(0.1, 0.3), 'medium': random.uniform(0.3, 0.7), 'high': random.uniform(0.7, 1.0)}
            
            change_descriptions = {
                'health_decline': f'Forest health declined by {random.randint(5, 25)}% in sector {random.randint(1, 10)}',
                'air_quality_change': f'Air quality index increased by {random.randint(10, 50)} points',
                'deforestation': f'Tree loss detected: {random.randint(100, 1000)} trees in {random.uniform(1, 10):.1f} hectares',
                'recovery': f'Forest recovery observed: {random.randint(5, 15)}% health improvement',
                'seasonal_change': f'Seasonal variation: {random.choice(["leaf color change", "growth spurt", "dormancy period"])}'
            }
            
            changes.append({
                'id': f'change_{i+1}',
                'date': change_date.isoformat(),
                'type': change_type,
                'severity': severity,
                'severity_score': round(severity_scores[severity], 2),
                'description': change_descriptions[change_type],
                'location_area': f'Sector {random.randint(1, 10)}',
                'affected_trees': random.randint(50, 5000),
                'recovery_time_estimate': f'{random.randint(1, 12)} months',
                'confidence': round(random.uniform(0.7, 0.95), 2)
            })
        
        # Sort by date (most recent first)
        changes.sort(key=lambda x: x['date'], reverse=True)
        
        changes_data = {
            'location': location,
            'total_changes_detected': len(changes),
            'recent_changes': changes[:5],  # Most recent 5
            'all_changes': changes,
            'summary': {
                'high_severity': len([c for c in changes if c['severity'] == 'high']),
                'medium_severity': len([c for c in changes if c['severity'] == 'medium']),
                'low_severity': len([c for c in changes if c['severity'] == 'low']),
                'recovery_events': len([c for c in changes if c['type'] == 'recovery']),
                'decline_events': len([c for c in changes if c['type'] in ['health_decline', 'deforestation']])
            },
            'timestamp': current_data['timestamp']
        }
        
        return json_response(changes_data)
        
    except Exception as e:
        return json_response({'error': str(e)}, 500)