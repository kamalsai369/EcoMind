"""
EcoMind Satellite Data Module
Real satellite data fetcher using Google Earth Engine and Copernicus Sentinel-2 SR Harmonized
"""

import ee
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime, timedelta
import logging
import time
import json

logger = logging.getLogger(__name__)

class SentinelDataFetcher:
    """Fetches real satellite data from Copernicus Sentinel-2 SR Harmonized dataset"""
    
    def __init__(self):
        """Initialize Earth Engine authentication"""
        self.authenticated = False
        self.initialize_earth_engine()
    
    def initialize_earth_engine(self):
        """Initialize and authenticate Google Earth Engine"""
        try:
            # Try to initialize Earth Engine
            ee.Initialize()
            self.authenticated = True
            logger.info("Google Earth Engine initialized successfully")
        except Exception as e:
            logger.warning(f"Earth Engine initialization failed: {e}")
            logger.info("Please authenticate using: earthengine authenticate")
            self.authenticated = False
    
    def get_coordinates_for_city(self, city_name: str) -> Tuple[float, float]:
        """Get approximate coordinates for a city"""
        # Expanded coordinate database
        city_coordinates = {
            # India - Major Cities
            "mumbai": [19.0760, 72.8777],
            "delhi": [28.7041, 77.1025], 
            "bangalore": [12.9716, 77.5946],
            "chennai": [13.0827, 80.2707],
            "kolkata": [22.5726, 88.3639],
            "hyderabad": [17.3850, 78.4867],
            "pune": [18.5204, 73.8567],
            "ahmedabad": [23.0225, 72.5714],
            "jaipur": [26.9124, 75.7873],
            "kakinada": [16.9891, 82.2475],
            "visakhapatnam": [17.6868, 83.2185],
            "vijayawada": [16.5062, 80.6480],
            "guntur": [16.3067, 80.4365],
            "tirupati": [13.6288, 79.4192],
            "kochi": [9.9312, 76.2673],
            "trivandrum": [8.5241, 76.9366],
            
            # International
            "new york": [40.7128, -74.0060],
            "london": [51.5074, -0.1278],
            "paris": [48.8566, 2.3522],
            "berlin": [52.5200, 13.4050],
            "tokyo": [35.6762, 139.6503],
            "beijing": [39.9042, 116.4074],
            "sydney": [-33.8688, 151.2093],
            "sao paulo": [-23.5505, -46.6333],
        }
        
        city_lower = city_name.lower().strip()
        
        # Direct match
        if city_lower in city_coordinates:
            return city_coordinates[city_lower]
        
        # Partial match
        for city, coords in city_coordinates.items():
            if city in city_lower or city_lower in city:
                return coords
        
        # Default to Kakinada (our reference location)
        logger.warning(f"Coordinates not found for {city_name}, using default location")
        return [16.9891, 82.2475]
    
    def create_roi_from_coordinates(self, lat: float, lon: float, buffer_km: float = 5.0) -> ee.Geometry:
        """Create Region of Interest around coordinates"""
        # Convert km to degrees (approximate)
        buffer_deg = buffer_km / 111.0  # 1 degree ≈ 111 km
        
        # Create bounding box
        bounds = [
            [lon - buffer_deg, lat - buffer_deg],  # SW
            [lon - buffer_deg, lat + buffer_deg],  # NW  
            [lon + buffer_deg, lat + buffer_deg],  # NE
            [lon + buffer_deg, lat - buffer_deg],  # SE
            [lon - buffer_deg, lat - buffer_deg]   # Close polygon
        ]
        
        return ee.Geometry.Polygon([bounds])
    
    def mask_clouds_and_shadows(self, image: ee.Image) -> ee.Image:
        """Advanced cloud and shadow masking for Sentinel-2"""
        # Scene Classification Layer (SCL) band
        scl = image.select('SCL')
        
        # Create mask for clear pixels
        clear_pixels = scl.eq(4).Or(scl.eq(5)).Or(scl.eq(6)).Or(scl.eq(11))  # Vegetation, not vegetated, water, snow
        
        # Additional cloud probability masking if available
        if 'MSK_CLDPRB' in image.bandNames().getInfo():
            cloud_prob = image.select('MSK_CLDPRB')
            clear_pixels = clear_pixels.And(cloud_prob.lt(20))  # Less than 20% cloud probability
        
        return image.updateMask(clear_pixels)
    
    def calculate_vegetation_indices(self, image: ee.Image) -> ee.Image:
        """Calculate vegetation indices from Sentinel-2 bands"""
        # NDVI (Normalized Difference Vegetation Index)
        ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
        
        # EVI (Enhanced Vegetation Index)
        evi = image.expression(
            '2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))',
            {
                'NIR': image.select('B8'),
                'RED': image.select('B4'),
                'BLUE': image.select('B2')
            }
        ).rename('EVI')
        
        # SAVI (Soil Adjusted Vegetation Index)
        savi = image.expression(
            '((NIR - RED) / (NIR + RED + 0.5)) * 1.5',
            {
                'NIR': image.select('B8'),
                'RED': image.select('B4')
            }
        ).rename('SAVI')
        
        return image.addBands([ndvi, evi, savi])
    
    def get_forest_health_from_satellite(self, city_name: str, days_back: int = 30) -> Dict[str, Any]:
        """Fetch real forest health data from Sentinel-2 satellite imagery"""
        
        if not self.authenticated:
            logger.error("Earth Engine not authenticated. Falling back to synthetic data.")
            return None
        
        try:
            # Get coordinates for city
            lat, lon = self.get_coordinates_for_city(city_name)
            roi = self.create_roi_from_coordinates(lat, lon, buffer_km=10)
            
            # Date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            # Load Sentinel-2 Surface Reflectance collection
            collection = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
                         .filterBounds(roi)
                         .filterDate(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
                         .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 30))
                         .map(self.mask_clouds_and_shadows)
                         .map(self.calculate_vegetation_indices))
            
            # Check if we have any images
            image_count = collection.size().getInfo()
            if image_count == 0:
                logger.warning(f"No clear Sentinel-2 images found for {city_name} in last {days_back} days")
                return None
            
            # Get median composite to reduce cloud influence
            composite = collection.median()
            
            # Calculate statistics over the region
            stats = composite.select(['NDVI', 'EVI', 'SAVI']).reduceRegion(
                reducer=ee.Reducer.mean().combine(
                    reducer2=ee.Reducer.stdDev(),
                    sharedInputs=True
                ).combine(
                    reducer2=ee.Reducer.minMax(),
                    sharedInputs=True
                ),
                geometry=roi,
                scale=10,  # 10m resolution
                maxPixels=1e9
            )
            
            stats_dict = stats.getInfo()
            
            # Extract NDVI statistics
            ndvi_mean = stats_dict.get('NDVI_mean', 0.3)
            ndvi_std = stats_dict.get('NDVI_stdDev', 0.1)
            ndvi_min = stats_dict.get('NDVI_min', 0.0)
            ndvi_max = stats_dict.get('NDVI_max', 0.8)
            
            # Extract EVI statistics  
            evi_mean = stats_dict.get('EVI_mean', 0.2)
            
            # Calculate forest health metrics from vegetation indices
            forest_data = self.calculate_forest_metrics_from_indices(
                ndvi_mean, ndvi_std, ndvi_min, ndvi_max, evi_mean, city_name, roi
            )
            
            forest_data.update({
                'data_source': 'sentinel_2_satellite',
                'satellite_info': {
                    'dataset': 'COPERNICUS/S2_SR_HARMONIZED',
                    'images_used': image_count,
                    'date_range': f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
                    'coordinates': [lat, lon],
                    'buffer_km': 10
                },
                'vegetation_indices': {
                    'ndvi_mean': round(ndvi_mean, 3),
                    'ndvi_std': round(ndvi_std, 3),
                    'ndvi_range': [round(ndvi_min, 3), round(ndvi_max, 3)],
                    'evi_mean': round(evi_mean, 3)
                }
            })
            
            logger.info(f"Successfully fetched satellite data for {city_name}")
            return forest_data
            
        except Exception as e:
            logger.error(f"Error fetching satellite data for {city_name}: {e}")
            return None
    
    def calculate_forest_metrics_from_indices(self, ndvi_mean: float, ndvi_std: float, 
                                            ndvi_min: float, ndvi_max: float, evi_mean: float,
                                            city_name: str, roi: ee.Geometry) -> Dict[str, Any]:
        """Calculate forest health metrics from vegetation indices"""
        
        # Estimate forest area based on NDVI thresholds
        # NDVI > 0.3 typically indicates dense vegetation/forest
        # NDVI 0.2-0.3 indicates moderate vegetation
        # NDVI < 0.2 indicates sparse/no vegetation
        
        # Estimate total area in hectares
        area_m2 = roi.area(maxError=1).getInfo()
        total_area_ha = area_m2 / 10000
        
        # Estimate forest coverage based on NDVI
        if ndvi_mean > 0.5:
            forest_coverage_pct = 0.7  # 70% forest coverage
        elif ndvi_mean > 0.3:
            forest_coverage_pct = 0.4  # 40% forest coverage  
        elif ndvi_mean > 0.2:
            forest_coverage_pct = 0.2  # 20% forest coverage
        else:
            forest_coverage_pct = 0.05  # 5% forest coverage
        
        forest_area_ha = total_area_ha * forest_coverage_pct
        
        # Estimate tree count (approximately 400-800 trees per hectare in forests)
        trees_per_hectare = 400 + (ndvi_mean * 400)  # Scale with vegetation density
        total_trees = int(forest_area_ha * trees_per_hectare)
        
        # Health classification based on NDVI and EVI
        # Healthy: NDVI > 0.6, EVI > 0.4
        # Moderate: NDVI 0.4-0.6, EVI 0.2-0.4  
        # Stressed: NDVI 0.2-0.4, EVI 0.1-0.2
        # Unhealthy: NDVI < 0.2, EVI < 0.1
        
        if ndvi_mean > 0.6 and evi_mean > 0.4:
            healthy_pct = 0.7
            moderate_pct = 0.2
            stressed_pct = 0.08
            unhealthy_pct = 0.02
        elif ndvi_mean > 0.4 and evi_mean > 0.2:
            healthy_pct = 0.5
            moderate_pct = 0.3
            stressed_pct = 0.15
            unhealthy_pct = 0.05
        elif ndvi_mean > 0.2 and evi_mean > 0.1:
            healthy_pct = 0.3
            moderate_pct = 0.3
            stressed_pct = 0.25
            unhealthy_pct = 0.15
        else:
            healthy_pct = 0.15
            moderate_pct = 0.25
            stressed_pct = 0.35
            unhealthy_pct = 0.25
        
        # Calculate tree counts by health category
        healthy_count = int(total_trees * healthy_pct)
        moderate_count = int(total_trees * moderate_pct)
        stressed_count = int(total_trees * stressed_pct)
        unhealthy_count = total_trees - healthy_count - moderate_count - stressed_count
        
        # Carbon sequestration based on forest health
        # Healthy forests: 5-8 tons CO2/hectare/year
        # Moderate forests: 3-5 tons CO2/hectare/year
        # Stressed forests: 1-3 tons CO2/hectare/year
        # Unhealthy forests: 0.5-1 tons CO2/hectare/year
        
        carbon_rate = (healthy_pct * 6.5 + moderate_pct * 4.0 + 
                      stressed_pct * 2.0 + unhealthy_pct * 0.75)
        carbon_tons = forest_area_ha * carbon_rate
        
        return {
            'location': city_name,
            'tree_count': total_trees,
            'healthy_count': healthy_count,
            'moderate_count': moderate_count,
            'stressed_count': stressed_count,
            'unhealthy_count': unhealthy_count,
            'carbon_tons': round(carbon_tons, 2),
            'forest_area_ha': round(forest_area_ha, 2),
            'total_area_ha': round(total_area_ha, 2),
            'forest_coverage_pct': round(forest_coverage_pct * 100, 1),
            'health_percentages': {
                'healthy': round(healthy_pct * 100, 1),
                'moderate': round(moderate_pct * 100, 1),
                'stressed': round(stressed_pct * 100, 1),
                'unhealthy': round(unhealthy_pct * 100, 1)
            },
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }


