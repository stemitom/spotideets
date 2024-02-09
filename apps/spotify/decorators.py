from rest_framework.response import Response

from apps.accounts.models import CustomUser


def check_privacy_settings(permission):
    """
    Permission decorator to add access check on endpoints for specific resources e.g (top tracks, top artists)
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            user_id = kwargs.get("user_id")
            user = CustomUser.objects.get(spotify_user_id=user_id)
            privacy_settings = user.privacy_settings

            if request.user and request.user.id == user_id:
                return view_func(request, *args, **kwargs)

            if not getattr(privacy_settings, permission):
                return Response({"detail": "Access denied due to privacy settings."}, status=403)

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
