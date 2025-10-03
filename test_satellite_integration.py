"""
Test script to demonstrate the satellite data integration
Shows the difference between satellite data and synthetic fallback
"""

import json
from satellite_data import get_sentinel_data, get_synthetic_fallback_data
from api_server import get_forest_data_for_city

def test_data_sources():
    """Test different data sources for comparison"""
    
    test_city = "Mumbai"
    
    print("🌲 EcoMind Satellite Data Integration Test")
    print("=" * 50)
    print(f"Testing with city: {test_city}")
    
    print("\n1. 🛰️ Testing Satellite Data (requires authentication):")
    print("-" * 40)
    
    try:
        satellite_data = get_sentinel_data(test_city)
        if satellite_data:
            print("✅ Satellite data fetch successful!")
            print(f"   Data source: {satellite_data.get('data_source', 'unknown')}")
            print(f"   Tree count: {satellite_data.get('tree_count', 0):,}")
            print(f"   Forest area: {satellite_data.get('forest_area_ha', 0):.1f} hectares")
            print(f"   Health distribution: {satellite_data.get('health_percentages', {})}")
            
            if 'satellite_info' in satellite_data:
                sat_info = satellite_data['satellite_info']
                print(f"   Dataset: {sat_info.get('dataset', 'unknown')}")
                print(f"   Images used: {sat_info.get('images_used', 0)}")
                print(f"   Date range: {sat_info.get('date_range', 'unknown')}")
            
            if 'vegetation_indices' in satellite_data:
                veg_indices = satellite_data['vegetation_indices']
                print(f"   NDVI mean: {veg_indices.get('ndvi_mean', 0):.3f}")
                print(f"   EVI mean: {veg_indices.get('evi_mean', 0):.3f}")
        else:
            print("❌ No satellite data available (authentication may be required)")
    
    except Exception as e:
        print(f"❌ Satellite data error: {e}")
    
    print("\n2. 📊 Testing Synthetic Fallback Data:")
    print("-" * 40)
    
    synthetic_data = get_synthetic_fallback_data(test_city)
    print("✅ Synthetic data generated successfully!")
    print(f"   Data source: {synthetic_data.get('data_source', 'unknown')}")
    print(f"   Tree count: {synthetic_data.get('tree_count', 0):,}")
    print(f"   Carbon tons: {synthetic_data.get('carbon_tons', 0):.2f}")
    
    print("\n3. 🔄 Testing Integrated Function (automatic fallback):")
    print("-" * 40)
    
    integrated_data = get_forest_data_for_city(test_city)
    print("✅ Integrated data fetch successful!")
    print(f"   Data source: {integrated_data.get('data_source', 'unknown')}")
    print(f"   Tree count: {integrated_data.get('tree_count', 0):,}")
    print(f"   Carbon tons: {integrated_data.get('carbon_tons', 0):.2f}")
    
    print("\n🎯 Summary:")
    print("-" * 40)
    
    if satellite_data and satellite_data.get('data_source') == 'sentinel_2_satellite':
        print("✅ Real satellite data is working!")
        print("🌍 EcoMind is now using Copernicus Sentinel-2 imagery")
        print("📡 Forest health calculated from actual NDVI/EVI indices")
    else:
        print("⚠️ Satellite data not available - using synthetic fallback")
        print("🔧 To enable satellite data:")
        print("   1. Run: python setup_earth_engine.py")
        print("   2. Authenticate with Google Earth Engine")
        print("   3. Test again: python test_satellite_integration.py")
    
    print(f"\n📊 Fallback system: {'✅ Working' if synthetic_data else '❌ Failed'}")
    print(f"🔗 Integration: {'✅ Working' if integrated_data else '❌ Failed'}")

if __name__ == "__main__":
    test_data_sources()
    
    print("\n🚀 Integration test completed!")
    print("\nNext steps:")
    print("1. Start API server: python api_server.py")
    print("2. Check satellite status: curl http://localhost:8000/api/data-source/info")
    print("3. Test location: curl http://localhost:8000/api/data-source/test/mumbai")
    print("4. Use frontend normally - it will automatically use satellite data when available!")