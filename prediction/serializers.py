"""Serializers for Prediction API"""

from rest_framework import serializers
from prediction.models import PredictionHistory

class PredictionInputSerializer(serializers.Serializer):
    """Serializer for prediction input"""
    open = serializers.FloatField()
    high = serializers.FloatField()
    low = serializers.FloatField()
    volume = serializers.FloatField()
    ma5 = serializers.FloatField()
    ma10 = serializers.FloatField()
    daily_return = serializers.FloatField()
    volatility = serializers.FloatField()


class PredictionHistorySerializer(serializers.ModelSerializer):
    """Serializer for prediction history"""
    
    class Meta:
        model = PredictionHistory
        fields = ['id', 'timestamp', 'input_data', 'predicted_price', 'actual_price']
        read_only_fields = ['timestamp']
