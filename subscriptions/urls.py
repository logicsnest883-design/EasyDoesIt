from django.urls import path

from .views import airtel_test


app_name = "subscriptions"


urlpatterns = [
    path(
        "airtel-test/",
        airtel_test,
        name="airtel_test",
    ),
]