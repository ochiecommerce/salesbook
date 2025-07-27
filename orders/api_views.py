from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from core.viewsets import WithUserAsCreator
from orders.serializers import *

class OrderViewSet(WithUserAsCreator):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemViewSet(ModelViewSet):
    querysetb=OrderItem.objects.all()
    serializer_class=OrderItemSerializer
    permission_classes=[IsAuthenticated]