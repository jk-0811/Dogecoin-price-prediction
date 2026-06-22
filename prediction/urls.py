"""URL configuration for Prediction app"""

from django.urls import path
from prediction import views

app_name = 'prediction'

urlpatterns = [
    # Frontend
    path('', views.dashboard, name='dashboard'),
    
    # Traditional Django endpoints
    path('predict/', views.predict_price, name='predict_price'),
    
    # DRF API endpoints
    path('api/predict/', views.api_predict, name='api_predict'),
    path('api/model-info/', views.api_model_info, name='api_model_info'),
]
