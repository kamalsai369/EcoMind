import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { MetricCard } from '@/components/MetricCard';
import { Brain, Target, Eye, Zap } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const trainingData = [
  { epoch: 1, accuracy: 76.2, loss: 0.45, precision: 73.1, recall: 78.5 },
  { epoch: 2, accuracy: 81.5, loss: 0.38, precision: 78.9, recall: 84.2 },
  { epoch: 3, accuracy: 84.1, loss: 0.32, precision: 81.4, recall: 86.8 },
  { epoch: 4, accuracy: 86.3, loss: 0.28, precision: 83.7, recall: 89.1 },
  { epoch: 5, accuracy: 87.8, loss: 0.25, precision: 84.9, recall: 90.3 },
  { epoch: 6, accuracy: 88.5, loss: 0.23, precision: 85.5, recall: 91.2 },
  { epoch: 7, accuracy: 89.1, loss: 0.21, precision: 85.8, recall: 91.8 },
  { epoch: 8, accuracy: 89.4, loss: 0.20, precision: 85.5, recall: 92.1 },
  { epoch: 9, accuracy: 89.2, loss: 0.19, precision: 85.3, recall: 92.3 },
  { epoch: 10, accuracy: 89.0, loss: 0.18, precision: 85.5, recall: 92.4 },
];

const AITrainingPage = () => {
  return (
    <div className="container mx-auto px-4 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-foreground mb-2">AI Model Training</h1>
        <p className="text-lg text-muted-foreground">
          UNet deep learning model performance and training analytics
        </p>
      </div>

      {/* Model Performance Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <MetricCard
          title="Training Accuracy"
          value="89.0"
          unit="%"
          icon={<Brain className="h-6 w-6" />}
          trend="up"
          variant="forest"
        />
        
        <MetricCard
          title="Precision Score"
          value="85.5"
          unit="%"
          icon={<Target className="h-6 w-6" />}
          trend="stable"
          variant="health"
        />
        
        <MetricCard
          title="Recall Score"
          value="92.4"
          unit="%"
          icon={<Eye className="h-6 w-6" />}
          trend="up"
          variant="sage"
        />
        
        <MetricCard
          title="F1-Score"
          value="87.2"
          unit="%"
          icon={<Zap className="h-6 w-6" />}
          trend="up"
          variant="carbon"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        {/* Training Progress */}
        <Card className="animate-slide-up">
          <CardHeader>
            <CardTitle>Training Progress (10 Epochs)</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={trainingData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                  <XAxis dataKey="epoch" stroke="hsl(var(--muted-foreground))" fontSize={12} />
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
                    dataKey="accuracy" 
                    stroke="hsl(var(--primary))" 
                    strokeWidth={3}
                    dot={{ fill: 'hsl(var(--primary))', strokeWidth: 2, r: 4 }}
                    name="Accuracy (%)"
                  />
                  <Line 
                    type="monotone" 
                    dataKey="precision" 
                    stroke="hsl(var(--success))" 
                    strokeWidth={3}
                    dot={{ fill: 'hsl(var(--success))', strokeWidth: 2, r: 4 }}
                    name="Precision (%)"
                  />
                  <Line 
                    type="monotone" 
                    dataKey="recall" 
                    stroke="hsl(var(--info))" 
                    strokeWidth={3}
                    dot={{ fill: 'hsl(var(--info))', strokeWidth: 2, r: 4 }}
                    name="Recall (%)"
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        {/* Model Architecture */}
        <Card className="animate-slide-up" style={{ animationDelay: '0.1s' }}>
          <CardHeader>
            <CardTitle>UNet Model Architecture</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="text-center p-4 bg-primary/10 rounded-lg">
                <h4 className="font-medium text-primary mb-2">Input Layer</h4>
                <p className="text-sm text-muted-foreground">512 × 512 × 3 (RGB Satellite Image)</p>
              </div>
              
              <div className="text-center p-4 bg-success/10 rounded-lg">
                <h4 className="font-medium text-success mb-2">Encoder</h4>
                <p className="text-sm text-muted-foreground">4 Convolutional Blocks + MaxPooling</p>
              </div>
              
              <div className="text-center p-4 bg-info/10 rounded-lg">
                <h4 className="font-medium text-info mb-2">Bottleneck</h4>
                <p className="text-sm text-muted-foreground">Deep Feature Extraction</p>
              </div>
              
              <div className="text-center p-4 bg-warning/10 rounded-lg">
                <h4 className="font-medium text-warning mb-2">Decoder</h4>
                <p className="text-sm text-muted-foreground">4 Upsampling + Skip Connections</p>
              </div>
              
              <div className="text-center p-4 bg-danger/10 rounded-lg">
                <h4 className="font-medium text-danger mb-2">Output Layer</h4>
                <p className="text-sm text-muted-foreground">512 × 512 × 1 (Tree Segmentation Mask)</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Dataset Statistics */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <Card className="animate-slide-up" style={{ animationDelay: '0.2s' }}>
          <CardHeader>
            <CardTitle>Dataset Statistics</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-6">
              <div className="flex justify-between items-center">
                <span className="font-medium">Training Samples</span>
                <span className="text-2xl font-bold text-primary">11,080</span>
              </div>
              
              <div className="flex justify-between items-center">
                <span className="font-medium">Validation Samples</span>
                <span className="text-2xl font-bold text-success">2,704</span>
              </div>
              
              <div className="flex justify-between items-center">
                <span className="font-medium">Test Samples</span>
                <span className="text-2xl font-bold text-info">1,352</span>
              </div>
              
              <div className="pt-4 border-t border-border">
                <div className="flex justify-between items-center mb-2">
                  <span className="font-medium">Data Augmentation</span>
                  <span className="text-success font-medium">Enabled</span>
                </div>
                <p className="text-sm text-muted-foreground">
                  Rotation, flipping, scaling, and color adjustments applied
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Training Configuration */}
        <Card className="animate-slide-up" style={{ animationDelay: '0.3s' }}>
          <CardHeader>
            <CardTitle>Training Configuration</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="text-center p-3 bg-muted/50 rounded-lg">
                  <p className="text-sm text-muted-foreground">Batch Size</p>
                  <p className="text-lg font-bold">16</p>
                </div>
                <div className="text-center p-3 bg-muted/50 rounded-lg">
                  <p className="text-sm text-muted-foreground">Learning Rate</p>
                  <p className="text-lg font-bold">0.001</p>
                </div>
                <div className="text-center p-3 bg-muted/50 rounded-lg">
                  <p className="text-sm text-muted-foreground">Optimizer</p>
                  <p className="text-lg font-bold">Adam</p>
                </div>
                <div className="text-center p-3 bg-muted/50 rounded-lg">
                  <p className="text-sm text-muted-foreground">Loss Function</p>
                  <p className="text-lg font-bold">BCE + Dice</p>
                </div>
              </div>
              
              <div className="p-4 bg-success/10 rounded-lg">
                <h4 className="font-medium text-success mb-2">Model Status</h4>
                <p className="text-sm text-muted-foreground mb-3">
                  Training completed successfully. Model deployed for production inference.
                </p>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-success rounded-full animate-pulse" />
                  <span className="text-sm text-success">Active & Monitoring</span>
                </div>
              </div>
              
              <div className="p-4 bg-info/10 rounded-lg">
                <h4 className="font-medium text-info mb-2">IoU Score</h4>
                <p className="text-2xl font-bold text-info mb-1">82.7%</p>
                <p className="text-sm text-muted-foreground">
                  Intersection over Union for segmentation accuracy
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default AITrainingPage;