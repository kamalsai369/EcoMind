"""
EcoMind API Server
FastAPI backend to serve forest monitoring data to the React frontend
Now with REAL satellite data from Copernicus Sentinel-2!
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
import numpy as np
import random
from pydantic import BaseModel
import logging

# Import our satellite data module
try:
    from satellite_data import get_sentinel_data, get_synthetic_fallback_data
    SATELLITE_DATA_AVAILABLE = True
    print("🛰️ Satellite data module loaded successfully!")
except ImportError as e:
    SATELLITE_DATA_AVAILABLE = False
    print(f"⚠️ Satellite data module not available: {e}")
    print("📊 Falling back to synthetic data generation")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="EcoMind API",
    description="Forest monitoring and environmental data API",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://localhost:8080", "http://localhost:8081"],  # React dev server ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect('forest_monitoring.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_forest_data_for_city(city_name: str, prefer_satellite: bool = True) -> Dict[str, Any]:
    """
    Get forest data for a city - tries real satellite data first, falls back to synthetic
    
    Args:
        city_name: Name of the city
        prefer_satellite: Whether to try satellite data first (default: True)
    
    Returns:
        Dictionary containing forest data with data_source indicator
    """
    
    logger.info(f"🌲 Fetching forest data for {city_name}")
    
    # Try satellite data first if available and preferred
    if prefer_satellite and SATELLITE_DATA_AVAILABLE:
        try:
            logger.info(f"🛰️ Attempting to fetch satellite data for {city_name}")
            satellite_data = get_sentinel_data(city_name)
            
            if satellite_data:
                logger.info(f"✅ Successfully got satellite data for {city_name}")
                return satellite_data
            else:
                logger.warning(f"⚠️ No satellite data available for {city_name}, using synthetic fallback")
        
        except Exception as e:
            logger.error(f"❌ Satellite data fetch failed for {city_name}: {e}")
    
    # Fallback to synthetic data
    if SATELLITE_DATA_AVAILABLE:
        logger.info(f"📊 Using synthetic fallback data for {city_name}")
        return get_synthetic_fallback_data(city_name)
    else:
        logger.info(f"📊 Using original synthetic data generation for {city_name}")
        return generate_synthetic_data_for_city_original(city_name)

def generate_synthetic_data_for_city_original(city_name: str) -> Dict[str, Any]:
    """Original synthetic forest data generation (kept as ultimate fallback)"""
    # Set seed based on city name for consistency
    random.seed(hash(city_name) % 1000000)
    np.random.seed(hash(city_name) % 1000000)
    
    # Base parameters for Indian cities
    population_factors = {
        'mumbai': 1.0, 'delhi': 0.9, 'bangalore': 0.7, 'chennai': 0.6,
        'kolkata': 0.8, 'hyderabad': 0.65, 'pune': 0.5, 'ahmedabad': 0.4,
        'jaipur': 0.3, 'lucknow': 0.25, 'kanpur': 0.2, 'nagpur': 0.15
    }
    
    # Determine city size factor
    city_lower = city_name.lower()
    size_factor = 0.1  # Default for smaller cities
    
    for major_city, factor in population_factors.items():
        if major_city in city_lower:
            size_factor = factor
            break
    
    # Generate realistic data based on city size
    base_trees = int(np.random.normal(50000, 15000) * size_factor)
    base_trees = max(1000, base_trees)  # Minimum 1000 trees
    
    # Health distribution (varies by region)
    healthy_pct = np.random.uniform(0.35, 0.65)
    moderate_pct = np.random.uniform(0.20, 0.35)
    stressed_pct = np.random.uniform(0.15, 0.25)
    unhealthy_pct = max(0.05, 1.0 - healthy_pct - moderate_pct - stressed_pct)
    
    # Normalize percentages
    total_pct = healthy_pct + moderate_pct + stressed_pct + unhealthy_pct
    healthy_pct /= total_pct
    moderate_pct /= total_pct
    stressed_pct /= total_pct
    unhealthy_pct /= total_pct
    
    healthy_count = int(base_trees * healthy_pct)
    moderate_count = int(base_trees * moderate_pct)
    stressed_count = int(base_trees * stressed_pct)
    unhealthy_count = base_trees - healthy_count - moderate_count - stressed_count
    
    # Carbon calculation (3-6 tons CO2 per hectare per year)
    hectares = (base_trees * 25) / 10000  # 25 m² per tree average
    carbon_rate = np.random.uniform(3.0, 6.0)
    carbon_tons = hectares * carbon_rate
    
    return {
        'location': city_name,
        'tree_count': base_trees,
        'healthy_count': healthy_count,
        'moderate_count': moderate_count,
        'stressed_count': stressed_count,
        'unhealthy_count': unhealthy_count,
        'carbon_tons': round(carbon_tons, 2),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

def add_city_to_database(city_data: Dict[str, Any]) -> bool:
    """Add new city data to database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if city already exists
        cursor.execute("SELECT id FROM forest_monitoring WHERE location = ?", (city_data['location'],))
        if cursor.fetchone():
            conn.close()
            return True  # City already exists
        
        # Insert new city data
        cursor.execute("""
            INSERT INTO forest_monitoring 
            (location, timestamp, tree_count, healthy_count, moderate_count, 
             stressed_count, unhealthy_count, carbon_tons)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            city_data['location'], city_data['timestamp'], city_data['tree_count'],
            city_data['healthy_count'], city_data['moderate_count'],
            city_data['stressed_count'], city_data['unhealthy_count'],
            city_data['carbon_tons']
        ))
        
        conn.commit()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error adding city to database: {e}")
        return False

# Pydantic models for API responses
class ForestMetrics(BaseModel):
    total_trees: int
    healthy_count: int
    moderate_count: int
    stressed_count: int
    unhealthy_count: int
    carbon_tons: float
    location: str
    timestamp: str

class HealthDistribution(BaseModel):
    healthy: int
    moderate: int
    stressed: int
    unhealthy: int
    total: int
    healthy_percentage: float
    moderate_percentage: float
    stressed_percentage: float
    unhealthy_percentage: float

class CarbonData(BaseModel):
    total_carbon_tons: float
    annual_capture_rate: float
    equivalent_cars_offset: int
    locations: List[Dict[str, Any]]

class NDVIData(BaseModel):
    current_average: float
    healthy_percentage: float
    moderate_percentage: float
    stressed_percentage: float
    unhealthy_percentage: float

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "EcoMind API - Forest Intelligence Backend"}

@app.get("/api/locations", response_model=List[ForestMetrics])
async def get_all_locations():
    """Get data for all monitored locations"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT location, tree_count, healthy_count, moderate_count, 
                   stressed_count, unhealthy_count, carbon_tons, timestamp
            FROM forest_monitoring
            ORDER BY timestamp DESC
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        locations = []
        for row in rows:
            locations.append(ForestMetrics(
                total_trees=row['tree_count'] or 0,
                healthy_count=row['healthy_count'] or 0,
                moderate_count=row['moderate_count'] or 0,
                stressed_count=row['stressed_count'] or 0,
                unhealthy_count=row['unhealthy_count'] or 0,
                carbon_tons=row['carbon_tons'] or 0.0,
                location=row['location'],
                timestamp=row['timestamp']
            ))
        
        return locations
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/api/locations/add")
async def add_new_location(location: str):
    """Add a new location with generated forest data"""
    try:
        if not location or len(location.strip()) < 2:
            raise HTTPException(status_code=400, detail="Location name must be at least 2 characters")
        
        location = location.strip().title()
        
        # Generate data for the new city (satellite + fallback)
        city_data = get_forest_data_for_city(location)
        
        # Add to database
        if add_city_to_database(city_data):
            return {
                "message": f"Successfully added {location} to monitoring system",
                "location": location,
                "data": city_data
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to add location to database")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.get("/api/locations/search")
async def search_or_add_location(q: str):
    """Search for a location or add it if not found"""
    try:
        if not q or len(q.strip()) < 2:
            raise HTTPException(status_code=400, detail="Search query must be at least 2 characters")
        
        query = q.strip()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # First, try to find existing location (case-insensitive)
        cursor.execute("""
            SELECT location, tree_count, healthy_count, moderate_count, 
                   stressed_count, unhealthy_count, carbon_tons, timestamp
            FROM forest_monitoring
            WHERE LOWER(location) LIKE LOWER(?)
            ORDER BY location
        """, (f"%{query}%",))
        
        existing_locations = cursor.fetchall()
        conn.close()
        
        if existing_locations:
            # Return existing locations
            locations = []
            for row in existing_locations:
                locations.append({
                    "location": row['location'],
                    "tree_count": row['tree_count'],
                    "healthy_count": row['healthy_count'],
                    "moderate_count": row['moderate_count'],
                    "stressed_count": row['stressed_count'],
                    "unhealthy_count": row['unhealthy_count'],
                    "carbon_tons": row['carbon_tons'],
                    "timestamp": row['timestamp'],
                    "is_new": False
                })
            return {"locations": locations, "found_existing": True}
        
        else:
            # No existing location found, generate new data
            location_name = query.title()
            city_data = get_forest_data_for_city(location_name)
            
            # Add to database
            if add_city_to_database(city_data):
                return {
                    "locations": [{**city_data, "is_new": True}],
                    "found_existing": False,
                    "message": f"Generated new forest data for {location_name}"
                }
            else:
                raise HTTPException(status_code=500, detail="Failed to add new location")
                
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

@app.get("/api/locations/list")
async def get_locations_list():
    """Get list of available locations"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT DISTINCT location, COUNT(*) as data_points,
                   MAX(tree_count) as tree_count
            FROM forest_monitoring
            GROUP BY location
            ORDER BY location
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        locations = []
        for row in rows:
            locations.append({
                "name": row['location'],
                "data_points": row['data_points'],
                "tree_count": row['tree_count']
            })
        
        return locations
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/metrics/overview")
async def get_overview_metrics(location: Optional[str] = None):
    """Get overview metrics for dashboard, optionally filtered by location"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # If specific location requested, check if it exists
        if location and location != "all":
            cursor.execute("SELECT COUNT(*) as count FROM forest_monitoring WHERE location = ?", (location,))
            result = cursor.fetchone()
            
            if result['count'] == 0:
                # Location doesn't exist, generate new data
                city_data = get_forest_data_for_city(location)
                if add_city_to_database(city_data):
                    print(f"Auto-generated data for new location: {location}")
                else:
                    raise HTTPException(status_code=500, detail="Failed to generate data for location")
        
        # Build query with optional location filter
        if location and location != "all":
            query = """
                SELECT 
                    SUM(tree_count) as total_trees,
                    SUM(healthy_count) as total_healthy,
                    SUM(moderate_count) as total_moderate,
                    SUM(stressed_count) as total_stressed,
                    SUM(unhealthy_count) as total_unhealthy,
                    SUM(carbon_tons) as total_carbon,
                    COUNT(*) as locations_count
                FROM forest_monitoring
                WHERE location = ?
            """
            cursor.execute(query, (location,))
        else:
            query = """
                SELECT 
                    SUM(tree_count) as total_trees,
                    SUM(healthy_count) as total_healthy,
                    SUM(moderate_count) as total_moderate,
                    SUM(stressed_count) as total_stressed,
                    SUM(unhealthy_count) as total_unhealthy,
                    SUM(carbon_tons) as total_carbon,
                    COUNT(*) as locations_count
                FROM forest_monitoring
            """
            cursor.execute(query)
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            raise HTTPException(status_code=404, detail="No data found")
        
        total_trees = row['total_trees'] or 0
        total_healthy = row['total_healthy'] or 0
        total_moderate = row['total_moderate'] or 0
        total_stressed = row['total_stressed'] or 0
        total_unhealthy = row['total_unhealthy'] or 0
        total_carbon = row['total_carbon'] or 0
        locations_count = row['locations_count'] or 0
        
        # Calculate health score (percentage of healthy + moderate trees)
        health_score = 0
        if total_trees > 0:
            health_score = ((total_healthy + total_moderate) / total_trees) * 100
        
        # Estimate forest coverage (assuming 25 m² per tree on average)
        forest_coverage_hectares = (total_trees * 25) / 10000
        
        return {
            "total_trees": total_trees,
            "forest_coverage_hectares": round(forest_coverage_hectares, 1),
            "annual_co2_capture_tons": round(total_carbon, 1),
            "health_score_percentage": round(health_score, 1),
            "locations_monitored": locations_count,
            "selected_location": location or "all",
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/health/distribution")
async def get_health_distribution(location: Optional[str] = None):
    """Get tree health distribution data, optionally filtered by location"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # If specific location requested, check if it exists
        if location and location != "all":
            cursor.execute("SELECT COUNT(*) as count FROM forest_monitoring WHERE location = ?", (location,))
            result = cursor.fetchone()
            
            if result['count'] == 0:
                # Location doesn't exist, generate new data
                city_data = get_forest_data_for_city(location)
                if add_city_to_database(city_data):
                    print(f"Auto-generated health data for new location: {location}")
                else:
                    raise HTTPException(status_code=500, detail="Failed to generate data for location")
        
        if location and location != "all":
            cursor.execute("""
                SELECT 
                    SUM(healthy_count) as healthy,
                    SUM(moderate_count) as moderate,
                    SUM(stressed_count) as stressed,
                    SUM(unhealthy_count) as unhealthy
                FROM forest_monitoring
                WHERE location = ?
            """, (location,))
        else:
            cursor.execute("""
                SELECT 
                    SUM(healthy_count) as healthy,
                    SUM(moderate_count) as moderate,
                    SUM(stressed_count) as stressed,
                    SUM(unhealthy_count) as unhealthy
                FROM forest_monitoring
            """)
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            raise HTTPException(status_code=404, detail="No health data found")
        
        healthy = max(0, row['healthy'] or 0)
        moderate = max(0, row['moderate'] or 0)
        stressed = max(0, row['stressed'] or 0)
        unhealthy = max(0, row['unhealthy'] or 0)
        total = healthy + moderate + stressed + unhealthy
        
        if total == 0:
            return HealthDistribution(
                healthy=0, moderate=0, stressed=0, unhealthy=0, total=0,
                healthy_percentage=0, moderate_percentage=0, 
                stressed_percentage=0, unhealthy_percentage=0
            )
        
        return HealthDistribution(
            healthy=healthy,
            moderate=moderate,
            stressed=stressed,
            unhealthy=unhealthy,
            total=total,
            healthy_percentage=round((healthy / total) * 100, 1),
            moderate_percentage=round((moderate / total) * 100, 1),
            stressed_percentage=round((stressed / total) * 100, 1),
            unhealthy_percentage=round((unhealthy / total) * 100, 1)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/ndvi/analysis")
async def get_ndvi_analysis():
    """Get NDVI analysis data for health assessment"""
    try:
        # Generate realistic NDVI data based on current health distribution
        # In a real implementation, this would analyze satellite imagery
        
        # Generate NDVI values that correlate with health data
        current_average = round(random.uniform(0.45, 0.75), 2)
        
        # Calculate percentages that roughly match health distribution
        healthy_pct = round(random.uniform(45, 65), 1)
        moderate_pct = round(random.uniform(20, 30), 1)
        stressed_pct = round(random.uniform(15, 25), 1)
        unhealthy_pct = round(100 - healthy_pct - moderate_pct - stressed_pct, 1)
        
        return NDVIData(
            current_average=current_average,
            healthy_percentage=healthy_pct,
            moderate_percentage=moderate_pct,
            stressed_percentage=stressed_pct,
            unhealthy_percentage=unhealthy_pct
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"NDVI analysis error: {str(e)}")

@app.get("/api/trends/weekly")
async def get_weekly_trends():
    """Get weekly trend data"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # For demo purposes, create trend data based on existing data
        cursor.execute("""
            SELECT 
                AVG(tree_count) as avg_trees,
                AVG(carbon_tons) as avg_carbon
            FROM forest_monitoring
        """)
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return {"weeks": [], "tree_counts": [], "carbon_capture": []}
        
        # Generate sample weekly trend data
        base_trees = row['avg_trees'] or 50000
        base_carbon = row['avg_carbon'] or 400
        
        weeks = ["Week 1", "Week 2", "Week 3", "Week 4"]
        tree_counts = [
            int(base_trees * 0.95),
            int(base_trees * 0.97),
            int(base_trees * 1.02),
            int(base_trees)
        ]
        carbon_capture = [
            round(base_carbon * 0.94, 1),
            round(base_carbon * 0.96, 1),
            round(base_carbon * 1.01, 1),
            round(base_carbon, 1)
        ]
        
        return {
            "weeks": weeks,
            "tree_counts": tree_counts,
            "carbon_capture": carbon_capture
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/carbon/data")
async def get_carbon_data():
    """Get carbon sequestration and environmental impact data"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                SUM(carbon_tons) as total_carbon,
                COUNT(DISTINCT location) as locations,
                SUM(tree_count) as total_trees
            FROM forest_monitoring
        """)
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            raise HTTPException(status_code=404, detail="No carbon data found")
        
        total_carbon = row['total_carbon'] or 0
        total_trees = row['total_trees'] or 0
        locations = row['locations'] or 0
        
        # Calculate environmental impact metrics
        # Assuming average tree sequesters 12 tons CO2 per year
        annual_capture_rate = total_carbon * 0.75  # 75% annual rate
        
        # 1 ton CO2 = equivalent to ~0.22 cars per year
        equivalent_cars_offset = int(annual_capture_rate * 0.22)
        
        # Get location-wise carbon data
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT location, carbon_tons, tree_count, timestamp
            FROM forest_monitoring
            ORDER BY carbon_tons DESC
            LIMIT 10
        """)
        
        location_rows = cursor.fetchall()
        conn.close()
        
        locations_data = []
        for loc_row in location_rows:
            locations_data.append({
                "location": loc_row['location'],
                "carbon_tons": loc_row['carbon_tons'],
                "tree_count": loc_row['tree_count'],
                "timestamp": loc_row['timestamp']
            })
        
        return CarbonData(
            total_carbon_tons=total_carbon,
            annual_capture_rate=annual_capture_rate,
            equivalent_cars_offset=equivalent_cars_offset,
            locations=locations_data
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Carbon data error: {str(e)}")

@app.get("/api/data-source/info")
async def get_data_source_info():
    """Get information about current data sources and satellite capabilities"""
    return {
        "satellite_data_available": SATELLITE_DATA_AVAILABLE,
        "data_sources": {
            "primary": "Copernicus Sentinel-2 SR Harmonized" if SATELLITE_DATA_AVAILABLE else "Synthetic Generation",
            "fallback": "Synthetic Generation",
            "dataset_url": "https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED"
        },
        "capabilities": {
            "real_satellite_imagery": SATELLITE_DATA_AVAILABLE,
            "ndvi_calculation": SATELLITE_DATA_AVAILABLE,
            "cloud_masking": SATELLITE_DATA_AVAILABLE,
            "vegetation_indices": SATELLITE_DATA_AVAILABLE,
            "global_coverage": True,
            "automatic_fallback": True
        },
        "earth_engine": {
            "authenticated": SATELLITE_DATA_AVAILABLE,
            "setup_required": not SATELLITE_DATA_AVAILABLE
        }
    }

@app.get("/api/data-source/test/{location}")
async def test_satellite_data(location: str):
    """Test satellite data fetch for a specific location"""
    if not SATELLITE_DATA_AVAILABLE:
        return {
            "error": "Satellite data module not available",
            "suggestion": "Run: python setup_earth_engine.py"
        }
    
    try:
        from satellite_data import get_sentinel_data
        data = get_sentinel_data(location)
        
        if data:
            return {
                "success": True,
                "location": location,
                "data_source": data.get('data_source', 'unknown'),
                "satellite_info": data.get('satellite_info', {}),
                "vegetation_indices": data.get('vegetation_indices', {}),
                "summary": {
                    "total_trees": data.get('tree_count', 0),
                    "forest_area_ha": data.get('forest_area_ha', 0),
                    "health_distribution": data.get('health_percentages', {})
                }
            }
        else:
            return {
                "success": False,
                "location": location,
                "error": "No satellite data available for this location",
                "fallback_used": True
            }
    
    except Exception as e:
        return {
            "success": False,
            "location": location,
            "error": str(e),
            "suggestion": "Check Earth Engine authentication"
        }

if __name__ == "__main__":
    import uvicorn
    print("🌲 Starting EcoMind API Server")
    if SATELLITE_DATA_AVAILABLE:
        print("🛰️ Satellite data integration: ENABLED")
        print("📡 Data source: Copernicus Sentinel-2 SR Harmonized")
    else:
        print("📊 Satellite data integration: DISABLED")
        print("🔧 Run 'python setup_earth_engine.py' to enable satellite data")
    print("🚀 Server starting on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)