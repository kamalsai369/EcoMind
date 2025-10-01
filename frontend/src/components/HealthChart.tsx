import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';
import { useHealthDistribution } from '@/hooks/useAPI';
import { useLocationContext } from '@/hooks/useLocationContext';

export function HealthChart() {
  const { selectedLocation } = useLocationContext();
  const { data: healthDistribution, isLoading, error } = useHealthDistribution(selectedLocation);

  if (isLoading) {
    return (
      <div className="bg-white rounded-xl shadow-forest p-6 animate-slide-up">
        <h3 className="text-lg font-semibold text-foreground mb-4">Tree Health Distribution</h3>
        <div className="h-80 flex items-center justify-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
        </div>
      </div>
    );
  }

  if (error || !healthDistribution) {
    return (
      <div className="bg-white rounded-xl shadow-forest p-6 animate-slide-up">
        <h3 className="text-lg font-semibold text-foreground mb-4">Tree Health Distribution</h3>
        <div className="h-80 flex items-center justify-center">
          <p className="text-muted-foreground">Failed to load health data</p>
        </div>
      </div>
    );
  }

  const healthData = [
    { name: 'Healthy', value: healthDistribution.healthy_percentage, color: 'hsl(var(--success))' },
    { name: 'Moderate', value: healthDistribution.moderate_percentage, color: 'hsl(var(--warning))' },
    { name: 'Stressed', value: healthDistribution.stressed_percentage, color: '#fb8c00' },
    { name: 'Unhealthy', value: healthDistribution.unhealthy_percentage, color: 'hsl(var(--danger))' },
  ];
  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white p-3 rounded-lg shadow-forest border border-border">
          <p className="font-medium text-foreground">{data.name}</p>
          <p className="text-sm text-muted-foreground">{data.value}% of trees</p>
        </div>
      );
    }
    return null;
  };

  const CustomLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent }: any) => {
    const RADIAN = Math.PI / 180;
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
    const x = cx + radius * Math.cos(-midAngle * RADIAN);
    const y = cy + radius * Math.sin(-midAngle * RADIAN);

    return (
      <text 
        x={x} 
        y={y} 
        fill="white" 
        textAnchor={x > cx ? 'start' : 'end'} 
        dominantBaseline="central"
        className="text-sm font-medium"
      >
        {`${(percent * 100).toFixed(1)}%`}
      </text>
    );
  };

  return (
    <div className="bg-white rounded-xl shadow-forest p-6 animate-slide-up">
      <h3 className="text-lg font-semibold text-foreground mb-4">Tree Health Distribution</h3>
      
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={healthData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={CustomLabel}
              outerRadius={100}
              fill="#8884d8"
              dataKey="value"
              animationBegin={0}
              animationDuration={1200}
            >
              {healthData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip content={<CustomTooltip />} />
          </PieChart>
        </ResponsiveContainer>
      </div>

      <div className="grid grid-cols-2 gap-3 mt-4">
        {healthData.map((item, index) => (
          <div key={index} className="flex items-center gap-2">
            <div 
              className="w-3 h-3 rounded-full" 
              style={{ backgroundColor: item.color }}
            />
            <span className="text-sm text-muted-foreground">{item.name}</span>
            <span className="text-sm font-medium ml-auto">{item.value}%</span>
          </div>
        ))}
      </div>
    </div>
  );
}