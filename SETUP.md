# Quick Setup Script for Dogecoin Price Prediction

This script automates the initial setup of the Dogecoin Price Prediction project.

## Prerequisites
- Python 3.8+
- pip

## Run Setup

### Windows:
```bash
setup.bat
```

### macOS/Linux:
```bash
chmod +x setup.sh
./setup.sh
```

## Manual Setup

If automated setup doesn't work, follow these steps:

1. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   ```

2. **Activate Virtual Environment**
   - Windows: `.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Train ML Model**
   ```bash
   python prediction/ml/train.py
   ```

5. **Run Django Server**
   ```bash
   python manage.py runserver
   ```

6. **Open Browser**
   Navigate to: `http://localhost:8000`

## Next Steps

- Check [README.md](README.md) for detailed documentation
- Explore the API at `/api/predict/`
- Experiment with different input values
- Review the source code for learning purposes
