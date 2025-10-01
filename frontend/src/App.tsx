import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Layout } from "@/components/Layout";
import { LocationProvider } from "@/hooks/useLocationContext";
import Index from "./pages/Index";
import HealthPage from "./pages/Health";
import CarbonPage from "./pages/Carbon";
import ChangesPage from "./pages/Changes";
import AITrainingPage from "./pages/AITraining";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <LocationProvider>
      <TooltipProvider>
        <Toaster />
        <Sonner />
        <BrowserRouter>
          <Layout>
            <Routes>
              <Route path="/" element={<Index />} />
              <Route path="/health" element={<HealthPage />} />
              <Route path="/carbon" element={<CarbonPage />} />
              <Route path="/changes" element={<ChangesPage />} />
              <Route path="/ai-training" element={<AITrainingPage />} />
              <Route path="*" element={<NotFound />} />
            </Routes>
          </Layout>
        </BrowserRouter>
      </TooltipProvider>
    </LocationProvider>
  </QueryClientProvider>
);

export default App;
