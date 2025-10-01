import { ReactNode } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { LocationSelector } from '@/components/LocationSelector';
import { useLocationContext } from '@/hooks/useLocationContext';
import { cn } from '@/lib/utils';
import { 
  LayoutDashboard, 
  Heart, 
  Leaf, 
  TrendingUp, 
  Brain,
  TreePine,
  Satellite
} from 'lucide-react';

interface LayoutProps {
  children: ReactNode;
}

const navigation = [
  { name: 'Overview', href: '/', icon: LayoutDashboard },
  { name: 'Tree Health', href: '/health', icon: Heart },
  { name: 'Carbon Analytics', href: '/carbon', icon: Leaf },
  { name: 'Change Detection', href: '/changes', icon: TrendingUp },
  { name: 'AI Training', href: '/ai-training', icon: Brain },
];

export function Layout({ children }: LayoutProps) {
  const location = useLocation();
  const { selectedLocation, setSelectedLocation } = useLocationContext();

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-primary/5">
      {/* Header */}
      <header className="border-b border-border/50 bg-white/80 backdrop-blur-md sticky top-0 z-50">
        <div className="container mx-auto px-4 lg:px-8">
          <div className="flex h-16 items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-2">
                <div className="relative">
                  <TreePine className="h-8 w-8 text-primary" />
                  <Satellite className="h-4 w-4 text-primary-light absolute -top-1 -right-1" />
                </div>
                <div>
                  <h1 className="text-xl font-bold text-primary">EcoMind</h1>
                  <p className="text-xs text-muted-foreground -mt-1">Forest Intelligence</p>
                </div>
              </div>
            </div>

            <nav className="hidden md:flex items-center gap-1">
              {navigation.map((item) => {
                const isActive = location.pathname === item.href;
                const Icon = item.icon;
                
                return (
                  <Button
                    key={item.name}
                    variant={isActive ? "default" : "ghost"}
                    size="sm"
                    asChild
                    className={cn(
                      "transition-all duration-200",
                      isActive && "bg-primary text-primary-foreground shadow-forest"
                    )}
                  >
                    <Link to={item.href} className="flex items-center gap-2">
                      <Icon className="h-4 w-4" />
                      <span className="font-medium">{item.name}</span>
                    </Link>
                  </Button>
                );
              })}
            </nav>

            <div className="flex items-center gap-4">
              <LocationSelector
                selectedLocation={selectedLocation}
                onLocationChange={setSelectedLocation}
              />
              <div className="hidden lg:flex items-center gap-2 text-sm text-muted-foreground">
                <div className="w-2 h-2 bg-success rounded-full animate-pulse" />
                <span>Live Data</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Mobile Navigation */}
      <nav className="md:hidden border-b border-border/50 bg-white/90 backdrop-blur-md">
        <div className="container mx-auto px-4">
          <div className="flex items-center gap-1 py-2 overflow-x-auto">
            {navigation.map((item) => {
              const isActive = location.pathname === item.href;
              const Icon = item.icon;
              
              return (
                <Button
                  key={item.name}
                  variant={isActive ? "default" : "ghost"}
                  size="sm"
                  asChild
                  className={cn(
                    "flex-shrink-0 transition-all duration-200",
                    isActive && "bg-primary text-primary-foreground"
                  )}
                >
                  <Link to={item.href} className="flex items-center gap-2">
                    <Icon className="h-4 w-4" />
                    <span className="text-xs font-medium">{item.name}</span>
                  </Link>
                </Button>
              );
            })}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="flex-1">
        {children}
      </main>

      {/* Footer */}
      <footer className="border-t border-border/50 bg-white/80 backdrop-blur-md mt-16">
        <div className="container mx-auto px-4 lg:px-8 py-8">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="flex items-center gap-2">
              <TreePine className="h-5 w-5 text-primary" />
              <span className="text-sm text-muted-foreground">
                © 2024 EcoMind Forest Intelligence System
              </span>
            </div>
            <div className="flex items-center gap-4 text-sm text-muted-foreground">
              <span>Powered by AI & Satellite Data</span>
              <div className="flex items-center gap-1">
                <div className="w-1.5 h-1.5 bg-success rounded-full" />
                <span>Operational</span>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}