"""
Google Earth Engine Authentication Setup for EcoMind
Run this script to authenticate your Google Earth Engine access
"""

import ee
import sys
import os
from pathlib import Path

def setup_earth_engine_authentication():
    """Setup Google Earth Engine authentication"""
    
    print("🌍 EcoMind - Google Earth Engine Authentication Setup")
    print("=" * 60)
    
    print("\n📋 Prerequisites:")
    print("1. Google account with Earth Engine access")
    print("2. Internet connection")
    print("3. Web browser available")
    
    print("\n🔑 Starting authentication process...")
    
    try:
        # Try to authenticate
        print("\n⏳ Opening web browser for authentication...")
        print("Please complete the authentication in your web browser.")
        print("After successful authentication, return to this terminal.")
        
        ee.Authenticate()
        
        print("\n✅ Authentication successful!")
        
        # Test initialization
        print("\n🧪 Testing Earth Engine initialization...")
        ee.Initialize()
        
        # Test basic functionality
        print("🛰️ Testing basic Earth Engine functionality...")
        test_collection = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        print(f"✅ Successfully connected to Sentinel-2 dataset")
        
        # Test with a small query
        mumbai = ee.Geometry.Point([72.8777, 19.0760]).buffer(1000)
        test_image = (test_collection
                     .filterBounds(mumbai)
                     .filterDate('2023-01-01', '2023-12-31')
                     .first())
        
        if test_image:
            print("✅ Successfully tested data access")
        else:
            print("⚠️ No test data found, but connection works")
        
        print("\n🎉 Google Earth Engine setup complete!")
        print("You can now run EcoMind with real satellite data.")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Authentication failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure you have Google Earth Engine access")
        print("2. Visit: https://signup.earthengine.google.com/")
        print("3. Check your internet connection")
        print("4. Try running: earthengine authenticate")
        
        return False

def check_earth_engine_status():
    """Check if Earth Engine is already authenticated"""
    try:
        ee.Initialize()
        print("✅ Google Earth Engine is already authenticated and working!")
        return True
    except Exception as e:
        print(f"❌ Earth Engine not authenticated: {e}")
        return False

def create_service_account_info():
    """Provide information about service account setup for production"""
    print("\n🏭 For Production Deployment:")
    print("=" * 40)
    print("Consider using a Service Account for automated access:")
    print("\n1. Go to Google Cloud Console")
    print("2. Create a new Service Account")
    print("3. Download the JSON key file")
    print("4. Set environment variable:")
    print("   export GOOGLE_APPLICATION_CREDENTIALS='path/to/key.json'")
    print("\n5. Or use ee.ServiceAccountCredentials() in your code")

if __name__ == "__main__":
    print("🚀 EcoMind Earth Engine Setup")
    
    # Check current status
    if not check_earth_engine_status():
        print("\n🔧 Setting up authentication...")
        if setup_earth_engine_authentication():
            print("\n✅ Setup completed successfully!")
        else:
            print("\n❌ Setup failed. Please check the troubleshooting steps.")
            sys.exit(1)
    
    # Show service account info
    create_service_account_info()
    
    print("\n🌲 Ready to fetch real forest data from satellites!")