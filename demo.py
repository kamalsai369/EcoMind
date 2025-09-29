"""
EcoMind Demo: Urban Forest Intelligence Demonstration
Showcasing key functionality without requiring authentication
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys
import os

# Add the current directory to Python path
sys.path.append(os.getcwd())

def create_synthetic_data():
    """Create synthetic satellite data for demonstration."""
    print("📡 Creating synthetic satellite data for demonstration...")
    
    # Create synthetic 6-band satellite image (256x256)
    np.random.seed(42)
    height, width = 256, 256
    bands = 6
    
    # Simulate different land cover types
    image = np.random.rand(bands, height, width) * 5000  # Simulate digital numbers
    
    # Add some structure to make it look more realistic
    # Simulate vegetation areas with higher NIR (band 4)
    vegetation_mask = np.zeros((height, width))
    vegetation_mask[50:150, 50:150] = 1  # Square vegetation area
    vegetation_mask[100:200, 100:200] = 1  # Overlapping area
    
    # Enhance NIR band in vegetation areas
    image[3] = image[3] + vegetation_mask * 3000
    
    # Create corresponding tree mask
    tree_mask = (vegetation_mask > 0).astype(np.uint8)
    
    return image, tree_mask

def demonstrate_ndvi_calculation(image):
    """Demonstrate NDVI calculation."""
    print("\n🌿 Calculating NDVI...")
    
    # Extract red (band 3) and NIR (band 4) - using 0-based indexing
    red = image[2] / 10000.0  # B3 (red)
    nir = image[3] / 10000.0  # B4 (NIR)
    
    # Calculate NDVI
    ndvi = (nir - red) / (nir + red + 1e-8)
    ndvi = np.clip(ndvi, -1, 1)
    
    print(f"NDVI range: {ndvi.min():.3f} to {ndvi.max():.3f}")
    print(f"Mean NDVI: {ndvi.mean():.3f}")
    
    return ndvi

def demonstrate_health_assessment(tree_mask, ndvi):
    """Demonstrate tree health assessment."""
    print("\n🏥 Assessing tree health...")
    
    healthy = (ndvi > 0.6) & (tree_mask > 0)
    moderate = (ndvi > 0.4) & (ndvi <= 0.6) & (tree_mask > 0)
    stressed = (ndvi > 0.2) & (ndvi <= 0.4) & (tree_mask > 0)
    unhealthy = (ndvi <= 0.2) & (tree_mask > 0)
    
    health_stats = {
        'healthy': int(np.sum(healthy)),
        'moderate': int(np.sum(moderate)),
        'stressed': int(np.sum(stressed)),
        'unhealthy': int(np.sum(unhealthy)),
        'total_pixels': int(np.sum(tree_mask > 0))
    }
    
    print("Tree Health Distribution:")
    for category, count in health_stats.items():
        if category != 'total_pixels':
            percentage = (count / health_stats['total_pixels']) * 100 if health_stats['total_pixels'] > 0 else 0
            print(f"  {category.capitalize()}: {count:,} pixels ({percentage:.1f}%)")
    
    return health_stats

def demonstrate_carbon_estimation(tree_mask, resolution=10):
    """Demonstrate carbon capture estimation."""
    print("\n💨 Estimating carbon capture...")
    
    # Calculate tree area
    tree_area_pixels = np.sum(tree_mask > 0)
    tree_area_m2 = tree_area_pixels * (resolution ** 2)
    tree_area_ha = tree_area_m2 / 10000
    
    # Carbon sequestration rate (tons CO2/ha/year)
    carbon_rate_tropical = 3.5
    carbon_captured = tree_area_ha * carbon_rate_tropical
    
    carbon_stats = {
        'tree_area_m2': float(tree_area_m2),
        'tree_area_ha': float(tree_area_ha),
        'carbon_tons_per_year': float(carbon_captured),
        'tree_count_estimate': int(tree_area_m2 / 25)  # Assume 5m diameter canopy
    }
    
    print(f"Tree Area: {carbon_stats['tree_area_ha']:.2f} hectares")
    print(f"Estimated Trees: {carbon_stats['tree_count_estimate']:,}")
    print(f"Carbon Capture: {carbon_stats['carbon_tons_per_year']:.2f} tons CO₂/year")
    print(f"Equivalent to offsetting {int(carbon_stats['carbon_tons_per_year']/4.6):,} cars/year")
    
    return carbon_stats

def create_visualization(image, tree_mask, ndvi, health_stats):
    """Create visualization of results."""
    print("\n📊 Creating visualizations...")
    
    try:
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # RGB composite (using bands 2, 1, 0 as RGB)
        rgb = image[:3].transpose(1, 2, 0)
        rgb = np.clip(rgb / 3000, 0, 1)  # Normalize for display
        axes[0, 0].imshow(rgb)
        axes[0, 0].set_title('RGB Composite')
        axes[0, 0].axis('off')
        
        # Tree mask
        axes[0, 1].imshow(tree_mask, cmap='Greens')
        axes[0, 1].set_title('Tree Mask')
        axes[0, 1].axis('off')
        
        # NDVI
        im = axes[1, 0].imshow(ndvi, cmap='RdYlGn', vmin=-1, vmax=1)
        axes[1, 0].set_title('NDVI')
        axes[1, 0].axis('off')
        plt.colorbar(im, ax=axes[1, 0], fraction=0.046, pad=0.04)
        
        # Health distribution
        categories = ['Healthy', 'Moderate', 'Stressed', 'Unhealthy']
        values = [health_stats['healthy'], health_stats['moderate'], 
                 health_stats['stressed'], health_stats['unhealthy']]
        colors = ['#2d6a4f', '#52b788', '#ffc107', '#dc3545']
        
        bars = axes[1, 1].bar(categories, values, color=colors)
        axes[1, 1].set_title('Tree Health Distribution')
        axes[1, 1].set_ylabel('Number of Pixels')
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            if value > 0:
                axes[1, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values)*0.01,
                               f'{value}', ha='center', va='bottom')
        
        plt.tight_layout()
        
        # Save the plot
        output_path = 'ecomind_demo_results.png'
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"Visualization saved as: {output_path}")
        
        # Try to show the plot (will work if in interactive environment)
        try:
            plt.show()
        except:
            print("Note: Plot display not available in this environment, but saved to file.")
        
    except Exception as e:
        print(f"Visualization error: {e}")
        print("Continuing without visualization...")

def generate_demo_report(health_stats, carbon_stats):
    """Generate a demonstration report."""
    print("\n📋 Generating EcoMind Analysis Report...")
    
    total_trees = health_stats['total_pixels']
    
    report = f"""
