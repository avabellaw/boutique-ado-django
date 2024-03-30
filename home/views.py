from django.shortcuts import render

# Create your views here.

def index(request):
    """View to show homepage"""
    return render(request, "home/index.html")