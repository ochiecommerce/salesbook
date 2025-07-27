from django.urls import include, path
from rest_framework.routers import DefaultRouter

from market.api_views import MarketViewSet, ProductViewSet, StoreViewSet

router = DefaultRouter()

router.register(r'markets',MarketViewSet,basename='market')
router.register(r'stores',StoreViewSet,basename='store')
router.register(r'products',ProductViewSet, basename='product')

urlpatterns = [
    path('',include(router.urls))
]