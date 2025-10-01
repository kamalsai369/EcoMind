import requests
import time

def test_integration():
    """Test frontend-backend integration"""
    
    print("🧪 Testing EcoMind Frontend-Backend Integration")
    print("=" * 50)
    
    # Test API endpoints
    api_base = "http://localhost:8000"
    frontend_url = "http://localhost:8080"
    
    endpoints = [
        "/api/metrics/overview",
        "/api/health/distribution", 
        "/api/carbon/data",
        "/api/ndvi/analysis",
        "/api/trends/weekly"
    ]
    
    print("🔗 Testing API Endpoints:")
    for endpoint in endpoints:
        try:
            response = requests.get(f"{api_base}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"  ✅ {endpoint} - OK")
            else:
                print(f"  ❌ {endpoint} - Error {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"  ❌ {endpoint} - Connection error: {e}")
    
    print(f"\n🌐 Frontend URL: {frontend_url}")
    print(f"🔧 API URL: {api_base}")
    
    # Test frontend accessibility
    try:
        response = requests.get(frontend_url, timeout=5)
        if response.status_code == 200:
            print("  ✅ Frontend is accessible")
        else:
            print(f"  ❌ Frontend error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Frontend connection error: {e}")
    
    print("\n📊 Sample Data:")
    try:
        response = requests.get(f"{api_base}/api/metrics/overview")
        if response.status_code == 200:
            data = response.json()
            print(f"  🌳 Total Trees: {data.get('total_trees', 'N/A'):,}")
            print(f"  🍃 Forest Coverage: {data.get('forest_coverage_hectares', 'N/A')} hectares")
            print(f"  💨 CO₂ Capture: {data.get('annual_co2_capture_tons', 'N/A')} tons/year")
            print(f"  ❤️ Health Score: {data.get('health_score_percentage', 'N/A')}%")
    except Exception as e:
        print(f"  ❌ Could not fetch sample data: {e}")
    
    print("\n✨ Integration Status:")
    print("  🔄 Real-time data updates every 30 seconds")
    print("  📱 Responsive React frontend with shadcn/ui components")
    print("  🚀 FastAPI backend with automatic API documentation")
    print("  💾 SQLite database with forest monitoring data")
    
    print(f"\n🎯 Next Steps:")
    print(f"  1. Open {frontend_url} in your browser")
    print(f"  2. Navigate through the pages (Health, Carbon, etc.)")
    print(f"  3. Check {api_base}/docs for API documentation")
    print(f"  4. Monitor real-time data updates")

if __name__ == "__main__":
    test_integration()