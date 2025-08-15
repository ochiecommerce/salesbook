# serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Contact,
    Column,
    Label,
    Labelling,
    ReadPermission,
    Tag,
    WritePermission,
    AlterPermission,
    Note,
    Phonebook,
    Attribute,
    Reminder,
)

# utils.py
from django.contrib.auth.models import User


def get_phonebook_users(phonebook):
    users = set()

    # Add the creator
    if phonebook.creator:
        users.add(phonebook.creator)

    # Add permission holders
    for perm_model in (
        phonebook.read_permissions.all(),
        phonebook.write_permissions.all(),
        phonebook.alter_permissions.all(),
    ):
        for perm in perm_model:
            users.add(perm.user)

    return list(users)


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
        fields = ["tagger_app", "tagger_id", "tagged_app", "tagged_id"]


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["contact", "note", "user", "timestamp", "pk"]
        read_only_fields = ["pk"]


class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ["field", "phonebook", "type", "pk"]
        read_only_fields = ["pk"]


class ReadPermissionSerializer(serializers.ModelSerializer):
    phonebook = serializers.PrimaryKeyRelatedField(
        queryset=Phonebook.objects.all(), required=False
    )

    class Meta:
        model = ReadPermission
        fields = ["user", "phonebook"]


class LabelSerializer(serializers.ModelSerializer):
    creator = UserSerializer(required=False)

    class Meta:
        model = Label
        fields = [
            "phonebook",
            "color",
            "pk",
            "name",
            "creator",
        ]


class LabellingSerializer(serializers.ModelSerializer):
    creator = UserSerializer(required=False)
    notify = serializers.BooleanField(write_only=True, default=False)

    class Meta:
        model = Labelling
        fields = ["contact", "label", "creator", "notify"]

    def create(self, validated_data):
        notify = validated_data.pop("notify", False)  # remove before creating
        labelling = Labelling.objects.create(**validated_data)

        if notify:
            self.send_notifications(labelling)

        return labelling

    def send_notifications(self, labelling):
        from django.core.mail import send_mass_mail

        phonebook_users = get_phonebook_users(labelling.contact.phonebook)
        subject = f"[Phonebook] New Label Assigned"
        message = f"The contact {labelling.contact.phone} with the name {labelling.contact.name} has been labelled as '{labelling.label.name}'. Please consider this label while using the data of this contact'."
        datatuple = [
            (subject, message, None, [user.email])
            for user in phonebook_users
            if user.email
        ]
        send_mass_mail(datatuple, fail_silently=False)


class ContactSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    notes = NoteSerializer(many=True, required=False)
    labellings = LabellingSerializer(many=True, required=False)

    class Meta:
        model = Contact
        fields = ["name", "phone", "phonebook", "pk", "tags", "notes", "labellings"]
        read_only_fields = ["created_at", "updated_at"]


class PhonebookSerializer(serializers.ModelSerializer):
    creator = UserSerializer(required=False)
    contact_count = serializers.CharField(required=False)
    columns = ColumnSerializer(many=True, required=False)
    labels = LabelSerializer(many=True, required=False)
    read_permissions = ReadPermissionSerializer(many=True, required=False)

    class Meta:
        model = Phonebook
        fields = [
            "name",
            "description",
            "creator",
            "pk",
            "contact_count",
            "columns",
            "labels",
            "read_permissions",
        ]


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
