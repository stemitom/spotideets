import requests

from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import CustomUser
from commons.enums import TimeFrame


class SpotifyAPIView(APIView):
    spotify_endpoint = None

    def dispatch(self, request, *args, **kwargs):
        self.user_id = kwargs.get('user_id')  # noqa
        self.user = CustomUser.objects.filter(spotify_user_id=self.user_id).first()  # noqa
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        if not self.user:
            return Response({"error": f"User not found for id: {self.user_id}"}, status=404)
        access_token = self.user.spotifytoken.access_token

        time_frame = request.GET.get("time_frame", "medium_term")
        time_frame_map = {
            "weeks": TimeFrame.SHORT_TERM,
            "months": TimeFrame.MEDIUM_TERM,
            "lifetime": TimeFrame.LONG_TERM,
        }
        time_frame = time_frame_map.get(time_frame, TimeFrame.MEDIUM_TERM)

        try:
            limit = int(request.GET.get("limit", 20))
        except ValueError:
            limit = 10

        response = requests.get(
            self.spotify_endpoint,
            headers={"Authorization": f"Bearer {access_token}"},
            params={"limit": limit, "time_range": time_frame.value},
        )

        if response.status_code == 200:
            return self.handle_response(response, time_frame)

        return Response(
            {"error": f"Failed to retrieve data from {self.spotify_endpoint}"},
            status=response.status_code,
        )

    def handle_response(self, response, time_frame):
        raise NotImplementedError
