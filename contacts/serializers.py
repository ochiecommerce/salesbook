from rest_framework import serializers
from .models import Contact, InteractionLog

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'client', 'properties', 'status', 'created_at', 'updated_at']
        read_only_fields = ['client', 'created_at', 'updated_at']


class InteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InteractionLog
        fields = ['contact','user',]