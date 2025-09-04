from django.core.management.base import BaseCommand
from dashboard.ml_model import AQIPredictor
import os

class Command(BaseCommand):
    help = 'Trains the AQI prediction model'

    def handle(self, *args, **options):
        self.stdout.write('Training AQI prediction model...')
        
        # Initialize predictor
        predictor = AQIPredictor()
        
        # Get path to data
        csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                               'data', 'test_environmental_data.csv')
        
        # Train model
        predictor.train(csv_path)
        
        self.stdout.write(self.style.SUCCESS('Model trained successfully!')) 