"""Views for Prediction app"""

import json
import logging
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.apps import apps
import numpy as np
from datetime import datetime

logger = logging.getLogger(__name__)

def get_ml_model():
    """Get the loaded ML model from app config"""
    try:
        prediction_app = apps.get_app_config('prediction')
        return prediction_app.ml_model
    except:
        return None


# ============ FRONTEND VIEWS ============

def dashboard(request):
    """Render main dashboard"""
    return render(request, 'prediction/dashboard.html')


# ============ API ENDPOINTS ============

@csrf_exempt
@require_http_methods(["POST"])
def predict_price(request):
    """
    POST endpoint for price prediction
    Expected JSON format:
    {
        "open": float,
        "high": float,
        "low": float,
        "volume": float,
        "ma5": float,
        "ma10": float,
        "daily_return": float,
        "volatility": float
    }
    """
    try:
        data = json.loads(request.body)
        
        # Get ML model
        ml_model = get_ml_model()
        
        if ml_model is None or ml_model.model is None:
            return JsonResponse({
                'success': False,
                'error': 'ML model not loaded or not trained'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Prepare features
        features_dict = {
            'Open': float(data.get('open', 0)),
            'High': float(data.get('high', 0)),
            'Low': float(data.get('low', 0)),
            'Volume': float(data.get('volume', 0)),
            'MA5': float(data.get('ma5', 0)),
            'MA10': float(data.get('ma10', 0)),
            'Daily_Return': float(data.get('daily_return', 0)),
            'Volatility': float(data.get('volatility', 0))
        }
        
        # Make prediction
        predicted_price = ml_model.predict(features_dict)
        
        # Ensure prediction is reasonable (DOGE price typically between 0 and 1)
        if predicted_price < 0:
            predicted_price = abs(predicted_price)
        
        return JsonResponse({
            'success': True,
            'predicted_price': float(predicted_price),
            'timestamp': datetime.now().isoformat(),
            'input_features': features_dict
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON format'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    except KeyError as e:
        return JsonResponse({
            'success': False,
            'error': f'Missing required field: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': f'Prediction failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ============ REST FRAMEWORK ENDPOINTS ============

@api_view(['POST'])
def api_predict(request):
    """
    DRF endpoint for prediction
    POST /api/predict/
    """
    try:
        data = request.data
        
        ml_model = get_ml_model()
        
        if ml_model is None or ml_model.model is None:
            return Response({
                'success': False,
                'error': 'ML model not loaded or not trained'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        features_dict = {
            'Open': float(data.get('open', 0)),
            'High': float(data.get('high', 0)),
            'Low': float(data.get('low', 0)),
            'Volume': float(data.get('volume', 0)),
            'MA5': float(data.get('ma5', 0)),
            'MA10': float(data.get('ma10', 0)),
            'Daily_Return': float(data.get('daily_return', 0)),
            'Volatility': float(data.get('volatility', 0))
        }
        
        predicted_price = ml_model.predict(features_dict)
        
        if predicted_price < 0:
            predicted_price = abs(predicted_price)
        
        return Response({
            'success': True,
            'predicted_price': float(predicted_price),
            'timestamp': datetime.now().isoformat(),
            'input_features': features_dict
        })
        
    except Exception as e:
        logger.error(f"API prediction error: {str(e)}")
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def api_model_info(request):
    """Get information about the trained model"""
    ml_model = get_ml_model()
    
    if ml_model is None or ml_model.model is None:
        return Response({
            'success': False,
            'error': 'Model not loaded'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({
        'success': True,
        'model_type': type(ml_model.model).__name__,
        'trained': ml_model.model is not None,
        'features': ['Open', 'High', 'Low', 'Volume', 'MA5', 'MA10', 'Daily_Return', 'Volatility']
    })
