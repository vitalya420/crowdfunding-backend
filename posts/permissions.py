from rest_framework import permissions


class IsSubscriber(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_authenticated:
            return user.sub_info.filter(target_user=obj.target_user).exists()
        return False
