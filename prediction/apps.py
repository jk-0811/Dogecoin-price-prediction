"""
Django App Configuration for Prediction
Loads ML model on startup
"""

from django.apps import AppConfig
import logging
import os

logger = logging.getLogger(__name__)

class PredictionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'prediction'
    
    def ready(self):
        """Initialize model when Django app is ready"""
        from django.conf import settings
        from prediction.ml.train import DogeMLModel
        from pathlib import Path
        
        try:
            # Initialize global model instance
            BASE_DIR = Path(settings.BASE_DIR)
            data_path = BASE_DIR / 'DOGE-USD.csv'
            model_path = BASE_DIR / 'prediction' / 'ml' / 'model.pkl'
            
            global_model = DogeMLModel(data_path, model_path)
            
            # Check if model exists, if not train it
            if model_path.exists():
                logger.info("Loading existing ML model...")
                global_model.load()
            else:
                logger.info("Model not found. Training new model...")
                if data_path.exists():
                    global_model.train()
                    global_model.save()
                    logger.info("Model trained and saved successfully")
                else:
                    logger.warning(f"Data file not found at {data_path}")
            
            # Store in Django cache or app instance
            self.ml_model = global_model
            
        except Exception as e:
            logger.error(f"Error loading ML model: {str(e)}")
            self.ml_model = None
