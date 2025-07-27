from django.db import models

from market.models import Product

# Create your models here.
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.FloatField()
    comment = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)