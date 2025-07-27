from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_view import (
    ContactsViewSet,
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
# router.register(r"notes", NoteViewSet, basename="note")

VIEWSET_ACTIONS = {"get": "list", "post": "create"}

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("dj_rest_auth.urls")),
    # path("auth/jwt/",include('dj_rest_auth.jwt_urls')),
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
    path(
        "phonebooks/<int:phonebook_id>/contacts/",
        ContactsViewSet.as_view(VIEWSET_ACTIONS),
        name="custom_contacts",
    ),
    path(
        "phonebooks/<int:phonebook_id>/contacts/<int:pk>",
        ContactsViewSet.as_view({"get": "retrieve"}),
        name="contact_detils",
    ),
    path(
        "phonebooks/<int:phonebook_id>/read_permissions/",
        ReadPermissionViewSet.as_view({"post": "create", "get": "list"}),
        name="read_permission",
    ),
    path(
        "phonebooks/<int:phonebook_id>/write_permissions/",
        WritePermissionViewSet.as_view({"post": "create", "get": "list"}),
        name="write_permission",
    ),
    path(
        "phonebooks/<int:phonebook_id>/alter_permissions/",
        AlterPermissionViewSet.as_view({"post": "create", "get": "list"}),
        name="alter_permission",
    ),
    path('notes/',NoteViewSet.as_view(),name='create_note'),
    
]
