from core.viewsets import WithUserAsCreator
from forum.serializers import MessageSerializer, Message


class MessageViewSet(WithUserAsCreator):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    