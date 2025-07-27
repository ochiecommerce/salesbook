from django.urls import include, path
from rest_framework.routers import DefaultRouter

from forum.api_views import MessageViewSet

router = DefaultRouter()
router.register(r'messages',MessageViewSet,basename='message')

urlpatterns = [
    path('',include(router.urls)),
]