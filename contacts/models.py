from django.db import models
from django.contrib.auth.models import User

class Branch(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Contact(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('converted', 'Converted'),
        ('not_interested', 'Not Interested'),
    ]

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True)
    id_number = models.CharField(max_length=50)
    employment_number = models.CharField(max_length=50)
    employer_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    ability = models.FloatField(default=.0)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name} ({self.phone})"

class InteractionLog(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='interactions')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    notes = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Interaction with {self.contact.name} by {self.user.username}"
