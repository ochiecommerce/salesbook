from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_view import (
    ContactsViewSet,
    LabelViewSet,
    LabellingViewSet,
    PhonebookViewSet,
    ColumnViewSet,
    AttributeViewSet,
    NoteViewSet,
    ReadPermissionViewSet,
    WritePermissionViewSet,
    AlterPermissionViewSet,
)
from .views import UsernameCheckView, UserSearchView

router = DefaultRouter()
router.register(r"columns", ColumnViewSet, basename="column")
router.register(r"attributes", AttributeViewSet, basename="attribute")
router.register(r"phonebooks", PhonebookViewSet, basename="phonebook")
router.register(r"contacts", ContactsViewSet, basename="contact")
router.register(r"read_permissions", ReadPermissionViewSet, basename="read_permission")
router.register(
    r"write_permissions", WritePermissionViewSet, basename="write_permission"
)
router.register(r"labels", LabelViewSet, basename="label")
router.register(r"labellings", LabellingViewSet, basename="labelling")
router.register(
    r"alter_permissions", AlterPermissionViewSet, basename="alter_permission"
)
# router.register(r"notes", NoteViewSet, basename="note")

VIEWSET_ACTIONS = {"get": "list", "post": "create"}

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
    path("notes/", NoteViewSet.as_view(), name="create_note"),
]
