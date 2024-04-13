from django.shortcuts import render


def view_bag(request):
    """View the shopping bag"""

    return render(request, 'bag/bag.html')
