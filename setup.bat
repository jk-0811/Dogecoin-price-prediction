@echo off
echo ============================================
echo Dogecoin Price Prediction - Setup Script
echo ============================================
echo.

echo Step 1: Creating virtual environment...
python -m venv .venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment created

echo.
echo Step 2: Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment activated

echo.
echo Step 3: Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed

echo.
echo Step 4: Training ML Model...
python prediction\ml\train.py
if errorlevel 1 (
    echo ERROR: Failed to train model
    pause
    exit /b 1
)
echo ✓ Model trained successfully

echo.
echo ============================================
echo Setup Complete!
echo ============================================
echo.
echo To start the server, run:
echo   python manage.py runserver
echo.
echo Then open: http://localhost:8000
echo.
pause
