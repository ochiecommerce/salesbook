from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_view import (
    ContactsViewSet,
    CustomContactView,
    PhonebookViewSet,
    ColumnViewSet,
    AttributeViewSet,
)

router = DefaultRouter()
router.register(r"columns", ColumnViewSet, basename="column")
router.register(r"attributes", AttributeViewSet, basename="attribute")
router.register(r'phonebooks',PhonebookViewSet,basename='phonebook')

VIEWSET_ACTIONS={
    "get":"list",
    "post":"create"
}

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
    path(
        "phonebooks/<int:phonebook_id>/contacts/",
        ContactsViewSet.as_view(VIEWSET_ACTIONS),
        name="custom_contacts",
    ),
]
