from rest_framework import permissions

class isInStaffGroup(permissions.BasePermission):
    def has_permission(self, request, view):
        # checks if user is authenticated
        if not request.user.is_authenticated:
            print("Error: user not in STAFF group - user not authenticated")
            return False
        # checks if user in in Staff group
        return request.user.groups.filter(name="Staff").exists()
    
class isInDisplaysGroup(permissions.BasePermission):
    def has_permission(self, request, view):
        # checks if user is authenticated
        if not request.user.is_authenticated:
            print("Error: user not in DISPLAYS group - user not authenticated")
            return False
        # checks if user in in Displays group
        return request.user.groups.filter(name="Displays").exists()