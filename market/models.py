from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Market(models.Model):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(User,on_delete=models.CASCADE)

class Store(models.Model):
    name = models.CharField(max_length=255)
    market = models.ForeignKey(Market,on_delete=models.CASCADE)
    creator = models.ForeignKey(User,on_delete=models.CASCADE)

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    creator = models.ForeignKey(User,on_delete=models.CASCADE,related_name='products')
    store = models.ForeignKey(Store,on_delete=models.CASCADE)

class Column(models.Model):
    name = models.CharField(max_length=255)
    market = models.ForeignKey(Market,on_delete=models.CASCADE)

class Attribute(models.Model):
    column = models.ForeignKey(Column,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)