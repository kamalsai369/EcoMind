import requests
import json
import time

def test_api():
    base_url = "http://localhost:8000"
    
    # Wait a moment for server to start
    time.sleep(3)
    
    try:
        # Test overview endpoint
        response = requests.get(f"{base_url}/api/metrics/overview")
        print("Overview API Response:")
        print(json.dumps(response.json(), indent=2))
        print("\n" + "="*50 + "\n")
        
        # Test health distribution
        response = requests.get(f"{base_url}/api/health/distribution")
        print("Health Distribution API Response:")
        print(json.dumps(response.json(), indent=2))
        print("\n" + "="*50 + "\n")
        
        # Test carbon data
        response = requests.get(f"{base_url}/api/carbon/data")
        print("Carbon Data API Response:")
        print(json.dumps(response.json(), indent=2))
        
    except requests.exceptions.RequestException as e:
        print(f"API test failed: {e}")
        print("Make sure the API server is running on http://localhost:8000")

if __name__ == "__main__":
    test_api()