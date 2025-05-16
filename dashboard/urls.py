from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api/environmental-data/', views.get_environmental_data, name='environmental_data'),
    path('api/predict-aqi/', views.predict_aqi, name='predict_aqi'),
] 