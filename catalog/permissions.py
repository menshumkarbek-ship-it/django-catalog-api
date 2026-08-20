from rest_framework.permissions import SAFE_METHODS, BasePermission

class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        owner = getattr(obj, "author", None)
        return request.user.is_staff or owner == request.user

class IsOwnerOrAdminForAll(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user and request.user.is_authenticated
