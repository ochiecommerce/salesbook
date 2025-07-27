# cart/serializers.py
from rest_framework import serializers
from .models import Cart, CartItem
from market.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'subtotal']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total']
