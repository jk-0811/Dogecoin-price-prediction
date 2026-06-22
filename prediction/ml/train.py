"""
Machine Learning Model Training
Random Forest Regressor for Dogecoin Price Prediction
"""

import os
import pickle
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from pathlib import Path

class DogeMLModel:
    """Machine Learning Model for DOGE Price Prediction"""
    
    def __init__(self, data_path, model_path):
        self.data_path = data_path
        self.model_path = model_path
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = ['Open', 'High', 'Low', 'Volume']
        
    def prepare_data(self):
        """Load and prepare data for training"""
        df = pd.read_csv(self.data_path)
        
        # Handle missing values
        df = df.dropna()
        
        # Create features (lag features for time series)
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date').reset_index(drop=True)
        
        # Technical indicators
        df['MA5'] = df['Close'].rolling(window=5).mean()
        df['MA10'] = df['Close'].rolling(window=10).mean()
        df['Daily_Return'] = df['Close'].pct_change()
        df['Volatility'] = df['Close'].rolling(window=10).std()
        
        # Drop NaN values created by rolling calculations
        df = df.dropna()
        
        # Features: Using multiple price factors + technical indicators
        feature_cols = ['Open', 'High', 'Low', 'Volume', 'MA5', 'MA10', 'Daily_Return', 'Volatility']
        X = df[feature_cols].copy()
        y = df['Close'].copy()
        
        # Normalize features
        X_scaled = self.scaler.fit_transform(X)
        
        return X_scaled, y, df, feature_cols
    
    def train(self):
        """Train Random Forest Regressor"""
        print("Loading and preparing data...")
        X, y, df, feature_cols = self.prepare_data()
        
        # Split data (80/20)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        print(f"Training set size: {len(X_train)}")
        print(f"Test set size: {len(X_test)}")
        
        # Train Random Forest Regressor
        print("\nTraining Random Forest Regressor...")
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1,
            verbose=1
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print("\n" + "="*50)
        print("MODEL PERFORMANCE")
        print("="*50)
        print(f"Mean Squared Error (MSE): {mse:.6f}")
        print(f"Root Mean Squared Error (RMSE): {rmse:.6f}")
        print(f"Mean Absolute Error (MAE): {mae:.6f}")
        print(f"R² Score: {r2:.4f}")
        print("="*50)
        
        # Feature importance
        print("\nFeature Importance:")
        for feature, importance in zip(feature_cols, self.model.feature_importances_):
            print(f"  {feature}: {importance:.4f}")
        
        return self.model, rmse, r2
    
    def save(self):
        """Save model and scaler to disk"""
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        # Create directory if not exists
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save model
        with open(self.model_path, 'wb') as f:
            pickle.dump({'model': self.model, 'scaler': self.scaler}, f)
        
        print(f"\nModel saved to {self.model_path}")
    
    def load(self):
        """Load model from disk"""
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model not found at {self.model_path}")
        
        with open(self.model_path, 'rb') as f:
            data = pickle.load(f)
            self.model = data['model']
            self.scaler = data['scaler']
        
        print(f"Model loaded from {self.model_path}")
    
    def predict(self, features_dict):
        """
        Make prediction for new data
        features_dict: dict with keys ['Open', 'High', 'Low', 'Volume', 'MA5', 'MA10', 'Daily_Return', 'Volatility']
        """
        if self.model is None:
            raise ValueError("Model not loaded. Call load() first.")
        
        feature_cols = ['Open', 'High', 'Low', 'Volume', 'MA5', 'MA10', 'Daily_Return', 'Volatility']
        
        # Create feature array
        features = np.array([[features_dict.get(col, 0) for col in feature_cols]])
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Predict
        prediction = self.model.predict(features_scaled)[0]
        
        return prediction


if __name__ == "__main__":
    # Setup paths
    BASE_DIR = Path(__file__).resolve().parent.parent
    data_path = BASE_DIR / 'DOGE-USD.csv'
    model_path = BASE_DIR / 'prediction' / 'ml' / 'model.pkl'
    
    # Create and train model
    ml_model = DogeMLModel(data_path, model_path)
    ml_model.train()
    ml_model.save()
    
    print("\nModel training and saving complete!")
