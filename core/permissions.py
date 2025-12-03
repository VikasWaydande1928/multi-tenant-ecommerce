from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrStaffForWrite(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return getattr(request.user, 'role', None) in ['owner','staff'] and request.user.vendor == getattr(request, 'tenant', None)

class IsOwnerOnly(BasePermission):
    def has_permission(self, request, view):
        return getattr(request.user, 'role', None) == 'owner' and request.user.vendor == getattr(request, 'tenant', None)
