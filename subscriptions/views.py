from django.http import JsonResponse

from .airtel import get_airtel_access_token


def airtel_test(request):
    try:
        token = get_airtel_access_token()

        return JsonResponse({
            "success": True,
            "message": "Airtel authentication successful.",
            "token_received": bool(token),
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e),
        }, status=500)