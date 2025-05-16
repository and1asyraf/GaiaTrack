from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import EnvironmentalData
from .utils import get_simulated_data, get_thresholds
from .ml_model import AQIPredictor
from datetime import datetime
import os
import random

# Initialize the AQI predictor
predictor = AQIPredictor()
model_path = os.path.join(os.path.dirname(__file__), 'models', 'aqi_model.joblib')
scaler_path = os.path.join(os.path.dirname(__file__), 'models', 'aqi_scaler.joblib')

# Load the model if it exists
if os.path.exists(model_path) and os.path.exists(scaler_path):
    print(f"Loading model from {model_path}")
    predictor.load(model_path, scaler_path)
    print("Model loaded successfully")
else:
    print(f"Warning: Model files not found at {model_path} and {scaler_path}. Please train the model first.")

# Create your views here.

@login_required
def dashboard(request):
    """Render the dashboard with prediction form"""
    return render(request, 'prediction_input.html')

@login_required
def get_environmental_data(request):
    """Get real-time environmental data"""
    print("get_environmental_data view called")  # Debug log
    try:
        # Simulate environmental data
        data = {
            'temperature': round(random.uniform(20, 30), 1),
            'humidity': round(random.uniform(40, 60), 1),
            'co2_level': round(random.uniform(400, 800), 1),
            'air_quality': round(random.uniform(50, 100), 1),  # AQI range
            'noise_level': round(random.uniform(40, 80), 1),   # Noise level in dB
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        print(f"Generated data: {data}")  # Debug log
        
        # Save to database
        try:
            EnvironmentalData.objects.create(
                temperature=data['temperature'],
                humidity=data['humidity'],
                co2_level=data['co2_level'],
                air_quality=data['air_quality'],
                noise_level=data['noise_level']
            )
            print("Data saved to database successfully")  # Debug log
        except Exception as db_error:
            print(f"Database error: {str(db_error)}")  # Debug log
        
        print(f"Sending response: {data}")  # Debug log
        return JsonResponse(data)
    except Exception as e:
        print(f"Error in get_environmental_data: {str(e)}")  # Debug log
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def predict_aqi(request):
    """Predict AQI based on input parameters"""
    if request.method == 'POST':
        try:
            # Get input data and map to model's expected column names
            input_data = {
                'temperature': float(request.POST.get('temperature')),
                'humidity': float(request.POST.get('humidity')),
                'co2_level': float(request.POST.get('co2')),  # Map 'co2' to 'co2_level'
                'pm2_5': float(request.POST.get('pm2_5')),
                'pm10': float(request.POST.get('pm10')),
                'noise_level': float(request.POST.get('noise'))  # Map 'noise' to 'noise_level'
            }
            
            print(f"Input data: {input_data}")  # Debug log
            
            # Check if model is loaded
            if predictor.model is None:
                raise ValueError("Model not loaded. Please train the model first.")
            
            # Make prediction
            prediction = predictor.predict(input_data)
            print(f"Prediction result: {prediction}")  # Debug log
            
            return JsonResponse({
                'success': True,
                'prediction': prediction
            })
        except (ValueError, TypeError) as e:
            print(f"Prediction error: {str(e)}")  # Add logging
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    })
