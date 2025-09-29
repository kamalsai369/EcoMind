"""
EcoMind: Urban Forest Intelligence Utility Functions
A comprehensive toolkit for satellite-based tree detection and environmental analysis.
"""

import ee
import geemap
import rasterio
import numpy as np
import pandas as pd
import geopandas as gpd
from rasterio.windows import Window
from rasterio import features
from pathlib import Path
import cv2
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
from shapely.geometry import shape
import albumentations as A
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Tuple, Dict, List, Optional
import warnings
warnings.filterwarnings('ignore')


class EarthEngineDataDownloader:
    """Google Earth Engine data downloader for Sentinel-2 imagery."""
    
    def __init__(self):
        """Initialize Earth Engine."""
        try:
            ee.Initialize()
        except Exception:
            print("Please authenticate Earth Engine: ee.Authenticate()")
            ee.Authenticate()
            ee.Initialize()
    
    def define_roi(self, coordinates: List[List[float]] = None, 
                   center: List[float] = None, buffer: int = 5000) -> ee.Geometry:
        """
        Define Region of Interest.
        
        Args:
            coordinates: List of [lon, lat] coordinates for polygon
            center: [lon, lat] for center point
            buffer: Buffer distance in meters for center point
        
        Returns:
            Earth Engine Geometry object
        """
        if coordinates:
            return ee.Geometry.Polygon([coordinates])
        elif center:
            return ee.Geometry.Point(center).buffer(buffer)
        else:
            # Default: Kakinada city, India
            return ee.Geometry.Polygon([
                [[82.209, 16.92], [82.209, 16.85],
                 [82.35, 16.85], [82.35, 16.92]]
            ])
    
    def mask_clouds(self, image: ee.Image) -> ee.Image:
        """Mask clouds using Sentinel-2 cloud probability and SCL bands."""
        cloud_prob = image.select('MSK_CLDPRB')
        scl = image.select('SCL')
        
        mask = (cloud_prob.lt(5)
                .And(scl.neq(3))   # Cloud shadows
                .And(scl.neq(8))   # Cloud medium probability
                .And(scl.neq(9))   # Cloud high probability
                .And(scl.neq(10))  # Thin cirrus
                .And(scl.neq(11))) # Snow/ice
        
        return image.updateMask(mask)
    
    def download_sentinel2_data(self, roi: ee.Geometry, start_date: str, 
                               end_date: str, output_folder: str = 'EcoMind_Data') -> Dict:
        """
        Download Sentinel-2 data from Google Earth Engine.
        
        Args:
            roi: Region of Interest
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            output_folder: Google Drive folder name
        
        Returns:
            Dictionary with task information
        """
        # Load and filter collection
        collection = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
                      .filterBounds(roi)
                      .filterDate(start_date, end_date)
                      .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
                      .map(self.mask_clouds))
        
        # Create median composite
        composite = collection.median()
        
        # Select bands for analysis
        bands = ['B2', 'B3', 'B4', 'B8', 'B11', 'B12']
        image_export = composite.select(bands).clip(roi)
        
        # Calculate NDVI
        ndvi = composite.normalizedDifference(['B8', 'B4']).rename('NDVI')
        
        # Create initial tree mask
        tree_mask = ndvi.gt(0.3).selfMask().clip(roi)
        
        # Export tasks
        task_image = ee.batch.Export.image.toDrive(
            image=image_export,
            description='sentinel2_composite',
            folder=output_folder,
            fileNamePrefix='s2_composite',
            region=roi,
            scale=10,
            maxPixels=1e13,
            crs='EPSG:4326'
        )
        
        task_ndvi = ee.batch.Export.image.toDrive(
            image=ndvi.clip(roi),
            description='sentinel2_ndvi',
            folder=output_folder,
            fileNamePrefix='s2_ndvi',
            region=roi,
            scale=10,
            maxPixels=1e13,
            crs='EPSG:4326'
        )
        
        task_mask = ee.batch.Export.image.toDrive(
            image=tree_mask.clip(roi),
            description='tree_mask',
            folder=output_folder,
            fileNamePrefix='s2_tree_mask',
            region=roi,
            scale=10,
            maxPixels=1e13,
            crs='EPSG:4326'
        )
        
        # Start tasks
        task_image.start()
        task_ndvi.start()
        task_mask.start()
        
        return {
            'image_task_id': task_image.id,
            'ndvi_task_id': task_ndvi.id,
            'mask_task_id': task_mask.id,
            'message': f"Tasks started! Check Google Drive folder '{output_folder}' in 10-30 minutes"
        }


