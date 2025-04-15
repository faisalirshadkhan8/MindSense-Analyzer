from django.urls import path
from . import views

app_name = 'sentiment_analysis'  # Add this if not already present

urlpatterns = [
    path('', views.home, name='home'),
]
