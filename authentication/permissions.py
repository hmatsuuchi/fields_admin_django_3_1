from rest_framework import permissions

class isInStaffGroup(permissions.BasePermission):
    
    def has_permission(self, request, view):
        # checks if user is authenticated
        if not request.user.is_authenticated:
            print("Error: user not authenticated")
            return False
        # checks if user in in Staff group
        return request.user.groups.filter(name="Staff").exists()