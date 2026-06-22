# 🚀 Dogecoin Price Prediction with Machine Learning

A Django-based web application that uses Random Forest Regression to predict Dogecoin (DOGE-USD) prices based on historical data and technical indicators.

## 📋 Features

- **Machine Learning Model**: Random Forest Regressor trained on historical DOGE-USD data
- **Multiple Input Features**: Open, High, Low, Volume, MA5, MA10, Daily Return, Volatility
- **Web Dashboard**: Beautiful, responsive interface for making predictions
- **REST API**: JSON-based API endpoints for programmatic access
- **Real-time Predictions**: Get instant price predictions based on market data
- **Chart Visualizations**: View trends and predictions with interactive charts
- **Model Auto-loading**: Model loads automatically on server startup

## 🛠️ Project Setup

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Step 1: Create Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Train the ML Model

```bash
python prediction/ml/train.py
```

This will:
- Load the `DOGE-USD.csv` data
- Prepare features with technical indicators
- Train the Random Forest model
- Save the model to `prediction/ml/model.pkl`
- Display model performance metrics

**Expected Output:**
```
==================================================
MODEL PERFORMANCE
==================================================
Mean Squared Error (MSE): 0.000012
Root Mean Squared Error (RMSE): 0.003456
Mean Absolute Error (MAE): 0.002345
R² Score: 0.8567
==================================================
```

### Step 4: Run Django Server

```bash
python manage.py runserver
```

The application will be available at: `http://localhost:8000`

### Step 5: Access the Dashboard

Open your browser and navigate to:
- **Dashboard**: `http://localhost:8000/`
- **API Endpoint**: `http://localhost:8000/api/predict/`
- **Model Info**: `http://localhost:8000/api/model-info/`

## 📊 Project Architecture

```
doge_project/
├── doge_project/              # Django project settings
│   ├── settings.py            # Configuration
│   ├── urls.py                # URL routing
│   ├── asgi.py
│   └── wsgi.py
├── prediction/                # Main app
│   ├── ml/
│   │   ├── train.py          # ML model training
│   │   └── model.pkl         # Saved trained model
│   ├── static/
│   │   └── prediction/
│   │       ├── styles.css    # Dashboard styles
│   │       └── script.js     # Frontend logic
│   ├── templates/
│   │   └── prediction/
│   │       └── dashboard.html # Main UI
│   ├── views.py              # API views
│   ├── urls.py               # App routing
│   ├── models.py             # Database models
│   ├── apps.py               # App config (model loading)
│   └── serializers.py        # DRF serializers
├── DOGE-USD.csv              # Training dataset
├── manage.py
└── requirements.txt
```

## 🔌 API Endpoints

### 1. Predict Price (POST)

**Traditional Django Endpoint:**
```
POST /predict/
```

**DRF Endpoint:**
```
POST /api/predict/
```

**Request Body (JSON):**
```json
{
    "open": 0.15,
    "high": 0.16,
    "low": 0.14,
    "volume": 1250000000,
    "ma5": 0.152,
    "ma10": 0.151,
    "daily_return": 0.025,
    "volatility": 0.015
}
```

**Response:**
```json
{
    "success": true,
    "predicted_price": 0.1645,
    "timestamp": "2024-03-25T10:30:45.123456",
    "input_features": {
        "Open": 0.15,
        "High": 0.16,
        "Low": 0.14,
        "Volume": 1250000000,
        "MA5": 0.152,
        "MA10": 0.151,
        "Daily_Return": 0.025,
        "Volatility": 0.015
    }
}
```

### 2. Get Model Info (GET)

```
GET /api/model-info/
```

**Response:**
```json
{
    "success": true,
    "model_type": "RandomForestRegressor",
    "trained": true,
    "features": ["Open", "High", "Low", "Volume", "MA5", "MA10", "Daily_Return", "Volatility"]
}
```

## 🤖 Machine Learning Model Details

### Algorithm: Random Forest Regressor

**Configuration:**
- **Estimators**: 100 trees
- **Max Depth**: 15
- **Min Samples Split**: 5
- **Min Samples Leaf**: 2
- **Random State**: 42

