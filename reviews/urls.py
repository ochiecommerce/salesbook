from django.urls import include, path
from rest_framework.routers import DefaultRouter

from reviews.api_views import ReviewViewSet

router = DefaultRouter()
router.register(r'reviews',ReviewViewSet,basename='review')

urlpatterns = [
    path('',include(router.urls))
]