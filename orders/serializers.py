from rest_framework import serializers

from contacts.serializers import UserSerializer
from orders.models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product','quantity','order']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True,required=False)
    creator = UserSerializer(required=False)
    class Meta:
        model = Order
        fields = ['id','creator','created_at','items']