### Training Data

The model is trained on historical Dogecoin price data from `DOGE-USD.csv` with the following columns:
- Date
- Open (opening price)
- High (highest price of the day)
- Low (lowest price of the day)
- Close (closing price)
- Adjusted Close
- Volume (trading volume)

### Feature Engineering

**Technical Indicators:**
1. **MA5**: 5-day moving average
2. **MA10**: 10-day moving average
3. **Daily Return**: Daily percentage change
4. **Volatility**: 10-day standard deviation

**Feature Normalization**: StandardScaler for feature scaling

### Model Performance

The model achieves strong predictive performance:
- **Train/Test Split**: 80/20
- **R² Score**: Measures variance explained (higher is better)
- **RMSE**: Root mean squared error in USD
- **MAE**: Mean absolute error in USD

## 🎨 Frontend Dashboard

The dashboard provides:

1. **Input Form**:
   - 8 input fields for market data
   - Real-time validation
   - Quick example buttons to load sample data

2. **Results Section**:
   - Displays predicted price
   - Shows all input features
   - Timestamp of prediction
   - Feature details grid

3. **Charts**:
   - Price trend analysis with Chart.js
   - Historical data with Plotly

4. **Responsive Design**:
   - Works on desktop and mobile
   - Dark theme optimized
   - Accessibility features

## 🔐 Security Considerations

⚠️ **Important**: This is a development/educational project.

For production deployment:
1. Change `SECRET_KEY` in `settings.py`
2. Set `DEBUG = False`
3. Configure `ALLOWED_HOSTS`
4. Use environment variables for sensitive data
5. Enable HTTPS
6. Set up proper CSRF token handling

## 📝 Usage Examples

### Using cURL

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

### Using Python

```python
import requests
import json

url = "http://localhost:8000/api/predict/"
data = {
    "open": 0.15,
    "high": 0.16,
    "low": 0.14,
    "volume": 1250000000,
    "ma5": 0.152,
    "ma10": 0.151,
    "daily_return": 0.025,
    "volatility": 0.015
}

response = requests.post(url, json=data)
result = response.json()

print(f"Predicted Price: ${result['predicted_price']:.6f}")
```

### Using JavaScript (Fetch API)

```javascript
fetch('/api/predict/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        open: 0.15,
        high: 0.16,
        low: 0.14,
        volume: 1250000000,
        ma5: 0.152,
        ma10: 0.151,
        daily_return: 0.025,
        volatility: 0.015
    })
})
.then(response => response.json())
.then(data => console.log(`Predicted: $${data.predicted_price.toFixed(6)}`));
```

## 🚀 Deployment

### Django Development Server

```bash
python manage.py runserver 0.0.0.0:8000
```

### Production with Gunicorn

```bash
pip install gunicorn
gunicorn doge_project.wsgi:application --bind 0.0.0.0:8000
```

### Docker Deployment

Example Dockerfile:
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "doge_project.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## 📦 Database

By default, the project uses SQLite. To use PostgreSQL:

1. Install: `pip install psycopg2-binary`
2. Update `DATABASES` in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'doge_db',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🐛 Troubleshooting

### Model Not Loading

```bash
# Retrain the model
python prediction/ml/train.py
```

### Port Already in Use

```bash
# Use a different port
python manage.py runserver 8001
```

### Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## 📚 Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [scikit-learn Documentation](https://scikit-learn.org/)
- [Plotly Documentation](https://plotly.com/python/)

## ⚠️ Disclaimer

This model is for **educational purposes only**. It should not be used for actual investment decisions. Cryptocurrency markets are highly volatile and unpredictable. Always conduct your own research and consult with financial advisors before making any investment decisions.

## 📄 License

This project is open source and available for educational use.

## ✨ Features to Add

- [ ] User authentication
- [ ] Prediction history database
- [ ] Real-time data integration with APIs
- [ ] Export predictions as CSV
- [ ] Advanced chart interactions
- [ ] Model retraining endpoint
- [ ] WebSocket for real-time updates
- [ ] Multiple model comparison

---

**Happy Predicting! 🚀 To The Moon! 🌙**
