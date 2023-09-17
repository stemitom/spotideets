import base64

import requests
from decouple import config
from django.http import JsonResponse

SPOTIFY_CLIENT_ID = config("CLIENT_ID")
SPOTIFY_CLIENT_SECRET = config("CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = config("REDIRECT_URI")


def spotify_callback(request):
    auth_code = request.GET.get("code")

    token_url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f'Basic {base64.encode(SPOTIFY_CLIENT_ID + ":" + SPOTIFY_CLIENT_SECRET)}',
    }
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": SPOTIFY_REDIRECT_URI,
    }

    response = requests.post(token_url, headers=headers, data=data)

    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data["access_token"]
        # refresh_token = token_data["refresh_token"]
        return JsonResponse({"access_token": access_token})
    else:
        return JsonResponse({"error": "Failed to obtain access token"}, status=400)
