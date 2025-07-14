from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Contact,
    Column,
    ReadPermission,
    WritePermission,
    AlterPermission,
    Note,
    Phonebook,
    Attribute,
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields =['id','username']

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ["name", "phone", "phonebook", "pk"]
        read_only_fields = ["created_at", "updated_at"]



class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = [
            "contact",
            "user",
        ]


class PhonebookSerializer(serializers.ModelSerializer):
    creator = UserSerializer()
    class Meta:
        model = Phonebook
        fields = ["name", "creator", "pk"]


class ReadPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadPermission
        fields = ["user", "phonebook"]


class WritePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WritePermission
        fields = ["user", "phonebook"]


class AlterPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlterPermission
        fields = ["user", "phonebook"]


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ["contact", "column", "value"]


class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields =['name','phonebook']
