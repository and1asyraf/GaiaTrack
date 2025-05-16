from django.db import models
from django.utils import timezone

class EnvironmentalData(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    air_quality = models.FloatField()
    co2_level = models.FloatField()
    temperature = models.FloatField()
    noise_level = models.FloatField()
    humidity = models.FloatField()
    particulate_matter = models.FloatField()
    location = models.CharField(max_length=100, default='Factory Floor A')
    sensor_id = models.CharField(max_length=50, default='ENV-SENSOR-001')
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"Environmental Data at {self.timestamp}"
