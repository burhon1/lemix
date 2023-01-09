from rest_framework.permissions import BasePermission

class ObjectLevelPermission(BasePermission):
    """
        Check user to create object.
        permission class needs: 
            - `model` in view class,
            - `object_level_permissions` in view class.
            - `request` for getting user  
            
    """

    def has_permission(self, request, view):
        if request.user.has_perm(view.object_level_permissions):
            return True
        
        return False