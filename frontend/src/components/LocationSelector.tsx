import { useState } from 'react';
import { MapPin, ChevronDown, Plus, Search } from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
  DropdownMenuSeparator,
} from '@/components/ui/dropdown-menu';
import { Input } from '@/components/ui/input';
import { useLocationList, type LocationInfo } from '@/hooks/useAPI';

interface LocationSelectorProps {
  selectedLocation: string;
  onLocationChange: (location: string) => void;
}

export function LocationSelector({ selectedLocation, onLocationChange }: LocationSelectorProps) {
  const { data: locations, isLoading, refetch } = useLocationList();
  const [searchTerm, setSearchTerm] = useState('');
  const [isOpen, setIsOpen] = useState(false);
  const [isAddingNew, setIsAddingNew] = useState(false);

  const filteredLocations = locations?.filter(location =>
    location.name.toLowerCase().includes(searchTerm.toLowerCase())
  ) || [];

  const handleLocationSelect = (location: string) => {
    onLocationChange(location);
    setIsOpen(false);
    setSearchTerm('');
    setIsAddingNew(false);
  };

  const handleAddNewLocation = async () => {
    if (searchTerm.trim().length < 2) return;
    
    try {
      const response = await fetch(`http://localhost:8000/api/locations/search?q=${encodeURIComponent(searchTerm.trim())}`);
      if (response.ok) {
        const data = await response.json();
        if (data.locations && data.locations.length > 0) {
          const newLocation = data.locations[0].location;
          await refetch(); // Refresh the location list
          handleLocationSelect(newLocation);
        }
      }
    } catch (error) {
      console.error('Error adding new location:', error);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && searchTerm.trim().length >= 2) {
      if (filteredLocations.length > 0) {
        handleLocationSelect(filteredLocations[0].name);
      } else {
        handleAddNewLocation();
      }
    }
  };

  const getDisplayName = (location: string) => {
    if (location === 'all') return 'All Locations';
    return location;
  };

  const showAddNewOption = searchTerm.trim().length >= 2 && 
    filteredLocations.length === 0 && 
    !isAddingNew;

  return (
    <div className="flex items-center gap-2">
      <MapPin className="h-4 w-4 text-muted-foreground" />
      <DropdownMenu open={isOpen} onOpenChange={setIsOpen}>
        <DropdownMenuTrigger asChild>
          <Button 
            variant="outline" 
            className="justify-between min-w-[200px]"
            disabled={isLoading}
          >
            <span className="truncate">
              {isLoading ? 'Loading...' : getDisplayName(selectedLocation)}
            </span>
            <ChevronDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent className="w-[300px] p-2">
          <div className="mb-2">
            <div className="relative">
              <Search className="absolute left-2 top-2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Type any city in India..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                onKeyPress={handleKeyPress}
                className="h-8 pl-8"
              />
            </div>
          </div>
          
          <DropdownMenuItem
            onClick={() => handleLocationSelect('all')}
            className={`cursor-pointer ${selectedLocation === 'all' ? 'bg-accent' : ''}`}
          >
            <div className="flex items-center justify-between w-full">
              <span className="font-medium">All Locations</span>
              <span className="text-sm text-muted-foreground">
                {locations?.reduce((total, loc) => total + loc.data_points, 0) || 0} records
              </span>
            </div>
          </DropdownMenuItem>
          
          {filteredLocations.length > 0 && <DropdownMenuSeparator />}
          
          <div className="max-h-[200px] overflow-y-auto">
            {filteredLocations.map((location) => (
              <DropdownMenuItem
                key={location.name}
                onClick={() => handleLocationSelect(location.name)}
                className={`cursor-pointer ${selectedLocation === location.name ? 'bg-accent' : ''}`}
              >
                <div className="flex items-center justify-between w-full">
                  <span className="truncate">{location.name}</span>
                  <span className="text-sm text-muted-foreground ml-2">
                    {location.data_points} records
                  </span>
                </div>
              </DropdownMenuItem>
            ))}
          </div>
          
          {showAddNewOption && (
            <>
              <DropdownMenuSeparator />
              <DropdownMenuItem
                onClick={handleAddNewLocation}
                className="cursor-pointer text-primary"
              >
                <div className="flex items-center gap-2 w-full">
                  <Plus className="h-4 w-4" />
                  <span>Add "{searchTerm.trim()}" to monitoring</span>
                </div>
              </DropdownMenuItem>
            </>
          )}
          
          {filteredLocations.length === 0 && searchTerm && !showAddNewOption && (
            <div className="p-2 text-sm text-muted-foreground text-center">
              Press Enter to add "{searchTerm.trim()}"
            </div>
          )}
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  );
}