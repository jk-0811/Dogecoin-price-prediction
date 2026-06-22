"""Models for Prediction app"""

from django.db import models

class PredictionHistory(models.Model):
    """Store prediction history for analytics"""
    timestamp = models.DateTimeField(auto_now_add=True)
    input_data = models.JSONField()
    predicted_price = models.FloatField()
    actual_price = models.FloatField(null=True, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"Prediction {self.timestamp}: ${self.predicted_price:.4f}"
