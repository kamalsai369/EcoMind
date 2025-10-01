# 🚀 EcoMind Vercel Deployment Guide

This guide will help you deploy the EcoMind Forest Monitoring System on Vercel with serverless functions.

## 📋 Prerequisites

- Vercel account ([Sign up here](https://vercel.com))
- GitHub repository with EcoMind code
- Node.js 16+ installed locally (for testing)

## 🔧 Deployment Steps

### 1. **Prepare Your Repository**

Ensure your repository has the following structure:
```
EcoMind/
├── api/                    # Serverless Python functions
│   ├── _utils.py          # Shared utilities
│   ├── locations.py       # /api/locations endpoint
│   ├── health.py          # /api/health endpoint
│   ├── trends.py          # /api/trends endpoint
│   ├── carbon.py          # /api/carbon endpoint
│   ├── changes.py         # /api/changes endpoint
│   └── training.py        # /api/training endpoint
├── frontend/              # React application
│   ├── src/
│   ├── package.json
│   └── dist/ (generated)
├── vercel.json            # Vercel configuration
├── package.json           # Root package.json
├── requirements.txt       # Python dependencies
└── README.md
```

### 2. **Connect to Vercel**

#### Option A: Vercel CLI (Recommended)
```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy from project root
vercel

# Follow the prompts:
# ? Set up and deploy "EcoMind"? [Y/n] y
# ? Which scope? [Your Account]
# ? Link to existing project? [y/N] n
# ? What's your project's name? ecomind-forest-monitoring
# ? In which directory is your code located? ./
```

#### Option B: Vercel Dashboard
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Import your GitHub repository
4. Configure project settings (see below)

### 3. **Project Configuration**

When setting up the project, configure these settings:

#### **Build & Development Settings:**
- **Framework Preset**: Other
- **Build Command**: `cd frontend && npm install && npm run build`
- **Output Directory**: `frontend/dist`
- **Install Command**: `cd frontend && npm install`
- **Development Command**: `cd frontend && npm run dev`

#### **Environment Variables:**
Add these environment variables in Vercel dashboard:
```
VITE_API_BASE_URL=https://your-app-name.vercel.app
```

### 4. **Domain Configuration**

After deployment, your app will be available at:
- **Production**: `https://your-app-name.vercel.app`
- **API Endpoints**: `https://your-app-name.vercel.app/api/*`

Example API endpoints:
- `https://your-app-name.vercel.app/api/locations`
- `https://your-app-name.vercel.app/api/health?location=Seattle`
- `https://your-app-name.vercel.app/api/trends?location=Seattle&days=30`

## 🔧 Configuration Files Explained

### **vercel.json**
```json
{
  "version": 2,
  "buildCommand": "cd frontend && npm install && npm run build",
  "outputDirectory": "frontend/dist",
  "installCommand": "cd frontend && npm install",
  "functions": {
    "api/*.py": {
      "runtime": "python3.9"
    }
  },
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/frontend/dist/$1"
    }
  ]
}
```

### **requirements.txt**
```
numpy==1.24.3
```

### **Frontend Environment Variables**
Create `frontend/.env.production`:
```env
VITE_API_BASE_URL=https://your-app-name.vercel.app
```

## 🚀 Deployment Process

### **Automatic Deployment:**
1. Push changes to your main branch
2. Vercel automatically builds and deploys
3. Visit your Vercel dashboard to monitor deployment

### **Manual Deployment:**
```bash
# From project root
vercel --prod
```

## 🧪 Testing Your Deployment

### **1. Test API Endpoints:**
```bash
# Test locations endpoint
curl https://your-app-name.vercel.app/api/locations

# Test health endpoint
curl https://your-app-name.vercel.app/api/health?location=Seattle

# Test trends endpoint
curl https://your-app-name.vercel.app/api/trends?location=Seattle&days=7
```

### **2. Test Frontend:**
Visit `https://your-app-name.vercel.app` and verify:
- ✅ Dashboard loads without errors
- ✅ Location selector works
- ✅ Charts display data
- ✅ Navigation between pages works
- ✅ Real-time data updates

## 🔧 Troubleshooting

### **Common Issues:**

#### **Build Failures:**
```bash
# Check build logs in Vercel dashboard
# Common fixes:
- Ensure frontend/package.json exists
- Check Node.js version compatibility
- Verify all dependencies are listed
```

#### **API Function Errors:**
```bash
# Check function logs in Vercel dashboard
# Common fixes:
- Verify Python syntax in api/*.py files
- Check imports in _utils.py
- Ensure requirements.txt includes all dependencies
```

#### **CORS Issues:**
```javascript
// Update frontend/.env.production
VITE_API_BASE_URL=https://your-app-name.vercel.app

// Verify vercel.json has CORS headers configured
```

#### **Environment Variables:**
```bash
# In Vercel dashboard, go to:
# Project Settings > Environment Variables
# Add: VITE_API_BASE_URL = https://your-app-name.vercel.app
```

### **Development vs Production:**

#### **Local Development:**
```bash
# Backend (if needed for testing)
python api_server.py  # Runs on localhost:8000

# Frontend
cd frontend
npm run dev          # Runs on localhost:8080
```

#### **Production:**
- Frontend: `https://your-app-name.vercel.app`
- API: `https://your-app-name.vercel.app/api/*`

## 📊 Performance Optimization

### **Frontend Optimization:**
- ✅ Vite build optimization enabled
- ✅ Code splitting for React components
- ✅ Environment-based API URLs
- ✅ Static asset optimization

### **API Optimization:**
- ✅ Serverless functions with cold start optimization
- ✅ Lightweight Python functions
- ✅ In-memory data generation (no database dependency)
- ✅ CORS headers for cross-origin requests

## 🔄 Continuous Deployment

### **Automatic Deployments:**
- Every push to `main` branch triggers deployment
- Pull requests create preview deployments
- Environment-specific builds (staging/production)

### **Deployment Monitoring:**
- View deployment status in Vercel dashboard
- Monitor function performance and errors
- Set up notifications for deployment failures

## 🌐 Custom Domain (Optional)

### **Add Custom Domain:**
1. Go to Project Settings > Domains
2. Add your custom domain
3. Configure DNS records as instructed
4. Update environment variables if needed

Example: `https://ecomind.yourdomain.com`

## 📈 Analytics & Monitoring

### **Vercel Analytics:**
- Real-time visitor analytics
- Performance metrics
- Function execution stats
- Error tracking

### **Custom Monitoring:**
```javascript
// Add to frontend for custom tracking
// Monitor API response times
// Track user interactions
// Log frontend errors
```

## 🔒 Security Considerations

### **Environment Variables:**
- ✅ API URLs configured via environment variables
- ✅ No sensitive data in code
- ✅ HTTPS enforced on all endpoints

### **CORS Configuration:**
- ✅ Properly configured CORS headers
- ✅ Restricted to necessary origins in production
- ✅ Secure API endpoint access

## 🎯 Next Steps After Deployment

1. **Test all functionality** on production URL
2. **Monitor performance** using Vercel analytics
3. **Set up custom domain** (optional)
4. **Configure monitoring alerts** for uptime
5. **Share your deployment** with stakeholders

---

## 🆘 Support

If you encounter issues:

1. **Check Vercel Dashboard** for build/runtime logs
2. **Review this guide** for configuration steps
3. **Test locally** to isolate deployment vs code issues
4. **Check GitHub Issues** for similar problems

**Your EcoMind application is now ready for the world! 🌲🚀**

### **Production URLs:**
- **App**: `https://your-app-name.vercel.app`
- **API**: `https://your-app-name.vercel.app/api/locations`
- **Dashboard**: [Vercel Dashboard](https://vercel.com/dashboard)