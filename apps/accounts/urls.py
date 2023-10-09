from django.urls import path

from apps.accounts.views import CustomUserRetrieveUpdateAPIView, PrivacySettingsRetrieveUpdateView

app_name = "accounts"

urlpatterns = [
    path(
        "profile/",
        CustomUserRetrieveUpdateAPIView.as_view(),
        name="profile",
    ),
    path(
        "privacy/",
        PrivacySettingsRetrieveUpdateView.as_view(),
        name="privacy",
    ),
]
