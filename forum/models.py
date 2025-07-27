from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Message(models.Model):
    creator = models.ForeignKey(User,on_delete=models.CASCADE,related_name='messages')
    message = models.TextField()
    sent_on = models.DateTimeField(auto_now=True)
