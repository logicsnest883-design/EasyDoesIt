from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("buy-me-a-coffee/", views.buy_me_coffee, name="buy_me_coffee"),
]