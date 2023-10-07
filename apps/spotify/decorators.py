from functools import wraps

from rest_framework.response import Response


def check_privacy_setting(setting_key):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, *args, **kwargs):
            param_user = self.user
            if self.request.user.is_authenticated and param_user == self.request.user:
                return view_func(self, *args, **kwargs)

            privacy_settings = param_user.privacy_settings
            if not getattr(privacy_settings, setting_key, True):
                return Response({"detail": "Access denied due to privacy settings."}, status=403)

            return view_func(self, *args, **kwargs)

        return _wrapped_view

    return decorator
