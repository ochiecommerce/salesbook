# api_view.py
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404
from contacts.tagging import TagListener
from contacts.serializers import *

User = get_user_model()

from .permissions import (
    HasAlterPermission,
    HasAlterPermissionOrOwner,
    HasReadPermission,
    HasWritePermission,
)

note_tag_listener = TagListener("notes")


class PhonebookViewSet(viewsets.ModelViewSet):
    serializer_class = PhonebookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [permissions.IsAuthenticated(), HasAlterPermissionOrOwner()]
        return [permissions.IsAuthenticated(), HasReadPermission()]

    def get_queryset(self):
        return Phonebook.objects.filter(read_permissions__user=self.request.user).all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Customize the create process here
        phonebook = serializer.save(creator=request.user)
        read_permission = ReadPermission(user=request.user, phonebook=phonebook)
        read_permission.save()
        write_permission = WritePermission(user=request.user, phonebook=phonebook)
        write_permission.save()
        alter_permission = AlterPermission(user=request.user, phonebook=phonebook)
        alter_permission.save()

        return Response(serializer.data)


class ContactsViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [permissions.IsAuthenticated, HasReadPermission]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [permissions.IsAuthenticated(), HasWritePermission()]
        return [permissions.IsAuthenticated(), HasReadPermission()]

    def get_queryset(self):
        return Contact.objects.filter(
            phonebook__read_permissions__user=self.request.user
        ).all()

    def create(self, request, *args, **kwargs):
        contact_serializer = ContactSerializer(data=request.data)

        if contact_serializer.is_valid(raise_exception=True):
            phonebook_id = request.data.get("phonebook")
            phonebook = get_object_or_404(Phonebook, pk=phonebook_id)
            contact = contact_serializer.save(phonebook=phonebook)
            return Response(ContactSerializer(contact).data)

    def list(self, request):
        phonebook_id = request.data.get("phonebook")
        phonebook = get_object_or_404(Phonebook, pk=phonebook_id)
        contacts = self.get_queryset().filter(phonebook=phonebook)
        columns_serializer = ColumnSerializer(phonebook.columns.all(), many=True)
        data = {}
        data["columns"] = columns_serializer.data
        data["data"] = []
        for contact in contacts.all():
            contact_serializer = ContactSerializer(contact)
            attributes = Attribute.objects.filter(column__phonebook=contact.phonebook)
            row: dict = contact_serializer.data
            for attribute in attributes:
                row[attribute.column.name] = attribute.value
            data["data"].append(row)

        return Response(data)

    def retrieve(self, request, pk, *args, **kwargs):
        contact = Contact.objects.get(pk=pk)
        contact_serializer = ContactSerializer(contact)
        attributes = Attribute.objects.filter(column__phonebook=contact.phonebook)
        for attr in attributes:
            contact_serializer.data[attr.column.name] = attr.value  # type: ignore

        return Response(contact_serializer.data)


class ColumnViewSet(viewsets.ModelViewSet):
    queryset = Column.objects.all()
    serializer_class = ColumnSerializer
    permission_classes = [permissions.IsAuthenticated, HasAlterPermission]

    def get_queryset(self):
        return Column.objects.filter(
            phonebook__read_permissions__user=self.request.user
        ).all()

    def create(self, request, *args, **kwargs):
        column_serializer = ColumnSerializer(data=request.data)
        if column_serializer.is_valid(raise_exception=True):
            column = column_serializer.save()
            return Response(ColumnSerializer(column).data)


class NoteViewSet(viewsets.generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request: HttpRequest, *args, **kwargs):
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            note = serializer.save(user=request.user)
            return Response(NoteSerializer(note).data)


class ReminderViewSet(viewsets.ModelViewSet):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Reminder.objects.filter(creator=self.request.user).all()

    def create(self, request, *args, **kwargs):
        reminder_serializer = ReminderSerializer(data=request.data)
        reminder_serializer.is_valid(raise_exception=True)
        reminder = reminder_serializer.save(creator=request.user)
        return Response(ReminderSerializer(reminder).data)


class ReadPermissionViewSet(viewsets.ModelViewSet):
    queryset = ReadPermission.objects.all()
    serializer_class = ReadPermissionSerializer
    permission_classes = [permissions.IsAuthenticated, HasAlterPermissionOrOwner]

    def get_queryset(self):
        phonebook_id = self.kwargs.get("phonebook_id")
        return ReadPermission.objects.filter(phonebook__pk=phonebook_id)

    def perform_create(self, serializer):
        phonebook_id = self.kwargs.get("phonebook_id")
        user = User.objects.get(pk=self.request.data.get("user"))
        phonebook = get_object_or_404(Phonebook, pk=phonebook_id)
        self.check_object_permissions(
            self.request, phonebook
        )  # Ensure they can manage perms
        serializer.is_valid(raise_exception=True)
        serializer.save(phonebook=phonebook, user=user)


class WritePermissionViewSet(viewsets.ModelViewSet):
    queryset = WritePermission.objects.all()
    serializer_class = WritePermissionSerializer
    permission_classes = [permissions.IsAuthenticated, HasAlterPermissionOrOwner]

    def get_queryset(self):
        phonebook_id = self.kwargs.get("phonebook_id")
        return WritePermission.objects.filter(phonebook__pk=phonebook_id)

    def perform_create(self, serializer):
        phonebook_id = self.kwargs.get("phonebook_id")
        phonebook = get_object_or_404(Phonebook, pk=phonebook_id)
        self.check_object_permissions(self.request, phonebook)
        serializer.save(phonebook=phonebook)


class AlterPermissionViewSet(viewsets.ModelViewSet):
    queryset = AlterPermission.objects.all()
    serializer_class = AlterPermissionSerializer
    permission_classes = [permissions.IsAuthenticated, HasAlterPermissionOrOwner]

    def get_queryset(self):
        phonebook_id = self.kwargs.get("phonebook_id")
        return AlterPermission.objects.filter(phonebook__pk=phonebook_id)

    def perform_create(self, serializer):
        phonebook_id = self.kwargs.get("phonebook_id")
        phonebook = get_object_or_404(Phonebook, pk=phonebook_id)
        self.check_object_permissions(self.request, phonebook)
        serializer.save(phonebook=phonebook)


class AttributeViewSet(viewsets.ModelViewSet):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
    permission_classes = [permissions.IsAuthenticated]
