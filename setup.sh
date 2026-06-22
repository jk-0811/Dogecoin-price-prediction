#!/bin/bash

echo "============================================"
echo "Dogecoin Price Prediction - Setup Script"
echo "============================================"
echo ""

echo "Step 1: Creating virtual environment..."
python3 -m venv .venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi
echo "✓ Virtual environment created"

echo ""
echo "Step 2: Activating virtual environment..."
source .venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi
echo "✓ Virtual environment activated"

echo ""
echo "Step 3: Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo "✓ Dependencies installed"

echo ""
echo "Step 4: Training ML Model..."
python prediction/ml/train.py
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to train model"
    exit 1
fi
echo "✓ Model trained successfully"

echo ""
echo "============================================"
echo "Setup Complete!"
echo "============================================"
echo ""
echo "To start the server, run:"
echo "  python manage.py runserver"
echo ""
echo "Then open: http://localhost:8000"
echo ""
