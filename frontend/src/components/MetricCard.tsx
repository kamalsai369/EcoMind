import { ReactNode } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { cn } from '@/lib/utils';

interface MetricCardProps {
  title: string;
  value: string | number;
  unit?: string;
  icon: ReactNode;
  trend?: 'up' | 'down' | 'stable';
  variant?: 'forest' | 'health' | 'carbon' | 'sage';
  className?: string;
}

export function MetricCard({ 
  title, 
  value, 
  unit, 
  icon, 
  trend, 
  variant = 'forest',
  className 
}: MetricCardProps) {
  const getVariantClasses = () => {
    switch (variant) {
      case 'health':
        return 'gradient-health text-white shadow-forest-lg';
      case 'carbon':
        return 'gradient-carbon text-white shadow-forest-lg';
      case 'sage':
        return 'gradient-sage text-primary shadow-forest';
      default:
        return 'gradient-forest text-white shadow-forest-lg';
    }
  };

  const getTrendIcon = () => {
    switch (trend) {
      case 'up':
        return '↗️';
      case 'down':
        return '↘️';
      default:
        return '→';
    }
  };

  return (
    <Card className={cn(
      'relative overflow-hidden transition-all duration-300 hover:scale-105 hover:shadow-forest-lg animate-fade-in-up',
      getVariantClasses(),
      className
    )}>
      <CardContent className="p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="p-3 bg-white/10 rounded-lg backdrop-blur-sm">
            {icon}
          </div>
          {trend && (
            <span className="text-lg opacity-80">
              {getTrendIcon()}
            </span>
          )}
        </div>
        
        <div className="space-y-1">
          <p className="text-sm opacity-90 font-medium">{title}</p>
          <div className="flex items-baseline gap-1">
            <span className="text-3xl font-bold animate-counter">
              {typeof value === 'number' ? value.toLocaleString() : value}
            </span>
            {unit && (
              <span className="text-lg opacity-80 font-medium">{unit}</span>
            )}
          </div>
        </div>

        {/* Decorative gradient overlay */}
        <div className="absolute top-0 right-0 w-20 h-20 bg-white/5 rounded-full -translate-y-10 translate-x-10" />
      </CardContent>
    </Card>
  );
}