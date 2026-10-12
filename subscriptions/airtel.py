import requests
from django.conf import settings


def get_airtel_access_token():
    url = f"{settings.AIRTEL_BASE_URL}/auth/oauth2/token"

    headers = {
        "Content-Type": "application/json",
        "Accept": "*/*",
    }

    payload = {
        "client_id": settings.AIRTEL_CLIENT_ID,
        "client_secret": settings.AIRTEL_CLIENT_SECRET,
        "grant_type": "client_credentials",
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=30,
    )

    try:
        data = response.json()
    except ValueError:
        data = {"raw_response": response.text}

    if not response.ok:
        raise Exception(
            f"Airtel authentication failed "
            f"(HTTP {response.status_code}): {data}"
        )

    token = data.get("access_token")

    if not token:
        raise Exception(
            f"Airtel did not return an access token: {data}"
        )

    return token