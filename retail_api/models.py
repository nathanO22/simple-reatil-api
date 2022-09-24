from django.db import models
from retail_project import settings
# Create your models here.

class Inventory(models.Model):
    STATUS = (
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
    )

    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits = 15, decimal_places=2)
    quantity = models.DecimalField(max_digits = 15, decimal_places=2)
    description = models.TextField(blank=True)
    status = models.CharField(max_length = 255, choices=STATUS, default= 'available')

    class Meta:
        ordering = ['-name']

    def __str__(self):
        return self.name + '\n' + self.description




    
