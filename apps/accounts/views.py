from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.accounts.serializers import CustomUserRetrieveUpdateSerializer

from .models import CustomUser


class CustomUserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserRetrieveUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        serializer.save()
