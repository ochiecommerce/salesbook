from django.urls import include, path
from rest_framework.routers import DefaultRouter

from orders.api_views import OrderItemViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'orders',OrderViewSet,basename='order')
router.register(r'orderitems',OrderItemViewSet,basename='order_item')

urlpatterns = [
    path('',include(router.urls))
]