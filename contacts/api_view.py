from rest_framework import viewsets, permissions
from .serializers import ContactSerializer, Contact, InteractionLog, InteractionSerializer

class ContactsViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class InteractionViewSet(viewsets.ModelViewSet):
    queryset = InteractionLog.objects.all()
    serializer_class = InteractionSerializer
    permission_classes = [permissions.IsAuthenticated]