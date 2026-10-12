from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')










from django.shortcuts import render

def buy_me_coffee(request):
    return render(request, "core/buy_me_coffee.html")