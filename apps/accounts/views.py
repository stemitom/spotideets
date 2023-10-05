from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.accounts.serializers import CustomUserRetrieveUpdateSerializer, PrivacySettingsSerializer

from .models import CustomUser


class CustomUserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserRetrieveUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'privacy_settings': PrivacySettingsSerializer(self.request.user.privacy_settings).data})
        return context

    def perform_update(self, serializer):
        serializer.save()
