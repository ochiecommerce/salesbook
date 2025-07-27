from rest_framework import serializers

from contacts.serializers import UserSerializer
from forum.models import Message

class MessageSerializer(serializers.ModelSerializer):
    sent_on = serializers.DateTimeField(required=False)
    creator = UserSerializer(required=False)
    class Meta:
        model = Message
        fields = ['message','creator','sent_on']