def get_sentinel_data(city_name: str) -> Optional[Dict[str, Any]]:
    """Main function to get Sentinel-2 satellite data for a city"""
    fetcher = SentinelDataFetcher()
    return fetcher.get_forest_health_from_satellite(city_name)


# Fallback to synthetic data if satellite fails
def get_synthetic_fallback_data(city_name: str) -> Dict[str, Any]:
    """Generate synthetic data as fallback when satellite data unavailable"""
    import random
    import numpy as np
    
    # Set seed for consistency
    random.seed(hash(city_name) % 1000000)
    np.random.seed(hash(city_name) % 1000000)
    
    # City size factors
    population_factors = {
        'mumbai': 1.0, 'delhi': 0.9, 'bangalore': 0.7, 'chennai': 0.6,
        'kolkata': 0.8, 'hyderabad': 0.65, 'pune': 0.5, 'ahmedabad': 0.4,
        'jaipur': 0.3, 'lucknow': 0.25, 'kanpur': 0.2, 'nagpur': 0.15
    }
    
    city_lower = city_name.lower()
    size_factor = 0.1
    
    for major_city, factor in population_factors.items():
        if major_city in city_lower:
            size_factor = factor
            break
    
    # Generate synthetic data
    base_trees = int(np.random.normal(50000, 15000) * size_factor)
    base_trees = max(1000, base_trees)
    
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
    
    # Carbon calculation
    hectares = (base_trees * 25) / 10000
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
        'data_source': 'synthetic_fallback',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }