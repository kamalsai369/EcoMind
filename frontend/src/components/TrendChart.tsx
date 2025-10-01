import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { useTrendData } from '@/hooks/useAPI';

export function TrendChart() {
  const { data: trendData, isLoading, error } = useTrendData();

  if (isLoading) {
    return (
      <div className="bg-white rounded-xl shadow-forest p-6 animate-slide-up" style={{ animationDelay: '0.2s' }}>
        <h3 className="text-lg font-semibold text-foreground mb-4">Weekly Trends</h3>
        <div className="h-80 flex items-center justify-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
        </div>
      </div>
    );
  }

  if (error || !trendData) {
    return (
      <div className="bg-white rounded-xl shadow-forest p-6 animate-slide-up" style={{ animationDelay: '0.2s' }}>
        <h3 className="text-lg font-semibold text-foreground mb-4">Weekly Trends</h3>
        <div className="h-80 flex items-center justify-center">
          <p className="text-muted-foreground">Failed to load trend data</p>
        </div>
      </div>
    );
  }

  // Transform the API data to chart format
  const chartData = trendData.weeks.map((week, index) => ({
    week,
    trees: trendData.tree_counts[index],
    carbon: trendData.carbon_capture[index],
  }));
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-4 rounded-lg shadow-forest border border-border">
          <p className="font-medium text-foreground mb-2">{label}</p>
          {payload.map((entry: any, index: number) => (
            <p key={index} className="text-sm" style={{ color: entry.color }}>
              {entry.name}: {entry.value.toLocaleString()}
              {entry.dataKey === 'trees' ? ' trees' : ' tons CO₂'}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="bg-white rounded-xl shadow-forest p-6 animate-slide-up" style={{ animationDelay: '0.2s' }}>
      <h3 className="text-lg font-semibold text-foreground mb-4">6-Month Trends</h3>
      
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
            <XAxis 
              dataKey="week" 
              stroke="hsl(var(--muted-foreground))"
              fontSize={12}
            />
            <YAxis 
              stroke="hsl(var(--muted-foreground))"
              fontSize={12}
            />
            <Tooltip content={<CustomTooltip />} />
            <Line 
              type="monotone" 
              dataKey="trees" 
              stroke="hsl(var(--primary))" 
              strokeWidth={3}
              dot={{ fill: 'hsl(var(--primary))', strokeWidth: 2, r: 4 }}
              name="Tree Count"
              animationDuration={1500}
            />
            <Line 
              type="monotone" 
              dataKey="health" 
              stroke="hsl(var(--success))" 
              strokeWidth={3}
              dot={{ fill: 'hsl(var(--success))', strokeWidth: 2, r: 4 }}
              name="Health Score"
              animationDuration={1500}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="flex items-center justify-center gap-6 mt-4">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-primary" />
          <span className="text-sm text-muted-foreground">Tree Count</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-success" />
          <span className="text-sm text-muted-foreground">Health Score</span>
        </div>
      </div>
    </div>
  );
}