# permissions.py
from rest_framework import permissions
from .models import Phonebook


class HasReadPermission(permissions.BasePermission):
    """
    Allows access if the user has read permission for the phonebook.
    """

    def has_object_permission(self, request, view, obj):
        # `obj` can be Phonebook or Contact (which has phonebook)
        phonebook = obj if isinstance(obj, Phonebook) else obj.phonebook
        return (
            phonebook.read_permissions.filter(user=request.user).exists()
            or phonebook.creator == request.user
        )


class HasWritePermission(permissions.BasePermission):
    """
    Allows creation/update only if user has write permission.
    """

    def has_object_permission(self, request, view, obj):
        phonebook = obj if isinstance(obj, Phonebook) else obj.phonebook
        return (
            phonebook.write_permissions.filter(user=request.user).exists()
            or phonebook.creator == request.user
        )


class HasAlterPermission(permissions.BasePermission):
    """
    Allows changing permissions only if user has alter permission.
    """

    def has_object_permission(self, request, view, obj):
        phonebook = obj if isinstance(obj, Phonebook) else obj.phonebook
        return (
            phonebook.alter_permissions.filter(user=request.user).exists()
            or phonebook.creator == request.user
        )


class HasAlterPermissionOrOwner(permissions.BasePermission):
    """
    Grants access if user is phonebook creator OR has an AlterPermission on that phonebook.
    """

    def has_permission(self, request, view):
        # Need phonebook_id in URL (for list/create)
        print("request args", view.kwargs)
        phonebook_id = view.kwargs.get("phonebook_id")
        if not phonebook_id:
            return False
        try:
            phonebook = Phonebook.objects.get(pk=phonebook_id)
        except Phonebook.DoesNotExist:
            return False

        return (
            phonebook.creator == request.user
            or phonebook.alter_permissions.filter(user=request.user).exists()
        )

    def has_object_permission(self, request, view, obj):
        # For retrieving/deleting individual permission objects
        phonebook = obj
        return (
            phonebook.creator == request.user
            or phonebook.alter_permissions.filter(user=request.user).exists()
        )
