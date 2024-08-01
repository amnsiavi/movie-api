from rest_framework.permissions import BasePermission, IsAuthenticated


class Admin(BasePermission):
    
    def has_permission(self, request, view):
        return request.user.is_staff and request.user.is_superuser and IsAuthenticated().has_permission(request,view)

class User(BasePermission):


    def has_permission(self, request, view):
        return not request.user.is_staff and not request.user.is_superuser and IsAuthenticated().has_permission(request,view)
    