import requests
import json

def test_new_city_feature():
    """Test the new city auto-generation feature"""
    base_url = "http://localhost:8000"
    
    print("🏙️ Testing New City Generation Feature")
    print("=" * 50)
    
    # Test cities to add
    test_cities = ["Pune", "Jaipur", "Ahmedabad", "Chandigarh", "Kochi"]
    
    for city in test_cities:
        print(f"\n🔍 Testing city: {city}")
        
        try:
            # Test search endpoint
            response = requests.get(f"{base_url}/api/locations/search?q={city}")
            if response.status_code == 200:
                data = response.json()
                if data['found_existing']:
                    print(f"  ✅ Found existing data for {city}")
                else:
                    print(f"  🆕 Generated new data for {city}")
                    if data['locations']:
                        loc_data = data['locations'][0]
                        print(f"    🌳 Trees: {loc_data['tree_count']:,}")
                        print(f"    💨 Carbon: {loc_data['carbon_tons']} tons/year")
            else:
                print(f"  ❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ Exception: {e}")
    
    print("\n📊 Testing Overview with New Cities:")
    
    # Test overview for a new city
    test_city = "Lucknow"
    try:
        response = requests.get(f"{base_url}/api/metrics/overview?location={test_city}")
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ {test_city} Overview:")
            print(f"    🌳 Trees: {data['total_trees']:,}")
            print(f"    🍃 Coverage: {data['forest_coverage_hectares']} hectares")
            print(f"    💨 CO₂: {data['annual_co2_capture_tons']} tons")
            print(f"    ❤️ Health: {data['health_score_percentage']}%")
        else:
            print(f"  ❌ Overview Error: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Overview Exception: {e}")
    
    print("\n🔄 Testing Health Data for New City:")
    
    try:
        response = requests.get(f"{base_url}/api/health/distribution?location={test_city}")
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ {test_city} Health Distribution:")
            print(f"    🟢 Healthy: {data['healthy']:,} ({data['healthy_percentage']}%)")
            print(f"    🟡 Moderate: {data['moderate']:,} ({data['moderate_percentage']}%)")
            print(f"    🟠 Stressed: {data['stressed']:,} ({data['stressed_percentage']}%)")
            print(f"    🔴 Unhealthy: {data['unhealthy']:,} ({data['unhealthy_percentage']}%)")
        else:
            print(f"  ❌ Health Error: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Health Exception: {e}")

if __name__ == "__main__":
    test_new_city_feature()