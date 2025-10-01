import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { MetricCard } from '@/components/MetricCard';
import { HealthChart } from '@/components/HealthChart';
import { Heart, AlertTriangle, CheckCircle, XCircle } from 'lucide-react';
import { useHealthDistribution, useNDVIData } from '@/hooks/useAPI';
import { useLocationContext } from '@/hooks/useLocationContext';

const HealthPage = () => {
  const { selectedLocation } = useLocationContext();
  const { data: healthDistribution, isLoading: healthLoading, error: healthError } = useHealthDistribution(selectedLocation);
  const { data: ndviData, isLoading: ndviLoading, error: ndviError } = useNDVIData();

  if (healthLoading || ndviLoading) {
    return (
      <div className="container mx-auto px-4 lg:px-8 py-8">
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
            <p className="text-lg text-muted-foreground">Loading health data...</p>
          </div>
        </div>
      </div>
    );
  }

  if (healthError || ndviError || !healthDistribution || !ndviData) {
    return (
      <div className="container mx-auto px-4 lg:px-8 py-8">
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center">
            <p className="text-lg text-red-600 mb-4">Failed to load health data</p>
            <p className="text-sm text-muted-foreground">Please ensure the API server is running</p>
          </div>
        </div>
      </div>
    );
  }

  const healthMetrics = [
    { status: 'Healthy', count: healthDistribution.healthy, percentage: healthDistribution.healthy_percentage, color: 'health', icon: CheckCircle },
    { status: 'Moderate', count: healthDistribution.moderate, percentage: healthDistribution.moderate_percentage, color: 'sage', icon: AlertTriangle },
    { status: 'Stressed', count: healthDistribution.stressed, percentage: healthDistribution.stressed_percentage, color: 'carbon', icon: AlertTriangle },
    { status: 'Unhealthy', count: healthDistribution.unhealthy, percentage: healthDistribution.unhealthy_percentage, color: 'forest', icon: XCircle },
  ];

  return (
    <div className="container mx-auto px-4 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-foreground mb-2">Tree Health Monitor</h1>
        <p className="text-lg text-muted-foreground">
          Real-time health assessment using NDVI analysis and AI-powered monitoring
        </p>
      </div>

      {/* Health Overview Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {healthMetrics.map((metric) => {
          const Icon = metric.icon;
          return (
            <MetricCard
              key={metric.status}
              title={`${metric.status} Trees`}
              value={metric.count}
              unit={`(${metric.percentage.toFixed(1)}%)`}
              icon={<Icon className="h-6 w-6" />}
              variant={metric.color as 'health' | 'forest' | 'carbon' | 'sage'}
            />
          );
        })}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        {/* Health Distribution Chart */}
        <HealthChart />

        {/* NDVI Analysis */}
        <Card className="animate-slide-up" style={{ animationDelay: '0.1s' }}>
          <CardHeader>
            <CardTitle>NDVI Analysis</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex justify-between items-center p-4 bg-success/10 rounded-lg">
                <span className="font-medium">Current NDVI Average</span>
                <span className="text-2xl font-bold text-success">{ndviData.current_average.toFixed(2)}</span>
              </div>
              
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-sm">Healthy (0.6-1.0)</span>
                  <div className="flex items-center gap-2">
                    <div className="w-20 h-2 bg-gray-200 rounded-full overflow-hidden">
                      <div className="h-full bg-success rounded-full" style={{width: `${ndviData.healthy_percentage}%`}} />
                    </div>
                    <span className="text-sm font-medium">{ndviData.healthy_percentage.toFixed(1)}%</span>
                  </div>
                </div>
                
                <div className="flex justify-between items-center">
                  <span className="text-sm">Moderate (0.4-0.6)</span>
                  <div className="flex items-center gap-2">
                    <div className="w-20 h-2 bg-gray-200 rounded-full overflow-hidden">
                      <div className="h-full bg-warning rounded-full" style={{width: `${ndviData.moderate_percentage}%`}} />
                    </div>
                    <span className="text-sm font-medium">{ndviData.moderate_percentage.toFixed(1)}%</span>
                  </div>
                </div>
                
                <div className="flex justify-between items-center">
                  <span className="text-sm">Stressed (0.2-0.4)</span>
                  <div className="flex items-center gap-2">
                    <div className="w-20 h-2 bg-gray-200 rounded-full overflow-hidden">
                      <div className="h-full bg-orange-500 rounded-full" style={{width: `${ndviData.stressed_percentage}%`}} />
                    </div>
                    <span className="text-sm font-medium">{ndviData.stressed_percentage.toFixed(1)}%</span>
                  </div>
                </div>
                
                <div className="flex justify-between items-center">
                  <span className="text-sm">Unhealthy (&lt;0.2)</span>
                  <div className="flex items-center gap-2">
                    <div className="w-20 h-2 bg-gray-200 rounded-full overflow-hidden">
                      <div className="h-full bg-red-500 rounded-full" style={{width: `${ndviData.unhealthy_percentage}%`}} />
                    </div>
                    <span className="text-sm font-medium">{ndviData.unhealthy_percentage.toFixed(1)}%</span>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Health Alerts */}
      <Card className="animate-slide-up" style={{ animationDelay: '0.2s' }}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <AlertTriangle className="h-5 w-5 text-warning" />
            Health Alerts & Recommendations
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-start gap-3 p-4 bg-warning/10 border border-warning/20 rounded-lg">
              <AlertTriangle className="h-5 w-5 text-warning mt-1 flex-shrink-0" />
              <div>
                <h4 className="font-medium text-foreground">Drought Stress Detected</h4>
                <p className="text-sm text-muted-foreground mt-1">
                  12 trees in Sector C showing signs of water stress. Recommend increased irrigation.
                </p>
                <p className="text-xs text-warning mt-2">Priority: Medium</p>
              </div>
            </div>
            
            <div className="flex items-start gap-3 p-4 bg-success/10 border border-success/20 rounded-lg">
              <CheckCircle className="h-5 w-5 text-success mt-1 flex-shrink-0" />
              <div>
                <h4 className="font-medium text-foreground">Health Improvement</h4>
                <p className="text-sm text-muted-foreground mt-1">
                  Overall health score increased by 2.3% this month due to recent maintenance efforts.
                </p>
                <p className="text-xs text-success mt-2">Status: Positive Trend</p>
              </div>
            </div>
            
            <div className="flex items-start gap-3 p-4 bg-info/10 border border-info/20 rounded-lg">
              <Heart className="h-5 w-5 text-info mt-1 flex-shrink-0" />
              <div>
                <h4 className="font-medium text-foreground">Scheduled Maintenance</h4>
                <p className="text-sm text-muted-foreground mt-1">
                  Routine health assessment and pruning scheduled for next week in Sectors A & B.
                </p>
                <p className="text-xs text-info mt-2">Scheduled: Next Tuesday</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default HealthPage;