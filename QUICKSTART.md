# 🚀 QUICK START GUIDE - Dogecoin Price Prediction ML Project

## ⚡ 5-Minute Setup

### Step 1: Run Setup (Windows)
```bash
setup.bat
```

**What it does:**
- Creates Python virtual environment
- Installs all dependencies
- Trains the Random Forest ML model
- Saves the trained model

### Step 2: Activate Virtual Environment (After Setup)
```bash
.venv\Scripts\activate
```

### Step 3: Start Django Server
```bash
python manage.py runserver
```

### Step 4: Open Dashboard
Open your browser and go to: **http://localhost:8000**

---

## 📊 Project Structure

```
doge_project/
├── doge_project/              # Django Core
│   ├── settings.py            # ✓ Configured with REST_FRAMEWORK
│   ├── urls.py                # ✓ Routes to prediction app
│   ├── wsgi.py                # ✓ Production server
│   └── asgi.py                # ✓ Async server
│
├── prediction/                # Main Application
│   ├── ml/
│   │   ├── train.py           # ✓ ML Model Training
│   │   ├── model.pkl          # Generated after training
│   │   └── __init__.py
│   │
│   ├── static/
│   │   └── prediction/
│   │       ├── styles.css     # ✓ Dashboard Styling (Dark Theme)
│   │       └── script.js      # ✓ Frontend Logic (Charts, API)
│   │
│   ├── templates/
│   │   └── prediction/
│   │       └── dashboard.html # ✓ Main Interface
│   │
│   ├── views.py               # ✓ API Endpoints & Views
│   ├── urls.py                # ✓ Routing
│   ├── models.py              # ✓ Database Models
│   ├── apps.py                # ✓ App Config (Model Loading)
│   ├── serializers.py         # ✓ DRF Serializers
│   ├── admin.py               # ✓ Django Admin
│   └── __init__.py
│
├── DOGE-USD.csv               # Historical Data (Training Dataset)
├── manage.py                  # Django Management
├── requirements.txt           # Dependencies
├── README.md                  # Full Documentation
├── setup.bat                  # Windows Setup Script
├── setup.sh                   # Linux/macOS Setup Script
├── quickstart.py              # Python Setup Script
├── test_api.py                # API Testing Suite
├── .env.example               # Environment Variables Template
└── .gitignore                 # Git Ignore Rules
```

---

## 🔧 What Each Component Does

### prediction/ml/train.py
**Machine Learning Model**
- Algorithm: Random Forest Regressor (100 trees)
- Loads: DOGE-USD.csv historical data
- Creates: Technical indicators (MA5, MA10, volatility, daily returns)
- Normalizes: Features with StandardScaler
- Outputs: model.pkl with trained model

### prediction/views.py
**API Endpoints**
- `POST /predict/` - Classic Django endpoint
- `POST /api/predict/` - Django REST Framework
- `GET /api/model-info/` - Model information

### dashboard.html
**User Interface**
- Form with 8 input fields (price data + indicators)
- Real-time validation
- Results display with formatted price
- Interactive charts (Chart.js + Plotly)
- Responsive design (mobile-friendly)

### apps.py
**Auto-Loading Model**
- Loads model.pkl when Django starts
- Model available globally in views
- Handles errors gracefully

---

## 💻 API Usage Examples

### cURL Command
```bash
curl -X POST http://localhost:8000/api/predict/ \
  -H "Content-Type: application/json" \
  -d '{
    "open": 0.15,
    "high": 0.16,
    "low": 0.14,
    "volume": 1250000000,
    "ma5": 0.152,
    "ma10": 0.151,
    "daily_return": 0.025,
    "volatility": 0.015
  }'
```

### Python
```python
import requests

response = requests.post('http://localhost:8000/api/predict/', json={
    "open": 0.15,
    "high": 0.16,
    "low": 0.14,
    "volume": 1250000000,
    "ma5": 0.152,
    "ma10": 0.151,
    "daily_return": 0.025,
    "volatility": 0.015
})

print(f"Predicted: ${response.json()['predicted_price']:.6f}")
```

### JavaScript (Fetch)
```javascript
fetch('/api/predict/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    open: 0.15, high: 0.16, low: 0.14,
    volume: 1250000000, ma5: 0.152, ma10: 0.151,
    daily_return: 0.025, volatility: 0.015
  })
}).then(r => r.json()).then(d => console.log(`$${d.predicted_price}`));
```

---

## 📋 Input Fields Explanation

