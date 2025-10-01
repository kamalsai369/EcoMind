import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { MetricCard } from '@/components/MetricCard';
import { TrendingUp, TrendingDown, Calendar, AlertCircle } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart } from 'recharts';

const changeData = [
  { month: 'Jan 23', coverage: 172, health: 85, newTrees: 150, lostTrees: 23 },
  { month: 'Apr 23', coverage: 173, health: 86, newTrees: 180, lostTrees: 15 },
  { month: 'Jul 23', coverage: 174, health: 87, newTrees: 210, lostTrees: 18 },
  { month: 'Oct 23', coverage: 174.5, health: 88, newTrees: 165, lostTrees: 12 },
  { month: 'Jan 24', coverage: 175, health: 89, newTrees: 145, lostTrees: 8 },
  { month: 'Apr 24', coverage: 175.2, health: 89, newTrees: 120, lostTrees: 5 },
  { month: 'Jul 24', coverage: 175.3, health: 89, newTrees: 95, lostTrees: 7 },
  { month: 'Sep 24', coverage: 175.5, health: 89, newTrees: 110, lostTrees: 3 },
];

const ChangesPage = () => {
  return (
    <div className="container mx-auto px-4 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-foreground mb-2">Change Detection</h1>
        <p className="text-lg text-muted-foreground">
          Temporal analysis and forest evolution monitoring over time
        </p>
      </div>

      {/* Change Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <MetricCard
          title="18-Month Coverage Change"
          value="+3.5"
          unit="hectares"
          icon={<TrendingUp className="h-6 w-6" />}
          trend="up"
          variant="forest"
        />
        
        <MetricCard
          title="Net Tree Gain"
          value="+2,247"
          unit="trees"
          icon={<TrendingUp className="h-6 w-6" />}
          trend="up"
          variant="health"
        />
        
        <MetricCard
          title="Health Improvement"
          value="+4.7"
          unit="%"
          icon={<TrendingUp className="h-6 w-6" />}
          trend="up"
          variant="sage"
        />
        
        <MetricCard
          title="Tree Mortality Rate"
          value="0.02"
          unit="%"
          icon={<TrendingDown className="h-6 w-6" />}
          trend="down"
          variant="carbon"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        {/* Coverage Evolution */}
        <Card className="animate-slide-up">
          <CardHeader>
            <CardTitle>Forest Coverage Evolution</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={changeData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                  <XAxis dataKey="month" stroke="hsl(var(--muted-foreground))" fontSize={12} />
                  <YAxis stroke="hsl(var(--muted-foreground))" fontSize={12} />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: 'white', 
                      border: '1px solid hsl(var(--border))',
                      borderRadius: '8px',
                      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                    }}
                  />
                  <Area 
                    type="monotone" 
                    dataKey="coverage" 
                    stroke="hsl(var(--primary))" 
                    fill="hsl(var(--primary))"
                    fillOpacity={0.3}
                    strokeWidth={2}
                    name="Coverage (hectares)"
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        {/* Tree Dynamics */}
        <Card className="animate-slide-up" style={{ animationDelay: '0.1s' }}>
          <CardHeader>
            <CardTitle>Tree Population Dynamics</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={changeData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                  <XAxis dataKey="month" stroke="hsl(var(--muted-foreground))" fontSize={12} />
                  <YAxis stroke="hsl(var(--muted-foreground))" fontSize={12} />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: 'white', 
                      border: '1px solid hsl(var(--border))',
                      borderRadius: '8px',
                      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                    }}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="newTrees" 
                    stroke="hsl(var(--success))" 
                    strokeWidth={3}
                    dot={{ fill: 'hsl(var(--success))', strokeWidth: 2, r: 4 }}
                    name="New Trees"
                  />
                  <Line 
                    type="monotone" 
                    dataKey="lostTrees" 
                    stroke="hsl(var(--danger))" 
                    strokeWidth={3}
                    dot={{ fill: 'hsl(var(--danger))', strokeWidth: 2, r: 4 }}
                    name="Lost Trees"
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
            
            <div className="flex items-center justify-center gap-6 mt-4">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-success" />
                <span className="text-sm text-muted-foreground">New Trees</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-danger" />
                <span className="text-sm text-muted-foreground">Lost Trees</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Change Comparison */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <Card className="animate-slide-up" style={{ animationDelay: '0.2s' }}>
          <CardHeader>
            <CardTitle>2023 vs 2024 Comparison</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-6">
              <div className="flex justify-between items-center p-4 bg-success/10 rounded-lg">
                <div>
                  <p className="font-medium">Forest Coverage</p>
                  <p className="text-sm text-muted-foreground">Hectares</p>
                </div>
                <div className="text-right">
                  <p className="text-2xl font-bold text-success">+2.0%</p>
                  <p className="text-sm text-muted-foreground">173 → 175.5</p>
                </div>
              </div>

              <div className="flex justify-between items-center p-4 bg-success/10 rounded-lg">
                <div>
                  <p className="font-medium">Tree Count</p>
                  <p className="text-sm text-muted-foreground">Total trees</p>
                </div>
                <div className="text-right">
                  <p className="text-2xl font-bold text-success">+3.2%</p>
                  <p className="text-sm text-muted-foreground">68,253 → 70,500</p>
                </div>
              </div>

              <div className="flex justify-between items-center p-4 bg-success/10 rounded-lg">
                <div>
                  <p className="font-medium">Health Score</p>
                  <p className="text-sm text-muted-foreground">Overall health</p>
                </div>
                <div className="text-right">
                  <p className="text-2xl font-bold text-success">+2.3%</p>
                  <p className="text-sm text-muted-foreground">87% → 89%</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Change Alerts */}
        <Card className="animate-slide-up" style={{ animationDelay: '0.3s' }}>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertCircle className="h-5 w-5 text-info" />
              Recent Changes & Alerts
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-start gap-3 p-4 bg-success/10 border border-success/20 rounded-lg">
                <TrendingUp className="h-5 w-5 text-success mt-1 flex-shrink-0" />
                <div>
                  <h4 className="font-medium text-foreground">New Growth Detected</h4>
                  <p className="text-sm text-muted-foreground mt-1">
                    110 new saplings identified in recent satellite imagery from Sector D
                  </p>
                  <p className="text-xs text-success mt-2">3 days ago</p>
                </div>
              </div>
              
              <div className="flex items-start gap-3 p-4 bg-warning/10 border border-warning/20 rounded-lg">
                <Calendar className="h-5 w-5 text-warning mt-1 flex-shrink-0" />
                <div>
                  <h4 className="font-medium text-foreground">Canopy Thinning</h4>
                  <p className="text-sm text-muted-foreground mt-1">
                    Minor density reduction in Sector B, likely due to seasonal changes
                  </p>
                  <p className="text-xs text-warning mt-2">1 week ago</p>
                </div>
              </div>
              
              <div className="flex items-start gap-3 p-4 bg-info/10 border border-info/20 rounded-lg">
                <TrendingUp className="h-5 w-5 text-info mt-1 flex-shrink-0" />
                <div>
                  <h4 className="font-medium text-foreground">Recovery Progress</h4>
                  <p className="text-sm text-muted-foreground mt-1">
                    Trees in Sector A showing strong recovery after maintenance intervention
                  </p>
                  <p className="text-xs text-info mt-2">2 weeks ago</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default ChangesPage;