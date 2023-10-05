from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.accounts.serializers import CustomUserRetrieveUpdateSerializer

from .models import CustomUser


@method_decorator(login_required, name="dispatch")
class CustomUserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserRetrieveUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        serializer.save()
