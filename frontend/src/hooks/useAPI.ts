import { useQuery } from '@tanstack/react-query';

// Use environment variable for API base URL, fallback to local development
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 
  (import.meta.env.PROD ? '' : 'http://localhost:8000');

// Types for API responses
export interface OverviewMetrics {
  total_trees: number;
  forest_coverage_hectares: number;
  annual_co2_capture_tons: number;
  health_score_percentage: number;
  locations_monitored: number;
  last_updated: string;
}

export interface HealthDistribution {
  healthy: number;
  moderate: number;
  stressed: number;
  unhealthy: number;
  total: number;
  healthy_percentage: number;
  moderate_percentage: number;
  stressed_percentage: number;
  unhealthy_percentage: number;
}

export interface CarbonData {
  total_carbon_tons: number;
  annual_capture_rate: number;
  equivalent_cars_offset: number;
  locations: Array<{
    location: string;
    carbon_tons: number;
    tree_count: number;
    timestamp: string;
  }>;
}

export interface NDVIData {
  current_average: number;
  healthy_percentage: number;
  moderate_percentage: number;
  stressed_percentage: number;
  unhealthy_percentage: number;
}

export interface TrendData {
  weeks: string[];
  tree_counts: number[];
  carbon_capture: number[];
}

export interface LocationInfo {
  name: string;
  data_points: number;
}

// API functions
const fetchOverviewMetrics = async (location?: string): Promise<OverviewMetrics> => {
  const targetLocation = location && location !== 'all' ? location : 'Seattle';
  const url = `${API_BASE_URL}/api/health?location=${encodeURIComponent(targetLocation)}`;
  
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error('Failed to fetch overview metrics');
  }
  const data = await response.json();
  
  // Transform the response to match expected format
  return {
    total_trees: data.tree_distribution?.total || 0,
    forest_coverage_hectares: Math.round((data.tree_distribution?.total || 0) / 100),
    annual_co2_capture_tons: data.carbon_sequestration || 0,
    health_score_percentage: data.health_score || 0,
    locations_monitored: 25,
    last_updated: data.timestamp || new Date().toISOString()
  };
};

const fetchHealthDistribution = async (location?: string): Promise<HealthDistribution> => {
  const targetLocation = location && location !== 'all' ? location : 'Seattle';
  const url = `${API_BASE_URL}/api/health?location=${encodeURIComponent(targetLocation)}`;
    
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error('Failed to fetch health distribution');
  }
  const data = await response.json();
  
  // Transform the response to match expected format
  const dist = data.tree_distribution || {};
  const total = dist.total || 1;
  
  return {
    healthy: dist.healthy || 0,
    moderate: dist.moderate || 0,
    stressed: dist.stressed || 0,
    unhealthy: dist.unhealthy || 0,
    total: total,
    healthy_percentage: Math.round(((dist.healthy || 0) / total) * 100),
    moderate_percentage: Math.round(((dist.moderate || 0) / total) * 100),
    stressed_percentage: Math.round(((dist.stressed || 0) / total) * 100),
    unhealthy_percentage: Math.round(((dist.unhealthy || 0) / total) * 100)
  };
};

const fetchLocationList = async (): Promise<LocationInfo[]> => {
  const response = await fetch(`${API_BASE_URL}/api/locations`);
  if (!response.ok) {
    throw new Error('Failed to fetch location list');
  }
  const data = await response.json();
  
  // Transform the response to match expected format
  return data.map((item: {location: string; total_trees: number; timestamp: string}) => ({
    location: item.location,
    tree_count: item.total_trees,
    timestamp: item.timestamp
  }));
};

const fetchCarbonData = async (): Promise<CarbonData> => {
  const response = await fetch(`${API_BASE_URL}/api/carbon?location=Seattle`);
  if (!response.ok) {
    throw new Error('Failed to fetch carbon data');
  }
  const data = await response.json();
  
  // Transform the response to match expected format
  return {
    total_carbon_tons: data.annual_sequestration_tons || 0,
    annual_capture_rate: data.annual_sequestration_tons || 0,
    equivalent_cars_offset: Math.round((data.co2_equivalent_offset || 0) / 4.6),
    locations: [{
      location: data.location,
      carbon_tons: data.annual_sequestration_tons || 0,
      tree_count: data.trees_monitored || 0,
      timestamp: data.timestamp || new Date().toISOString()
    }]
  };
};

const fetchNDVIData = async (): Promise<NDVIData> => {
  const response = await fetch(`${API_BASE_URL}/api/health?location=Seattle`);
  if (!response.ok) {
    throw new Error('Failed to fetch NDVI data');
  }
  const data = await response.json();
  
  // Transform health data to NDVI format
  const dist = data.tree_distribution || {};
  const total = dist.total || 1;
  
  return {
    current_average: data.health_score || 0,
    healthy_percentage: Math.round(((dist.healthy || 0) / total) * 100),
    moderate_percentage: Math.round(((dist.moderate || 0) / total) * 100),
    stressed_percentage: Math.round(((dist.stressed || 0) / total) * 100),
    unhealthy_percentage: Math.round(((dist.unhealthy || 0) / total) * 100)
  };
};

const fetchTrendData = async (): Promise<TrendData> => {
  const response = await fetch(`${API_BASE_URL}/api/trends?location=Seattle&days=30`);
  if (!response.ok) {
    throw new Error('Failed to fetch trend data');
  }
  const data = await response.json();
  
  // Transform trends data to expected format
  const trends = data.trends || [];
  
  interface TrendItem {
    date: string;
    health_score: number;
    carbon_sequestration: number;
  }
  
  return {
    weeks: trends.map((item: TrendItem) => new Date(item.date).toLocaleDateString()),
    tree_counts: trends.map((item: TrendItem) => Math.round(item.health_score * 1000)), // Scale for visualization
    carbon_capture: trends.map((item: TrendItem) => item.carbon_sequestration || 0)
  };
};

// Custom hooks
export const useOverviewMetrics = (location?: string) => {
  return useQuery({
    queryKey: ['overviewMetrics', location],
    queryFn: () => fetchOverviewMetrics(location),
    refetchInterval: 30000, // Refetch every 30 seconds for real-time updates
  });
};

export const useHealthDistribution = (location?: string) => {
  return useQuery({
    queryKey: ['healthDistribution', location],
    queryFn: () => fetchHealthDistribution(location),
    refetchInterval: 30000,
  });
};

export const useLocationList = () => {
  return useQuery({
    queryKey: ['locationList'],
    queryFn: fetchLocationList,
    refetchInterval: 60000, // Refetch every minute
  });
};

export const useCarbonData = () => {
  return useQuery({
    queryKey: ['carbonData'],
    queryFn: fetchCarbonData,
    refetchInterval: 30000,
  });
};

export const useNDVIData = () => {
  return useQuery({
    queryKey: ['ndviData'],
    queryFn: fetchNDVIData,
    refetchInterval: 30000,
  });
};

export const useTrendData = () => {
  return useQuery({
    queryKey: ['trendData'],
    queryFn: fetchTrendData,
    refetchInterval: 60000, // Refetch every minute for trend data
  });
};