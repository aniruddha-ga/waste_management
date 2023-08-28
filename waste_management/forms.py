from django import forms
from .models import DataEntry
from django.db import models

class DataEntryForm(forms.ModelForm):
    date = models.DateField()
    time = models.TimeField()
    kg = models.DecimalField(max_digits=5, decimal_places=2)
    hours_per_day = models.DecimalField(max_digits=5, decimal_places=2)

    # waste_generated_percentage = kg / hours_per_day 

    population_count = models.IntegerField()
    class Meta:
        model = DataEntry  # Specify the model class
        fields = ['date', 'time', 'kg', 'hours_per_day', 'population_count']
# Date,Time,kg,Hours Per Day,Waste Generated,Population