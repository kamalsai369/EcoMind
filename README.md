# 🌲 EcoMind: Forest Health Monitoring System

An AI-powered forest monitoring platform that provides real-time forest health analytics, predictive modeling, and comprehensive environmental data visualization.

## 📋 Table of Contents
- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Running the Application](#-running-the-application)
- [Vercel Deployment](#-vercel-deployment)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [Usage Guide](#-usage-guide)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

- **Real-time Forest Health Monitoring** - Live tracking of forest health metrics
- **AI-Powered Predictions** - Machine learning models for health forecasting
- **Dynamic Location Management** - Scalable monitoring across multiple forest areas
- **Interactive Dashboards** - Rich data visualizations and analytics
- **Environmental Metrics** - Air quality, carbon sequestration, biodiversity tracking
- **Trend Analysis** - Historical data analysis and pattern recognition
- **Change Detection** - Automated anomaly detection and alert systems

## 🔧 Prerequisites

Before you begin, ensure you have the following installed on your system:

### Required Software:
- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 16+** - [Download Node.js](https://nodejs.org/)
- **npm or yarn** - Package manager (comes with Node.js)
- **Git** - [Download Git](https://git-scm.com/downloads)

### Verify Installation:
```bash
# Check Python version
python --version

# Check Node.js version
node --version

# Check npm version
npm --version

# Check Git version
git --version
```

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/kamalsai369/EcoMind.git
cd EcoMind
```

### 2. Backend Setup (Python/FastAPI)

#### Install Python Dependencies:
```bash
# Create a virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install required packages
pip install -r api_requirements.txt
```

#### Required Python Packages:
The `api_requirements.txt` includes:
- `fastapi` - Web framework for building APIs
- `uvicorn` - ASGI server implementation
- `sqlite3` - Database management (built into Python)
- `torch` - PyTorch for AI model
- `pandas` - Data manipulation and analysis
- `numpy` - Numerical computing
- `python-multipart` - Form data parsing
- `python-cors` - Cross-Origin Resource Sharing

### 3. Frontend Setup (React/TypeScript)

#### Navigate to Frontend Directory:
```bash
cd frontend
```

#### Install Node.js Dependencies:
```bash
# Using npm
npm install

# Or using yarn
yarn install
```

#### Frontend Dependencies Include:
- React 18+ with TypeScript
- Vite (build tool)
- Tailwind CSS (styling)
- Chart.js (data visualization)
- Axios (HTTP client)
- React Router (navigation)
- Shadcn/ui components

## 🏃‍♂️ Running the Application

### Method 1: Run Both Services Separately

#### 1. Start the Backend API Server:
```bash
# From the root directory (EcoMind/)
# Make sure virtual environment is activated
python api_server.py
```
**Backend will be available at:** `http://localhost:8000`

#### 2. Start the Frontend Development Server:
```bash
# Open a new terminal and navigate to frontend directory
cd frontend

# Start the frontend server
npm run dev
# Or with yarn:
yarn dev
```
**Frontend will be available at:** `http://localhost:8080`

### Method 2: Quick Start Script (Windows)

Create a batch file `start.bat` in the root directory:
```batch
@echo off
echo Starting EcoMind Forest Monitoring System...

echo.
echo Starting Backend API Server...
start cmd /k "venv\Scripts\activate && python api_server.py"

echo.
echo Waiting for backend to initialize...
timeout /t 3 /nobreak > nul

echo.
echo Starting Frontend Development Server...
start cmd /k "cd frontend && npm run dev"

echo.
echo EcoMind is starting up!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:8080
echo.
pause
```

### Method 3: Quick Start Script (macOS/Linux)

Create a shell script `start.sh` in the root directory:
```bash
#!/bin/bash
echo "Starting EcoMind Forest Monitoring System..."

echo ""
echo "Starting Backend API Server..."
source venv/bin/activate
python api_server.py &
BACKEND_PID=$!

echo ""
echo "Waiting for backend to initialize..."
sleep 3

echo ""
echo "Starting Frontend Development Server..."
cd frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "EcoMind is starting up!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:8080"
echo ""
echo "Press Ctrl+C to stop both services"

# Wait for user interrupt
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
```

## 🚀 Vercel Deployment

EcoMind is optimized for deployment on Vercel with serverless functions. 

### **Quick Deploy:**
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/kamalsai369/EcoMind)

### **Manual Deployment:**
1. **Install Vercel CLI:** `npm i -g vercel`
2. **Login:** `vercel login`
3. **Deploy:** `vercel` (from project root)
4. **Set Environment Variables:**
   - `VITE_API_BASE_URL=https://your-app-name.vercel.app`

### **What happens during deployment:**
- ✅ Frontend built with Vite and deployed as static site
- ✅ Python API functions deployed as Vercel serverless functions  
- ✅ Automatic CORS configuration for cross-origin requests
- ✅ Environment variables configured for production API URLs

**📖 For detailed deployment instructions, see [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md)**

**🌐 Live Demo:** [https://ecomind-forest-monitoring.vercel.app](https://your-app-name.vercel.app) *(Replace with your actual URL)*

## 📁 Project Structure
```

Make it executable:
```bash
chmod +x start.sh
./start.sh
```

## 📁 Project Structure

```
EcoMind/
├── README.md                          # Main documentation
├── PROJECT_OVERVIEW.md                # Comprehensive project documentation  
├── VERCEL_DEPLOYMENT.md               # Vercel deployment guide
├── vercel.json                        # Vercel configuration
├── package.json                       # Root package.json for deployment
├── requirements.txt                   # Python dependencies for Vercel
├── api_requirements.txt               # Python dependencies for local development
├── api_server.py                      # Local FastAPI server (for development)
├── forest_model.pth                   # Trained AI model
├── forest_monitoring.db               # SQLite database (local development)
├── training_history.json              # Model training metrics
├── utils.py                           # Utility functions
├── demo.py                            # Demo data generator
├── check_db.py                        # Database verification script  
├── test_*.py                          # Test files
├── api/                               # 🆕 Vercel Serverless Functions
│   ├── _utils.py                      # Shared utilities for API functions
│   ├── locations.py                   # GET /api/locations - List all locations
│   ├── health.py                      # GET /api/health - Health data by location
│   ├── trends.py                      # GET /api/trends - Trend analysis data
│   ├── carbon.py                      # GET /api/carbon - Carbon sequestration data
│   ├── changes.py                     # GET /api/changes - Change detection data
│   └── training.py                    # GET /api/training - AI model status
└── frontend/                          # React frontend application
    ├── .env.example                   # Environment variables template
    ├── .env.local                     # Local development environment
    ├── package.json                   # Node.js dependencies
    ├── vite.config.ts                 # Vite configuration
    ├── tailwind.config.ts             # Tailwind CSS configuration
    ├── index.html                     # Main HTML file
    ├── src/
    │   ├── App.tsx                    # Main React component
    │   ├── main.tsx                   # Application entry point
    │   ├── components/                # React components
    │   │   ├── HealthChart.tsx        # Health visualization
    │   │   ├── TrendChart.tsx         # Trend analysis
    │   │   ├── LocationSelector.tsx   # Location management
    │   │   └── ui/                    # UI components library
    │   ├── pages/                     # Application pages
    │   │   ├── Health.tsx             # Health monitoring page
    │   │   ├── Carbon.tsx             # Carbon tracking page
    │   │   ├── Changes.tsx            # Change detection page
    │   │   └── AITraining.tsx         # AI model insights
    │   ├── hooks/                     # Custom React hooks
    │   │   └── useAPI.ts              # 🔄 Updated for Vercel endpoints
    │   └── lib/                       # Utility libraries
    └── public/                        # Static assets
```

## 📚 API Documentation

### Base URL: `http://localhost:8000`

### Available Endpoints:

#### Health Monitoring
- `GET /health/{location}` - Get current health metrics for a location
- `GET /health` - Get health data for all locations

#### Location Management
- `GET /locations` - Get all monitored locations
- `POST /locations` - Add a new location (automatic via data generation)

#### Trend Analysis
- `GET /trends/{location}` - Get historical trend data for a location
- `GET /trends/{location}?days=30` - Get trends for specific time period

#### Environmental Metrics
- `GET /carbon/{location}` - Get carbon sequestration data
- `GET /air-quality/{location}` - Get air quality measurements
- `GET /biodiversity/{location}` - Get biodiversity index data

#### AI Model
- `GET /model/status` - Get AI model training status
- `GET /model/predictions/{location}` - Get future health predictions

#### System Information
- `GET /` - API welcome message and status
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation

### Example API Usage:
```javascript
// Get health data for Seattle
fetch('http://localhost:8000/health/Seattle')
  .then(response => response.json())
  .then(data => console.log(data));

// Get all locations
fetch('http://localhost:8000/locations')
  .then(response => response.json())
  .then(locations => console.log(locations));
```

## 📖 Usage Guide

### 1. First Time Setup
1. Follow the installation steps above
2. Start both backend and frontend servers
3. Open your browser to `http://localhost:8080`
4. The system will automatically generate sample forest data

### 2. Navigating the Dashboard
- **Health Page** - Monitor real-time forest health metrics
- **Carbon Page** - Track carbon sequestration and climate impact
- **Changes Page** - View detected anomalies and environmental changes
- **AI Training Page** - Explore model performance and predictions

### 3. Location Selection
- Use the location dropdown to switch between different forest areas
- Data is automatically loaded for the selected location
- New locations are dynamically added as data is generated

### 4. Data Interpretation
- **Health Score**: 0-100% (higher is better)
- **Air Quality Index**: 0-500 (lower is better)
- **Carbon Sequestration**: Tons CO2/hectare/year
- **Biodiversity Index**: 0-100% species diversity
- **Environmental Factors**: Temperature, humidity, rainfall, soil pH

### 5. Troubleshooting Common Issues

#### Backend Issues:
```bash
# If database errors occur
python check_db.py

# If model loading fails
python demo.py  # Regenerate demo data

# Check API status
curl http://localhost:8000/
```

#### Frontend Issues:
```bash
# Clear node modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Check for port conflicts
netstat -ano | findstr :8080  # Windows
lsof -ti:8080  # macOS/Linux
```

#### Port Conflicts:
If ports 8000 or 8080 are in use:

**Backend (api_server.py):**
```python
# Change port in api_server.py
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)  # Change to 8001
```

**Frontend (vite.config.ts):**
```typescript
// Change port in vite.config.ts
export default defineConfig({
  server: {
    port: 3000  // Change to 3000
  }
})
```

## 🧪 Testing

Run the included test suite:
```bash
# Test API endpoints
python test_api.py

# Test complete integration
python test_complete.py

# Test new city generation
python test_new_cities.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues:

1. **Check the Prerequisites** - Ensure all required software is installed
2. **Review the Logs** - Check terminal output for error messages
3. **Database Issues** - Run `python check_db.py` to verify database integrity
4. **Port Conflicts** - Try different ports if 8000/8080 are in use
5. **Create an Issue** - Report bugs on the GitHub repository

## 🎯 Next Steps

After getting the system running:
1. Explore the interactive dashboards
2. Check out the AI model predictions
3. Monitor forest health trends
4. Experiment with different locations
5. Review the comprehensive project documentation in `PROJECT_OVERVIEW.md`

---

**EcoMind** - Transforming forest monitoring through AI and data visualization 🌲🤖

**Repository**: https://github.com/kamalsai369/EcoMind  
**Documentation**: PROJECT_OVERVIEW.md  
**Demo**: Run locally following this guide