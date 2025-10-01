import { useQuery } from '@tanstack/react-query';

const API_BASE_URL = 'http://localhost:8000';

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
  const url = location && location !== 'all' 
    ? `${API_BASE_URL}/api/metrics/overview?location=${encodeURIComponent(location)}`
    : `${API_BASE_URL}/api/metrics/overview`;
  
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error('Failed to fetch overview metrics');
  }
  return response.json();
};

const fetchHealthDistribution = async (location?: string): Promise<HealthDistribution> => {
  const url = location && location !== 'all'
    ? `${API_BASE_URL}/api/health/distribution?location=${encodeURIComponent(location)}`
    : `${API_BASE_URL}/api/health/distribution`;
    
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error('Failed to fetch health distribution');
  }
  return response.json();
};

const fetchLocationList = async (): Promise<LocationInfo[]> => {
  const response = await fetch(`${API_BASE_URL}/api/locations/list`);
  if (!response.ok) {
    throw new Error('Failed to fetch location list');
  }
  const data = await response.json();
  return data.locations;
};

const fetchCarbonData = async (): Promise<CarbonData> => {
  const response = await fetch(`${API_BASE_URL}/api/carbon/data`);
  if (!response.ok) {
    throw new Error('Failed to fetch carbon data');
  }
  return response.json();
};

const fetchNDVIData = async (): Promise<NDVIData> => {
  const response = await fetch(`${API_BASE_URL}/api/ndvi/analysis`);
  if (!response.ok) {
    throw new Error('Failed to fetch NDVI data');
  }
  return response.json();
};

const fetchTrendData = async (): Promise<TrendData> => {
  const response = await fetch(`${API_BASE_URL}/api/trends/weekly`);
  if (!response.ok) {
    throw new Error('Failed to fetch trend data');
  }
  return response.json();
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