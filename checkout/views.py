from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm
import os
import env

def checkout(request):
    bag = request.session.get('bag', {})

    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': os.environ.get("STRIPE_PUBLIC_KEY"),
        'client_secret_key': os.environ.get("CLIENT_SECRET_KEY")
    }
    return render(request, template, context)