| Field | Type | Example | Description |
|-------|------|---------|-------------|
| Open | Float | 0.15 | Opening price in USD |
| High | Float | 0.16 | Highest price of the day |
| Low | Float | 0.14 | Lowest price of the day |
| Volume | Integer | 1250000000 | Total trading volume |
| MA5 | Float | 0.152 | 5-day moving average |
| MA10 | Float | 0.151 | 10-day moving average |
| Daily Return | Float | 0.025 | Daily change rate (0-1) |
| Volatility | Float | 0.015 | Price volatility (std dev) |

---

## 🧪 Testing the API

Run the automated test suite:
```bash
python test_api.py
```

This tests:
- ✓ Model info retrieval
- ✓ Bullish market prediction
- ✓ Bearish market prediction
- ✓ Volatile market prediction

---

## 🎨 Frontend Features

### Dashboard Components

1. **Input Form**
   - 8 fields for market data
   - Real-time validation
   - Clear & Submit buttons
   - Quick example loaders

2. **Results Panel**
   - Large prediction display
   - Feature comparison grid
   - Timestamp tracking
   - Confidence indicator

3. **Charts**
   - Chart.js line chart
   - Plotly historical data
   - Interactive tooltips

4. **Theme**
   - Dark background (#1a1a1a)
   - Gold accents (#ffd000)
   - Responsive grid layout
   - Mobile-optimized

---

## 🤖 ML Model Details

### Training Data
- **Source**: DOGE-USD.csv
- **Columns**: Date, Open, High, Low, Close, Volume
- **Period**: 2017-2026 (7+ years)

### Feature Engineering
1. **Raw Features**: Open, High, Low, Volume
2. **Moving Averages**: MA5, MA10
3. **Returns**: Daily percentage change
4. **Volatility**: 10-day standard deviation

### Model Configuration
```python
RandomForestRegressor(
    n_estimators=100,      # 100 trees
    max_depth=15,          # Tree depth
    min_samples_split=5,   # Minimum samples to split
    min_samples_leaf=2,    # Minimum samples in leaf
    random_state=42        # Reproducibility
)
```

### Train/Test Split
- Training: 80% of data
- Testing: 20% of data
- Random state ensures consistency

---

## ⚙️ Configuration

### Django Settings (settings.py)
- REST Framework enabled
- CSRF protection
- SQLite database (configurable)
- Static files serving
- Templates configured

### Environment Variables (.env)
```
DEBUG=True
SECRET_KEY=your-key
ALLOWED_HOSTS=127.0.0.1,localhost
```

---

## 🚨 Troubleshooting

### Problem: "Model not found"
**Solution**: Run model training again
```bash
python prediction/ml/train.py
```

### Problem: "Port 8000 already in use"
**Solution**: Use a different port
```bash
python manage.py runserver 8001
```

### Problem: "Module not found"
**Solution**: Reinstall dependencies
```bash
pip install -r requirements.txt --force-reinstall
```

### Problem: "CSRF token missing"
**Solution**: The frontend handles this automatically. If using custom requests, include:
```python
requests.post(url, json=data, cookies={'csrftoken': token})
```

---

## 📚 Documentation Index

- **[README.md](README.md)** - Full project documentation
- **[SETUP.md](SETUP.md)** - Detailed setup instructions
- **[.env.example](.env.example)** - Environment configuration template
- **[requirements.txt](requirements.txt)** - Python dependencies

---

## 🎯 Next Steps

1. ✅ Run setup.bat
2. ✅ Start Django server
3. ✅ Open dashboard
4. ✅ Make predictions
5. ✅ Test API endpoints
6. ✅ Review source code
7. ✅ Customize as needed

---

## 📞 Support

For issues or questions:
1. Check [README.md](README.md) troubleshooting section
2. Run `python test_api.py` for diagnostics
3. Review Django logs: `python manage.py runserver`

---

## ✨ Features Summary

✅ **ML Model**: Random Forest with 100 trees
✅ **API**: Django REST Framework endpoints
✅ **Dashboard**: Beautiful dark-themed UI
✅ **Charts**: Interactive visualizations
✅ **Auto-loading**: Model loads on startup
✅ **Responsive**: Works on desktop & mobile
✅ **Tested**: Includes test suite
✅ **Documented**: Complete documentation

---

## 🌟 Quick Commands Reference

```bash
# Initial Setup
setup.bat                           # Windows setup
chmod +x setup.sh && ./setup.sh    # Linux/macOS setup

# Activate Environment
.venv\Scripts\activate             # Windows
source .venv/bin/activate          # Linux/macOS

# Run Server
python manage.py runserver

# Train Model
python prediction/ml/train.py

# Test API
python test_api.py

# Access Dashboard
http://localhost:8000

# API Endpoint
POST http://localhost:8000/api/predict/
```

---

**Happy predicting! 🚀 To the moon! 🌙**

*Remember: This is an educational project. Never use ML predictions for real financial decisions without proper research!*
