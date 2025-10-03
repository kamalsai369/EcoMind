"""
EcoMind Satellite Data Installation and Testing Script
Run this to install dependencies and test the satellite data integration
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔧 {description}")
    print(f"   Command: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"   ✅ Success!")
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Failed: {e}")
        if e.stderr:
            print(f"   Error: {e.stderr.strip()}")
        return False

def check_python_packages():
    """Check if required packages are installed"""
    print("\n📦 Checking Python packages...")
    
    required_packages = [
        'earthengine-api',
        'google-auth',
        'google-auth-oauthlib',
        'fastapi',
        'uvicorn'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - MISSING")
            missing_packages.append(package)
    
    return missing_packages

def install_packages():
    """Install required packages"""
    print("\n🚀 Installing EcoMind satellite data dependencies...")
    
    # Install from requirements
    success = run_command(
        "pip install -r api_requirements.txt",
        "Installing packages from api_requirements.txt"
    )
    
    if not success:
        print("\n❌ Package installation failed!")
        return False
    
    print("\n✅ All packages installed successfully!")
    return True

def test_earth_engine_import():
    """Test if Earth Engine can be imported"""
    print("\n🌍 Testing Google Earth Engine import...")
    
    try:
        import ee
        print("   ✅ earthengine-api imported successfully")
        return True
    except ImportError as e:
        print(f"   ❌ Failed to import earthengine-api: {e}")
        return False

def test_satellite_module():
    """Test our satellite data module"""
    print("\n🛰️ Testing satellite data module...")
    
    try:
        from satellite_data import SentinelDataFetcher, get_sentinel_data
        print("   ✅ Satellite data module imported successfully")
        
        # Test fetcher initialization
        fetcher = SentinelDataFetcher()
        print(f"   📡 Earth Engine authenticated: {fetcher.authenticated}")
        
        return fetcher.authenticated
    except ImportError as e:
        print(f"   ❌ Failed to import satellite module: {e}")
        return False
    except Exception as e:
        print(f"   ⚠️ Satellite module imported but Earth Engine not authenticated: {e}")
        return False

def test_api_endpoints():
    """Test the new API endpoints"""
    print("\n🔌 Testing API endpoints...")
    
    try:
        # Import the modified API server
        from api_server import app
        print("   ✅ Modified API server imported successfully")
        
        # Test that our new functions exist
        from api_server import get_forest_data_for_city
        print("   ✅ New satellite-enabled data function available")
        
        return True
    except ImportError as e:
        print(f"   ❌ Failed to import API server: {e}")
        return False

def run_setup_guide():
    """Show setup guide for Earth Engine authentication"""
    print("\n" + "="*60)
    print("🔑 GOOGLE EARTH ENGINE AUTHENTICATION SETUP")
    print("="*60)
    print("\nTo enable real satellite data, you need to:")
    print("\n1. 📝 Sign up for Google Earth Engine access:")
    print("   https://signup.earthengine.google.com/")
    print("\n2. 🔐 Run authentication setup:")
    print("   python setup_earth_engine.py")
    print("\n3. 🌐 Or authenticate manually:")
    print("   earthengine authenticate")
    print("\n4. 🧪 Test the integration:")
    print("   python test_satellite_integration.py")
    print("\n" + "="*60)

def main():
    print("🌲 EcoMind Satellite Data Integration Setup")
    print("=" * 50)
    
    # Check current directory
    if not os.path.exists('api_server.py'):
        print("❌ Please run this script from the EcoMind project directory")
        return
    
    # Check packages
    missing_packages = check_python_packages()
    
    if missing_packages:
        print(f"\n📦 Missing packages: {missing_packages}")
        install_result = install_packages()
        if not install_result:
            return
    else:
        print("\n✅ All required packages are already installed!")
    
    # Test imports
    if not test_earth_engine_import():
        return
    
    # Test our satellite module
    satellite_available = test_satellite_module()
    
    # Test API
    if not test_api_endpoints():
        return
    
    print("\n🎉 EcoMind Satellite Integration Setup Complete!")
    print("\n📊 Current Status:")
    print(f"   📦 Packages: ✅ Installed")
    print(f"   🛰️ Satellite Module: ✅ Available")
    print(f"   🌍 Earth Engine: {'✅ Authenticated' if satellite_available else '❌ Not Authenticated'}")
    print(f"   🔌 API Server: ✅ Updated")
    
    if not satellite_available:
        print("\n⚠️ Satellite data not available - authentication required")
        run_setup_guide()
    else:
        print("\n🚀 Ready to use real satellite data!")
        print("\nNext steps:")
        print("1. Start the API server: python api_server.py")
        print("2. Test satellite data: curl http://localhost:8000/api/data-source/info")
        print("3. Test a location: curl http://localhost:8000/api/data-source/test/mumbai")

if __name__ == "__main__":
    main()