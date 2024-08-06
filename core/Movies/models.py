from django.db import models
from django.core.validators import MaxValueValidator
from decimal import Decimal

# Create your models here.
class MoviesModel(models.Model):
    
    title = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=5, decimal_places=3, validators=[MaxValueValidator(Decimal('10.0'))])
    description = models.TextField()
    imageUrl = models.TextField(blank=True)
    movieUrl = models.URLField(blank=True)
    
    def __str__(self):
        return self.title
