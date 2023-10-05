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

    def get_serializer_context(self):
        context = super().get_serializer_context()
        privacy_settings = self.request.user.privacy_settings
        context.update({'privacy_settings': PrivacySettingsSerializer(privacy_settings).data})
        return context

    def perform_update(self, serializer):
        serializer.save()
