from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.accounts.models import CustomUser
from apps.accounts.serializers import CustomUserRetrieveUpdateSerializer, PrivacySettingsSerializer


class CustomUserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserRetrieveUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        serializer.save()


class PrivacySettingsRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = PrivacySettingsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.privacy_settings