class SatelliteDataPreprocessor:
    """Preprocessor for satellite imagery data."""
    
    def __init__(self, image_path: str, mask_path: str, output_dir: str, patch_size: int = 256):
        """
        Initialize preprocessor.
        
        Args:
            image_path: Path to satellite image
            mask_path: Path to tree mask
            output_dir: Output directory for processed data
            patch_size: Size of patches to extract
        """
        self.image_path = image_path
        self.mask_path = mask_path
        self.output_dir = Path(output_dir)
        self.patch_size = patch_size
        
        # Create output directories
        (self.output_dir / 'train' / 'images').mkdir(parents=True, exist_ok=True)
        (self.output_dir / 'train' / 'masks').mkdir(parents=True, exist_ok=True)
        (self.output_dir / 'val' / 'images').mkdir(parents=True, exist_ok=True)
        (self.output_dir / 'val' / 'masks').mkdir(parents=True, exist_ok=True)
    
    def normalize_image(self, image: np.ndarray) -> np.ndarray:
        """Normalize satellite imagery."""
        image = image.astype(np.float32) / 10000.0
        return np.clip(image, 0, 1)
    
    def extract_patches(self) -> Tuple[np.ndarray, np.ndarray]:
        """Extract patches from large satellite image."""
        # Read image
        with rasterio.open(self.image_path) as src:
            image = src.read()  # Shape: (bands, height, width)
            height, width = image.shape[1], image.shape[2]
        
        # Read mask
        with rasterio.open(self.mask_path) as src:
            mask = src.read(1)  # Shape: (height, width)
        
        patches_img = []
        patches_mask = []
        
        # Extract overlapping patches
        stride = self.patch_size // 2  # 50% overlap
        
        for i in range(0, height - self.patch_size + 1, stride):
            for j in range(0, width - self.patch_size + 1, stride):
                # Extract patch
                img_patch = image[:, i:i+self.patch_size, j:j+self.patch_size]
                mask_patch = mask[i:i+self.patch_size, j:j+self.patch_size]
                
                # Skip patches with too few trees
                if np.sum(mask_patch > 0) < 100:
                    continue
                
                # Normalize image
                img_patch = self.normalize_image(img_patch)
                
                # Convert to HWC format
                img_patch = np.transpose(img_patch, (1, 2, 0))
                
                patches_img.append(img_patch)
                patches_mask.append(mask_patch)
        
        return np.array(patches_img), np.array(patches_mask)
    
    def augment_data(self, images: np.ndarray, masks: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Apply data augmentation."""
        transform = A.Compose([
            A.HorizontalFlip(p=0.5),
            A.VerticalFlip(p=0.5),
            A.RandomRotate90(p=0.5),
            A.ShiftScaleRotate(shift_limit=0.1, scale_limit=0.1, rotate_limit=45, p=0.5),
            A.RandomBrightnessContrast(p=0.3),
        ])
        
        aug_images = []
        aug_masks = []
        
        for img, mask in zip(images, masks):
            transformed = transform(image=img, mask=mask)
            aug_images.append(transformed['image'])
            aug_masks.append(transformed['mask'])
        
        return np.array(aug_images), np.array(aug_masks)
    
    def prepare_dataset(self) -> Tuple[int, int]:
        """Complete preprocessing pipeline."""
        print("Extracting patches...")
        images, masks = self.extract_patches()
        print(f"Extracted {len(images)} patches")
        
        # Split train/val
        X_train, X_val, y_train, y_val = train_test_split(
            images, masks, test_size=0.2, random_state=42
        )
        
        # Augment training data
        print("Augmenting training data...")
        X_train_aug, y_train_aug = self.augment_data(X_train, y_train)
        
        # Combine original and augmented
        X_train = np.concatenate([X_train, X_train_aug])
        y_train = np.concatenate([y_train, y_train_aug])
        
        print(f"Final dataset size - Train: {len(X_train)}, Val: {len(X_val)}")
        
        # Save patches
        self._save_patches(X_train, y_train, 'train')
        self._save_patches(X_val, y_val, 'val')
        
        return len(X_train), len(X_val)
    
    def _save_patches(self, images: np.ndarray, masks: np.ndarray, split: str):
        """Save patches as numpy files."""
        for idx, (img, mask) in enumerate(zip(images, masks)):
            np.save(self.output_dir / split / 'images' / f'patch_{idx}.npy', img)
            np.save(self.output_dir / split / 'masks' / f'patch_{idx}.npy', mask)


# UNet Model Components
class DoubleConv(nn.Module):
    """Double convolution block."""
    
    def __init__(self, in_channels: int, out_channels: int):
        super().__init__()
        self.double_conv = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True)
        )
    
    def forward(self, x):
        return self.double_conv(x)


class UNet(nn.Module):
    """UNet model for semantic segmentation."""
    
    def __init__(self, n_channels: int = 6, n_classes: int = 1):
        super().__init__()
        
        # Encoder
        self.enc1 = DoubleConv(n_channels, 64)
        self.pool1 = nn.MaxPool2d(2)
        self.enc2 = DoubleConv(64, 128)
        self.pool2 = nn.MaxPool2d(2)
        self.enc3 = DoubleConv(128, 256)
        self.pool3 = nn.MaxPool2d(2)
        self.enc4 = DoubleConv(256, 512)
        self.pool4 = nn.MaxPool2d(2)
        
        # Bottleneck
        self.bottleneck = DoubleConv(512, 1024)
        
        # Decoder
        self.up4 = nn.ConvTranspose2d(1024, 512, kernel_size=2, stride=2)
        self.dec4 = DoubleConv(1024, 512)
        self.up3 = nn.ConvTranspose2d(512, 256, kernel_size=2, stride=2)
        self.dec3 = DoubleConv(512, 256)
        self.up2 = nn.ConvTranspose2d(256, 128, kernel_size=2, stride=2)
        self.dec2 = DoubleConv(256, 128)
        self.up1 = nn.ConvTranspose2d(128, 64, kernel_size=2, stride=2)
        self.dec1 = DoubleConv(128, 64)
        
        # Output
        self.out = nn.Conv2d(64, n_classes, kernel_size=1)
    
    def forward(self, x):
        # Encoder
        e1 = self.enc1(x)
        e2 = self.enc2(self.pool1(e1))
        e3 = self.enc3(self.pool2(e2))
        e4 = self.enc4(self.pool3(e3))
        
        # Bottleneck
        b = self.bottleneck(self.pool4(e4))
        
        # Decoder with skip connections
        d4 = self.dec4(torch.cat([self.up4(b), e4], dim=1))
        d3 = self.dec3(torch.cat([self.up3(d4), e3], dim=1))
        d2 = self.dec2(torch.cat([self.up2(d3), e2], dim=1))
        d1 = self.dec1(torch.cat([self.up1(d2), e1], dim=1))
        
        return torch.sigmoid(self.out(d1))


class TreeDataset(Dataset):
    """Custom dataset for tree segmentation."""
    
    def __init__(self, data_dir: str, split: str = 'train'):
        self.image_dir = Path(data_dir) / split / 'images'
        self.mask_dir = Path(data_dir) / split / 'masks'
        self.images = sorted(list(self.image_dir.glob('*.npy')))
    
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, idx):
        img_path = self.images[idx]
        mask_path = self.mask_dir / img_path.name
        
        image = np.load(img_path)  # Shape: (H, W, C)
        mask = np.load(mask_path)   # Shape: (H, W)
        
        # Convert to torch tensors
        image = torch.from_numpy(image).permute(2, 0, 1).float()  # (C, H, W)
        mask = torch.from_numpy(mask).unsqueeze(0).float()  # (1, H, W)
        
        # Binary mask
        mask = (mask > 0).float()
        
        return image, mask


class ModelTrainer:
    """Model training utilities."""
    
    def __init__(self, model: nn.Module, device: str = 'cuda'):
        self.model = model
        self.device = torch.device(device if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)
    
    def train_model(self, train_loader: DataLoader, val_loader: DataLoader, 
                   epochs: int = 50, lr: float = 1e-4, save_path: str = 'best_unet_model.pth') -> nn.Module:
        """Train the model."""
        criterion = nn.BCELoss()
        optimizer = optim.Adam(self.model.parameters(), lr=lr)
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=5, factor=0.5)
        
        best_val_loss = float('inf')
        train_losses = []
        val_losses = []
        
        for epoch in range(epochs):
            # Training
            self.model.train()
            train_loss = 0
            for images, masks in tqdm(train_loader, desc=f'Epoch {epoch+1}/{epochs}'):
                images, masks = images.to(self.device), masks.to(self.device)
                
                optimizer.zero_grad()
                outputs = self.model(images)
                loss = criterion(outputs, masks)
                loss.backward()
                optimizer.step()
                
                train_loss += loss.item()
            
            # Validation
            self.model.eval()
            val_loss = 0
            with torch.no_grad():
                for images, masks in val_loader:
                    images, masks = images.to(self.device), masks.to(self.device)
                    outputs = self.model(images)
                    loss = criterion(outputs, masks)
                    val_loss += loss.item()
            
            train_loss /= len(train_loader)
            val_loss /= len(val_loader)
            
            train_losses.append(train_loss)
            val_losses.append(val_loss)
            
            print(f'Epoch {epoch+1}: Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}')
            
            scheduler.step(val_loss)
            
            # Save best model
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                torch.save(self.model.state_dict(), save_path)
                print('Model saved!')
        
        return self.model


class TreeAnalyzer:
    """Tree analysis and carbon estimation."""
    
    def __init__(self, model_path: str, device: str = 'cuda'):
        self.device = torch.device(device if torch.cuda.is_available() else 'cpu')
        self.model = UNet(n_channels=6, n_classes=1).to(self.device)
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.eval()
    
    def predict_trees(self, image_path: str, output_path: str) -> np.ndarray:
        """Predict tree canopy for entire image."""
        with rasterio.open(image_path) as src:
            image = src.read()
            meta = src.meta.copy()
            height, width = image.shape[1], image.shape[2]
        
        # Normalize
        image = image.astype(np.float32) / 10000.0
        image = np.clip(image, 0, 1)
        
        # Predict in patches
        patch_size = 256
        stride = 128
        prediction = np.zeros((height, width), dtype=np.float32)
        count = np.zeros((height, width), dtype=np.float32)
        
        for i in range(0, height - patch_size + 1, stride):
            for j in range(0, width - patch_size + 1, stride):
                patch = image[:, i:i+patch_size, j:j+patch_size]
                patch_tensor = torch.from_numpy(patch).unsqueeze(0).to(self.device)
                
                with torch.no_grad():
                    pred = self.model(patch_tensor)
                    pred = pred.squeeze().cpu().numpy()
                
                prediction[i:i+patch_size, j:j+patch_size] += pred
                count[i:i+patch_size, j:j+patch_size] += 1
        
        # Average overlapping predictions
        prediction = prediction / np.maximum(count, 1)
        prediction = (prediction > 0.5).astype(np.uint8)
        
        # Save prediction
        meta.update(count=1, dtype='uint8')
        with rasterio.open(output_path, 'w', **meta) as dst:
            dst.write(prediction, 1)
        
        return prediction
    
    def calculate_ndvi(self, image_path: str) -> np.ndarray:
        """Calculate NDVI for health assessment."""
        with rasterio.open(image_path) as src:
            red = src.read(3).astype(float) / 10000.0  # B4
            nir = src.read(4).astype(float) / 10000.0  # B8
        
        ndvi = (nir - red) / (nir + red + 1e-8)
        return np.clip(ndvi, -1, 1)
    
    def assess_tree_health(self, tree_mask: np.ndarray, ndvi: np.ndarray) -> Dict:
        """Classify tree health based on NDVI."""
        healthy = (ndvi > 0.6) & (tree_mask > 0)
        moderate = (ndvi > 0.4) & (ndvi <= 0.6) & (tree_mask > 0)
        stressed = (ndvi > 0.2) & (ndvi <= 0.4) & (tree_mask > 0)
        unhealthy = (ndvi <= 0.2) & (tree_mask > 0)
        
        return {
            'healthy': int(np.sum(healthy)),
            'moderate': int(np.sum(moderate)),
            'stressed': int(np.sum(stressed)),
            'unhealthy': int(np.sum(unhealthy)),
            'total_pixels': int(np.sum(tree_mask > 0))
        }
    
    def estimate_carbon(self, tree_mask: np.ndarray, resolution: int = 10) -> Dict:
        """Estimate carbon capture in tons CO2/year."""
        # Calculate tree area
        tree_area_pixels = np.sum(tree_mask > 0)
        tree_area_m2 = tree_area_pixels * (resolution ** 2)
        tree_area_ha = tree_area_m2 / 10000
        
        # Carbon sequestration rates (tons CO2/ha/year)
        carbon_rate_tropical = 3.5  # Tropical/subtropical
        carbon_captured = tree_area_ha * carbon_rate_tropical
        
        return {
            'tree_area_m2': float(tree_area_m2),
            'tree_area_ha': float(tree_area_ha),
            'carbon_tons_per_year': float(carbon_captured),
            'tree_count_estimate': int(tree_area_m2 / 25)  # Assume avg 5m diameter canopy
        }
    
    def vectorize_trees(self, tree_mask: np.ndarray, output_shapefile: str, 
                       crs: str, transform) -> gpd.GeoDataFrame:
        """Convert tree mask to vector polygons."""
        shapes = features.shapes(tree_mask.astype(np.int16), 
                                mask=tree_mask > 0, 
                                transform=transform)
        
        records = [{'geometry': shape(geom), 'value': val} 
                   for geom, val in shapes]
        
        gdf = gpd.GeoDataFrame.from_records(records, crs=crs)
        gdf.to_file(output_shapefile)
        return gdf


class VisualizationUtils:
    """Utilities for visualization and reporting."""
    
    @staticmethod
    def plot_training_history(train_losses: List[float], val_losses: List[float]):
        """Plot training history."""
        plt.figure(figsize=(10, 6))
        plt.plot(train_losses, label='Training Loss', color='blue')
        plt.plot(val_losses, label='Validation Loss', color='red')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.title('Training History')
        plt.legend()
        plt.grid(True)
        plt.show()
    
    @staticmethod
    def plot_prediction_comparison(image: np.ndarray, true_mask: np.ndarray, 
                                 pred_mask: np.ndarray):
        """Plot comparison of true and predicted masks."""
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        # RGB image
        rgb = image[:3].transpose(1, 2, 0)
        rgb = np.clip(rgb * 3000, 0, 255).astype(np.uint8)
        axes[0].imshow(rgb)
        axes[0].set_title('RGB Image')
        axes[0].axis('off')
        
        # True mask
        axes[1].imshow(true_mask, cmap='Greens')
        axes[1].set_title('True Mask')
        axes[1].axis('off')
        
        # Predicted mask
        axes[2].imshow(pred_mask, cmap='Greens')
        axes[2].set_title('Predicted Mask')
        axes[2].axis('off')
        
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def plot_health_distribution(health_stats: Dict):
        """Plot tree health distribution."""
        categories = ['Healthy', 'Moderate', 'Stressed', 'Unhealthy']
        values = [health_stats['healthy'], health_stats['moderate'], 
                 health_stats['stressed'], health_stats['unhealthy']]
        colors = ['#2d6a4f', '#52b788', '#ffc107', '#dc3545']
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(categories, values, color=colors)
        plt.title('Tree Health Distribution')
        plt.ylabel('Number of Pixels')
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values)*0.01,
                    f'{value:,}', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def generate_report(health_stats: Dict, carbon_stats: Dict) -> str:
        """Generate a comprehensive analysis report."""
        total_trees = health_stats['total_pixels']
        
        report = f"""
EcoMind Urban Forest Analysis Report
====================================

TREE COVERAGE SUMMARY
---------------------
Total Tree Area: {carbon_stats['tree_area_ha']:.2f} hectares
Estimated Tree Count: {carbon_stats['tree_count_estimate']:,}
Tree Coverage: {total_trees:,} pixels

TREE HEALTH ASSESSMENT
----------------------
Healthy Trees: {health_stats['healthy']:,} ({health_stats['healthy']/total_trees*100:.1f}%)
Moderate Health: {health_stats['moderate']:,} ({health_stats['moderate']/total_trees*100:.1f}%)
Stressed Trees: {health_stats['stressed']:,} ({health_stats['stressed']/total_trees*100:.1f}%)
Unhealthy Trees: {health_stats['unhealthy']:,} ({health_stats['unhealthy']/total_trees*100:.1f}%)

ENVIRONMENTAL IMPACT
--------------------
Annual CO₂ Sequestration: {carbon_stats['carbon_tons_per_year']:.2f} tons
Equivalent Cars Offset: {int(carbon_stats['carbon_tons_per_year']/4.6):,} cars/year
Oxygen Production: {carbon_stats['carbon_tons_per_year']*0.73:.2f} tons/year
Air Pollutant Removal: {carbon_stats['tree_area_ha']*50:.0f} kg/year
Stormwater Interception: {carbon_stats['tree_area_ha']*2500:.0f} liters/year

RECOMMENDATIONS
---------------
1. Focus reforestation efforts on areas with high stressed/unhealthy tree counts
2. Implement monitoring program for areas showing vegetation stress
3. Consider irrigation or pest management in areas with NDVI < 0.4
4. Protect and maintain areas with healthy vegetation (NDVI > 0.6)
5. Establish buffer zones around healthy forest areas

SDG ALIGNMENT
-------------
- SDG 13: Climate Action (Carbon sequestration)
- SDG 15: Life on Land (Forest conservation)
- SDG 11: Sustainable Cities (Urban forest management)
"""
        return report


def setup_earth_engine():
    """Setup Google Earth Engine authentication."""
    try:
        ee.Initialize()
        print("Earth Engine initialized successfully!")
    except Exception as e:
        print(f"Earth Engine initialization failed: {e}")
        print("Please run: ee.Authenticate()")
        return False
    return True


def create_sample_pipeline():
    """Create a sample EcoMind analysis pipeline."""
    print("🌳 EcoMind Sample Pipeline")
    print("=" * 50)
    
    # 1. Setup Earth Engine
    if not setup_earth_engine():
        return
    
    # 2. Define ROI (example: small area)
    downloader = EarthEngineDataDownloader()
    roi = downloader.define_roi(center=[82.2475, 16.9891], buffer=2000)
    
    # 3. Download data
    print("\n📡 Downloading satellite data...")
    tasks = downloader.download_sentinel2_data(
        roi=roi,
        start_date='2024-01-01',
        end_date='2024-12-31'
    )
    print(tasks['message'])
    
    # 4. Setup preprocessing (when data is available)
    print("\n🔧 Setting up preprocessing pipeline...")
    preprocessor = SatelliteDataPreprocessor(
        image_path='path/to/s2_composite.tif',  # Update with actual path
        mask_path='path/to/s2_tree_mask.tif',   # Update with actual path
        output_dir='./dataset',
        patch_size=256
    )
    
    print("\n✅ Pipeline setup complete!")
    print("Next steps:")
    print("1. Wait for Google Drive downloads to complete")
    print("2. Update file paths in preprocessor")
    print("3. Run preprocessor.prepare_dataset()")
    print("4. Train model using ModelTrainer")
    print("5. Analyze results using TreeAnalyzer")


if __name__ == "__main__":
    create_sample_pipeline()
