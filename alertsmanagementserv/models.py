from django.db import models
from django.contrib.auth.models import User

class Alert(models.Model):
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('deleted', 'Deleted'),
        ('triggered', 'Triggered'),
        # Add more statuses as needed


    ]

    user= models.ForeignKey(User, on_delete=models.CASCADE)
    cryptocurrency = models.CharField(max_length=10)
    target_price = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')