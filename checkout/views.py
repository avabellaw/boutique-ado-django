import os
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

import stripe

from .forms import OrderForm
from bag.contexts import bag_contents


def checkout(request):
    bag = request.session.get('bag', {})

    public_key = settings.STRIPE_PUBLIC_KEY
    secret_key = settings.STRIPE_SECRET_KEY

    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))

    current_bag = bag_contents(request)
    total = current_bag['grand_total']
    stripe_total = round(total * 100)
    stripe.api_key = secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY
    )

    order_form = OrderForm()

    if not public_key:
        messages.warning(request, 'Stripe public key missing. \
            Did you forget to set the enviroment variable?')
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': public_key,
        'client_secret_key': intent.client_secret
    }
    return render(request, template, context)
