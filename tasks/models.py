from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1) 
    name = models.CharField(max_length=255, default='')
    description = models.TextField(default='')
    created_at = models.DateTimeField(default=timezone.now)



class StoreItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)