════════════════════════════════════════════════════════════
                    🌳 ECOMIND DEMO REPORT 🌳
════════════════════════════════════════════════════════════

TREE COVERAGE SUMMARY
---------------------
🌲 Total Tree Area: {carbon_stats['tree_area_ha']:.2f} hectares
🌳 Estimated Tree Count: {carbon_stats['tree_count_estimate']:,}
📊 Tree Coverage: {total_trees:,} pixels

TREE HEALTH ASSESSMENT
----------------------
✅ Healthy Trees: {health_stats['healthy']:,} ({health_stats['healthy']/total_trees*100:.1f}%)
🟡 Moderate Health: {health_stats['moderate']:,} ({health_stats['moderate']/total_trees*100:.1f}%)
🟠 Stressed Trees: {health_stats['stressed']:,} ({health_stats['stressed']/total_trees*100:.1f}%)
🔴 Unhealthy Trees: {health_stats['unhealthy']:,} ({health_stats['unhealthy']/total_trees*100:.1f}%)

ENVIRONMENTAL IMPACT
--------------------
💨 Annual CO₂ Sequestration: {carbon_stats['carbon_tons_per_year']:.2f} tons
🚗 Equivalent Cars Offset: {int(carbon_stats['carbon_tons_per_year']/4.6):,} cars/year
🌬️ Oxygen Production: {carbon_stats['carbon_tons_per_year']*0.73:.2f} tons/year
🏭 Air Pollutant Removal: {carbon_stats['tree_area_ha']*50:.0f} kg/year
🌧️ Stormwater Interception: {carbon_stats['tree_area_ha']*2500:.0f} liters/year

KEY INSIGHTS
------------
📈 Overall forest health appears good with {health_stats['healthy']/total_trees*100:.1f}% healthy vegetation
🎯 Carbon sequestration rate: {carbon_stats['carbon_tons_per_year']/carbon_stats['tree_area_ha']:.1f} tons CO₂/ha/year
🌡️ This forest contributes significantly to climate change mitigation
🌿 Regular monitoring recommended for stressed vegetation areas

RECOMMENDATIONS
---------------
🔄 Implement regular NDVI monitoring for early stress detection
💧 Consider irrigation for areas with NDVI < 0.4
🛡️ Protect high-performing vegetation areas (NDVI > 0.6)
🌱 Focus new plantations in areas with low tree coverage
📊 Quarterly health assessments recommended

SDG ALIGNMENT
-------------
🎯 SDG 13: Climate Action (Carbon sequestration)
🌲 SDG 15: Life on Land (Forest conservation)
🏙️ SDG 11: Sustainable Cities (Urban forest management)

════════════════════════════════════════════════════════════
Report generated by EcoMind Urban Forest Intelligence System
Visit: https://github.com/ecomind-ai for more information
════════════════════════════════════════════════════════════
"""
    
    print(report)
    
    # Save report to file
    with open('ecomind_demo_report.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("📄 Report saved as: ecomind_demo_report.txt")

def main():
    """Main demonstration function."""
    print("🌳 EcoMind Urban Forest Intelligence - DEMO MODE")
    print("=" * 60)
    print("This demonstration showcases core EcoMind functionality")
    print("using synthetic satellite data.\n")
    
    # Step 1: Create synthetic data
    image, tree_mask = create_synthetic_data()
    
    # Step 2: Calculate NDVI
    ndvi = demonstrate_ndvi_calculation(image)
    
    # Step 3: Assess tree health
    health_stats = demonstrate_health_assessment(tree_mask, ndvi)
    
    # Step 4: Estimate carbon capture
    carbon_stats = demonstrate_carbon_estimation(tree_mask)
    
    # Step 5: Create visualizations
    create_visualization(image, tree_mask, ndvi, health_stats)
    
    # Step 6: Generate report
    generate_demo_report(health_stats, carbon_stats)
    
    print("\n🎉 EcoMind demonstration completed successfully!")
    print("\n📋 Demo Summary:")
    print(f"   • Processed {image.shape[1]}x{image.shape[2]} pixel satellite image")
    print(f"   • Analyzed {health_stats['total_pixels']:,} tree pixels")
    print(f"   • Estimated {carbon_stats['carbon_tons_per_year']:.1f} tons CO₂/year sequestration")
    print(f"   • Generated visualization and comprehensive report")
    
    print("\n🚀 Next Steps (with real data):")
    print("   1. Authenticate Google Earth Engine: ee.Authenticate()")
    print("   2. Download real Sentinel-2 satellite data")
    print("   3. Train UNet model for tree detection")
    print("   4. Deploy Streamlit dashboard for monitoring")
    
    print("\n🌍 Ready to help save the planet, one tree at a time! 🌳")

if __name__ == "__main__":
    main()