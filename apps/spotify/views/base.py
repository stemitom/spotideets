import requests
from django.shortcuts import get_object_or_404
from requests import Response
from rest_framework.views import APIView

from apps.accounts.models import CustomUser
from commons.enums import TimeFrame


class SpotifyAPIView(APIView):
    spotify_endpoint = None

    def dispatch(self, request, *args, **kwargs):
        self.user = get_object_or_404(CustomUser, spotify_user_id=kwargs.get("user_id"))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        access_token = self.user.spotifytoken.access_token
        headers = {"Authorization": f"Bearer {access_token}"}

        time_frame = self.get_time_frame(request)
        limit = self.get_limit(request)

        params = {"limit": limit, "time_range": time_frame.value}
        response = requests.get(self.spotify_endpoint, headers=headers, params=params)

        if response.status_code == 200:
            return self.handle_response(response, time_frame)
        else:
            return Response(
                {"error": f"Failed to retrieve data from {self.spotify_endpoint}"},
                status=response.status_code,
            )

    def get_time_frame(self, request):
        time_frame_map = {
            "weeks": TimeFrame.SHORT_TERM,
            "months": TimeFrame.MEDIUM_TERM,
            "lifetime": TimeFrame.LONG_TERM,
        }
        time_frame = time_frame_map.get(request.GET.get("range", "medium_term"), TimeFrame.MEDIUM_TERM)
        return time_frame

    def get_limit(self, request):
        try:
            return int(request.GET.get("limit", 20))
        except ValueError:
            return 10

    def handle_response(self, response, time_frame):
        raise NotImplementedError
