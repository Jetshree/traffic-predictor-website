from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Prediction(models.Model):
    CONGESTION_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    
    MODE_CHOICES = [
        ('Car', 'Car'),
        ('Metro', 'Metro'),
        ('Bike', 'Bike'),
        ('Walk', 'Walk'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    city = models.CharField(max_length=100)
    source = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    source_lat = models.FloatField()
    source_lon = models.FloatField()
    dest_lat = models.FloatField()
    dest_lon = models.FloatField()
    distance_km = models.FloatField()
    hour = models.IntegerField()
    weekday = models.IntegerField()
    day_type = models.CharField(max_length=50)
    weather = models.CharField(max_length=100)
    event_flag = models.BooleanField(default=False)
    route_type = models.CharField(max_length=50)
    congestion_level = models.CharField(max_length=10, choices=CONGESTION_CHOICES)
    suggested_mode = models.CharField(max_length=10, choices=MODE_CHOICES)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.city}: {self.source} → {self.destination} ({self.congestion_level})"


class SavedScenario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    source = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.city}"
