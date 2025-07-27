from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from core.viewsets import WithUserAsCreator
from market.models import Market, Product, Store
from market.serializers import MarketSerializer, ProductSerializer, StoreSerializer

class MarketViewSet(WithUserAsCreator):
    queryset = Market.objects.all()
    serializer_class = MarketSerializer

class StoreViewSet(WithUserAsCreator):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

class ProductViewSet(WithUserAsCreator):
    queryset= Product.objects.all()
    serializer_class = ProductSerializer
    # Enable filtering & searching
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['price']  # example: ?price=100
    search_fields = ['name', 'description']  # example: ?search=phone
    