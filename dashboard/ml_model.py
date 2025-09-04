import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

class AQIPredictor:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_columns = ['temperature', 'humidity', 'co2_level', 'pm2_5', 'pm10', 'noise_level']
        
    def load_data(self, csv_path):
        """Load and preprocess the environmental data"""
        # Read CSV file
        df = pd.read_csv(csv_path)
        
        # Select only numeric columns for features
        X = df[self.feature_columns]
        y = df['air_quality_index']
        
        # Handle any missing values
        X = X.fillna(X.mean())
        
        # Scale the features
        X_scaled = self.scaler.fit_transform(X)
        
        return X_scaled, y
    
    def train(self, csv_path):
        """Train the Random Forest model"""
        X_scaled, y = self.load_data(csv_path)
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42
        )
        
        # Train the model
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        
        # Calculate and print model performance
        train_score = self.model.score(X_train, y_train)
        test_score = self.model.score(X_test, y_test)
        print(f"Training R² score: {train_score:.3f}")
        print(f"Testing R² score: {test_score:.3f}")
        
        # Save model
        model_dir = os.path.join(os.path.dirname(__file__), 'models')
        os.makedirs(model_dir, exist_ok=True)
        joblib.dump(self.model, os.path.join(model_dir, 'aqi_model.joblib'))
        joblib.dump(self.scaler, os.path.join(model_dir, 'aqi_scaler.joblib'))
        
        return train_score, test_score
    
    def predict(self, input_dict):
        """Predict AQI from input features"""
        if self.model is None:
            raise ValueError("Model not trained. Call train first.")
        
        print(f"Input dictionary: {input_dict}")  # Debug log
        
        # Convert input dictionary to array with correct column names
        input_array = np.array([[
            input_dict['temperature'],
            input_dict['humidity'],
            input_dict['co2_level'],
            input_dict['pm2_5'],
            input_dict['pm10'],
            input_dict['noise_level']
        ]])
        
        print(f"Input array: {input_array}")  # Debug log
        
        # Scale the input
        input_scaled = self.scaler.transform(input_array)
        print(f"Scaled input: {input_scaled}")  # Debug log
        
        # Make prediction
        predicted_aqi = self.model.predict(input_scaled)[0]
        print(f"Predicted AQI: {predicted_aqi}")  # Debug log
        
        return predicted_aqi
    
    def load(self, model_path, scaler_path):
        """Load a trained model and scaler"""
        print(f"Loading model from {model_path}")  # Debug log
        self.model = joblib.load(model_path)
        print(f"Loading scaler from {scaler_path}")  # Debug log
        self.scaler = joblib.load(scaler_path)
        print("Model and scaler loaded successfully")  # Debug log

# Initialize and train the model
def initialize_model():
    predictor = AQIPredictor()
    
    # Get the path to the CSV file
    csv_path = os.path.join(os.path.dirname(__file__), 'data', 'test_environmental_data.csv')
    model_path = os.path.join(os.path.dirname(__file__), 'models', 'aqi_model.joblib')
    scaler_path = os.path.join(os.path.dirname(__file__), 'models', 'aqi_scaler.joblib')
    
    # Create models directory if it doesn't exist
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    
    # Train and save the model
    predictor.train(csv_path)
    predictor.load(model_path, scaler_path)
    
    return predictor 