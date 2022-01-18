from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticatedOrReadOnly, IsAdminUser


class IsProductOfCurrentUser(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method in SAFE_METHODS:
            return True

        return user == obj.user


class IsProductImageOfCurrentUser(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method in SAFE_METHODS:
            return True
            
        return user == obj.product.user

