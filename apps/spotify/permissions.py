from rest_framework.permissions import BasePermission


class PrivacySettingPermission(BasePermission):
    def __init__(self, setting_key):
        self.setting_key = setting_key

    def has_permission(self, request, view):
        param_user = view.user
        if request.user.is_authenticated and param_user == request.user:
            return True

        privacy_settings = param_user.privacy_settings
        if not getattr(privacy_settings, self.setting_key, True):
            return False

        return True
