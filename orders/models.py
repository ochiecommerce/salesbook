from django.db import models
from django.contrib.auth import get_user_model

from market.models import Product

Client = get_user_model()
class Order(models.Model):
    creator = models.ForeignKey(Client,on_delete=models.CASCADE)
    received = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='orders')
    quantity = models.IntegerField()
    order=models.ForeignKey(Order, on_delete=models.CASCADE,related_name='items')