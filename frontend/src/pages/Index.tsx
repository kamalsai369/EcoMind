import { MetricCard } from '@/components/MetricCard';
import { HealthChart } from '@/components/HealthChart';
import { TrendChart } from '@/components/TrendChart';
import { TreePine, Users, Wind, Heart } from 'lucide-react';
import heroImage from '@/assets/hero-forest.jpg';
import { useOverviewMetrics } from '@/hooks/useAPI';
import { useLocationContext } from '@/hooks/useLocationContext';

const Index = () => {
  const { selectedLocation } = useLocationContext();
  const { data: metrics, isLoading, error } = useOverviewMetrics(selectedLocation);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-lg text-muted-foreground">Loading forest data...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-lg text-red-600 mb-4">Failed to load forest data</p>
          <p className="text-sm text-muted-foreground">Please ensure the API server is running</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative h-96 overflow-hidden">
        <div 
          className="absolute inset-0 bg-cover bg-center"
          style={{ backgroundImage: `url(${heroImage})` }}
        />
        <div className="absolute inset-0 bg-gradient-to-r from-primary/80 via-primary/60 to-transparent" />
        
        <div className="relative container mx-auto px-4 lg:px-8 h-full flex items-center">
          <div className="max-w-2xl text-white animate-fade-in-up">
            <h1 className="text-4xl md:text-6xl font-bold mb-4">
              Urban Forest Intelligence
            </h1>
            <p className="text-xl md:text-2xl mb-4 opacity-90">
              AI-powered satellite monitoring for sustainable urban forestry
            </p>
            {selectedLocation && selectedLocation !== 'all' && (
              <div className="mb-6 p-3 bg-white/20 backdrop-blur-sm rounded-lg border border-white/30">
                <p className="text-lg font-medium">
                  📍 Monitoring: <span className="text-yellow-200">{selectedLocation}</span>
                </p>
              </div>
            )}
            <div className="flex items-center gap-4 text-lg">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-success rounded-full animate-pulse" />
                <span>Real-time Monitoring</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-info rounded-full animate-pulse" />
                <span>AI Analysis Active</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Metrics Dashboard */}
      <section className="py-16">
        <div className="container mx-auto px-4 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-foreground mb-4">
              Forest Intelligence Overview
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Real-time insights into urban forest health, carbon impact, and environmental benefits
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
            <MetricCard
              title="Total Trees Monitored"
              value={metrics?.total_trees || 0}
              unit="trees"
              icon={<TreePine className="h-6 w-6" />}
              trend="up"
              variant="forest"
            />
            
            <MetricCard
              title="Forest Coverage"
              value={metrics?.forest_coverage_hectares || 0}
              unit="hectares"
              icon={<Users className="h-6 w-6" />}
              trend="stable"
              variant="sage"
            />
            
            <MetricCard
              title="Annual CO₂ Capture"
              value={metrics?.annual_co2_capture_tons?.toFixed(1) || "0"}
              unit="tons"
              icon={<Wind className="h-6 w-6" />}
              trend="up"
              variant="carbon"
            />
            
            <MetricCard
              title="Overall Health Score"
              value={metrics?.health_score_percentage?.toFixed(0) || "0"}
              unit="%"
              icon={<Heart className="h-6 w-6" />}
              trend="up"
              variant="health"
            />
          </div>

          {/* Charts Section */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <HealthChart />
            <TrendChart />
          </div>

          {/* Quick Stats */}
          <div className="mt-16 bg-white rounded-xl shadow-forest p-8">
            <h3 className="text-2xl font-bold text-foreground mb-8 text-center">
              Environmental Impact Summary
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="w-16 h-16 bg-gradient-forest rounded-full flex items-center justify-center mx-auto mb-4">
                  <TreePine className="h-8 w-8 text-white" />
                </div>
                <h4 className="text-lg font-semibold text-foreground mb-2">Carbon Sequestration</h4>
                <p className="text-3xl font-bold text-primary mb-1">{metrics?.annual_co2_capture_tons?.toFixed(1) || '0'}</p>
                <p className="text-sm text-muted-foreground">tons CO₂ annually</p>
              </div>
              
              <div className="text-center">
                <div className="w-16 h-16 bg-gradient-health rounded-full flex items-center justify-center mx-auto mb-4">
                  <Wind className="h-8 w-8 text-white" />
                </div>
                <h4 className="text-lg font-semibold text-foreground mb-2">Air Purification</h4>
                <p className="text-3xl font-bold text-success mb-1">{metrics?.annual_co2_capture_tons ? (metrics.annual_co2_capture_tons * 1.6).toFixed(0) : '0'}</p>
                <p className="text-sm text-muted-foreground">tons O₂ produced</p>
              </div>
              
              <div className="text-center">
                <div className="w-16 h-16 bg-gradient-carbon rounded-full flex items-center justify-center mx-auto mb-4">
                  <Users className="h-8 w-8 text-white" />
                </div>
                <h4 className="text-lg font-semibold text-foreground mb-2">Community Benefit</h4>
                <p className="text-3xl font-bold text-info mb-1">{metrics?.annual_co2_capture_tons ? Math.round(metrics.annual_co2_capture_tons * 0.22) : '0'}</p>
                <p className="text-sm text-muted-foreground">cars offset annually</p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Index;