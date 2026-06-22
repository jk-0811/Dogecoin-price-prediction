"""
URL configuration for doge_project.
"""
from django.urls import path, include

urlpatterns = [
    path('api/', include('prediction.urls')),
    path('', include('prediction.urls')),
]
