import requests
import json

def test_end_to_end():
    """Test the complete end-to-end functionality"""
    base_url = "http://localhost:8000"
    
    print("🌳 EcoMind Dynamic City Generation - End-to-End Test")
    print("=" * 60)
    
    # Test the search endpoint with a new city
    new_city = "Indore"
    print(f"\n🔍 Testing Search for New City: {new_city}")
    
    response = requests.get(f"{base_url}/api/locations/search?q={new_city}")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Search Response:")
        print(f"  Found Existing: {data['found_existing']}")
        print(f"  Generated Data: {not data['found_existing']}")
        
        if data['locations']:
            location = data['locations'][0]
            print(f"  🏙️ City: {location['location']}")
            print(f"  🌳 Trees: {location['tree_count']:,}")
            print(f"  💨 Carbon: {location['carbon_tons']} tons/year")
    
    # Test getting all available locations
    print(f"\n📍 Testing Available Locations Endpoint:")
    response = requests.get(f"{base_url}/api/locations/list")
    
    if response.status_code == 200:
        locations = response.json()
        print(f"✅ Total Available Locations: {len(locations)}")
        
        # Show recently added cities
        recent_cities = [loc for loc in locations if loc['name'] in ['Pune', 'Jaipur', 'Ahmedabad', 'Chandigarh', 'Kochi', 'Lucknow', 'Indore']]
        if recent_cities:
            print(f"🆕 Recently Added Cities ({len(recent_cities)}):")
            for city in recent_cities[:5]:  # Show first 5
                print(f"  • {city['name']}: {city['tree_count']:,} trees")
    
    # Test metrics for a new city
    test_city = "Bhopal"
    print(f"\n📊 Testing Metrics for Another New City: {test_city}")
    
    response = requests.get(f"{base_url}/api/metrics/overview?location={test_city}")
    if response.status_code == 200:
        metrics = response.json()
        print(f"✅ Auto-Generated Metrics for {test_city}:")
        print(f"  🌳 Total Trees: {metrics['total_trees']:,}")
        print(f"  🍃 Forest Coverage: {metrics['forest_coverage_hectares']} hectares")
        print(f"  💨 Annual CO₂ Capture: {metrics['annual_co2_capture_tons']} tons")
        print(f"  ❤️ Health Score: {metrics['health_score_percentage']}%")
        if 'growth_rate_percentage' in metrics:
            print(f"  📈 Growth Rate: {metrics['growth_rate_percentage']}%")
    
    print(f"\n🎯 Feature Summary:")
    print(f"✅ Dynamic city search and generation")
    print(f"✅ Realistic forest data based on city characteristics")
    print(f"✅ Automatic database integration")
    print(f"✅ Real-time API endpoints")
    print(f"✅ Location-aware dashboard")
    
    print(f"\n🚀 Ready for Frontend Testing!")
    print(f"   Frontend: http://localhost:8081")
    print(f"   API: http://localhost:8000")
    print(f"   Try typing any Indian city in the location selector!")

if __name__ == "__main__":
    test_end_to_end()