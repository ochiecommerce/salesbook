from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Contact,
    Column,
    ReadPermission,
    Tag,
    WritePermission,
    AlterPermission,
    Note,
    Phonebook,
    Attribute,
    Reminder,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username"]


class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = ["due", "title"]

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['tagger_app','tagger_id','tagged_app','tagged_id']


class ContactSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True,required=False)

    class Meta:
        model = Contact
        fields = ["name", "phone", "phonebook", "pk", "tags"]
        read_only_fields = ["created_at", "updated_at"]


class NoteSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    contact = ContactSerializer(required=False)

    class Meta:
        model = Note
        fields = [
            "contact",
            "note",
            "user",
        ]


class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ["name", "phonebook"]


class PhonebookSerializer(serializers.ModelSerializer):
    creator = UserSerializer(required=False)
    contact_count = serializers.CharField(required=False)
    columns = ColumnSerializer(many=True, required=False)

    class Meta:
        model = Phonebook
        fields = ["name", "description", "creator", "pk", "contact_count", "columns"]


class ReadPermissionSerializer(serializers.ModelSerializer):
    phonebook = serializers.PrimaryKeyRelatedField(
        queryset=Phonebook.objects.all(), required=False
    )
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
