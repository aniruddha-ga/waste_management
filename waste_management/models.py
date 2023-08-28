# from django.contrib.auth.models import AbstractUser
from django.db import models

# class GuestUser(AbstractUser):
#     is_guest = models.BooleanField(default=True)
#     # Add any additional fields as needed
    

class DataEntry(models.Model):
    date = models.DateField()
    time = models.TimeField()
    kg = models.DecimalField(max_digits=5, decimal_places=2)
    hours_per_day = models.DecimalField(max_digits=5, decimal_places=2)
    waste_generated_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    population_count = models.IntegerField()

