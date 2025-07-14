from rest_framework import viewsets, permissions,views
from rest_framework.response import Response
from .serializers import *


class PhonebookViewSet(viewsets.ModelViewSet):
    serializer_class = PhonebookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Phonebook.objects.filter(read_permissions__user=self.request.user).all()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Customize the create process here
        phonebook = serializer.save()

        # Set any additional attributes on the model instance if needed
        # For example, let's set a custom field 'created_by' with request.user
        phonebook.creator = request.user
        phonebook.save()
        read_permission = ReadPermission(user=request.user,phonebook=phonebook)
        read_permission.save()
        write_permission = WritePermission(user=request.user,phonebook=phonebook)
        write_permission.save()
        alter_permission = AlterPermission(user=request.user,phonebook=phonebook)
        alter_permission.save()

        return Response(serializer.data)



class ContactsViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request,phonebook_id, *args, **kwargs):
        contact_serializer = ContactSerializer(data=request.POST)
        phonebook = Phonebook.objects.get(pk=phonebook_id)
        if contact_serializer.is_valid(raise_exception=True):
            contact=contact_serializer.save(phonebook=phonebook)
            return Response(ContactSerializer(contact).data)
        

    def list(self, request,phonebook_id):
        phonebook = Phonebook.objects.get(pk=phonebook_id)
        contacts = Contact.objects.filter(phonebook=phonebook)
        columns_serializer = ColumnSerializer(phonebook.columns.all(),many=True)
        data = {}
        data['columns']=columns_serializer.data
        data['data']=[]
        for contact in contacts.all():
            contact_serializer = ContactSerializer(contact)
            attributes = Attribute.objects.filter(column__phonebook=contact.phonebook)
            attributes_serializer = AttributeSerializer(attributes,many=True)
            row={}
            row['primary']=contact_serializer.data
            row['secondary']=attributes_serializer.data
            data['data'].append(row)

        return Response(data)

    def retrieve(self, request,pk, *args, **kwargs):
        contact = Contact.objects.get(pk=pk)
        attributes = Attribute.objects.filter(column__phonebook=contact.phonebook)
        attribute_serializer = AttributeSerializer(attributes)
        return Response(attribute_serializer.data)

class ColumnViewSet(viewsets.ModelViewSet):
    queryset=Column.objects.all()
    serializer_class=ColumnSerializer
    permission_classes=[permissions.IsAuthenticated]


class NoteViewSet(viewsets.ModelViewSet):
    queryset=Note
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]


class ReadPermissionViewSet(viewsets.ModelViewSet):
    queryset=ReadPermission
    serializer_class = ReadPermissionSerializer
    permission_classes = [permissions.IsAuthenticated]


class WritePermissionViewSet(viewsets.ModelViewSet):
    queryset = WritePermission
    serializer_class = WritePermissionSerializer
    permission_classes = [permissions.IsAuthenticated]


class AttributeViewSet(viewsets.ModelViewSet):
    queryset=Attribute
    serializer_class = AttributeSerializer
    permission_classes = [permissions.IsAuthenticated]

class CustomContactView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    


