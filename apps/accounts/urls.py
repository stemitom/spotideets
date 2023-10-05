from django.urls import path

from apps.accounts.views import CustomUserRetrieveUpdateAPIView

app_name = "accounts"

urlpatterns = [
    path(
        "profile/",
        CustomUserRetrieveUpdateAPIView.as_view(),
        name="profile",
    ),
]
