from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from checkout.webhook_handler import StripeWebhookHandler
from django.conf import settings
from django.http import JsonResponse, HttpResponse
import json
import stripe


@require_POST
@csrf_exempt
def webhook(request):
    """Listen for Stripe webhooks"""
    # Setup
    event = None
    payload = request.body
    wh_secret = ''
    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        event = json.loads(payload)
    except json.decoder.JSONDecodeError as e:
        print('⚠️  Webhook error while parsing basic request.' + str(e))

        return JsonResponse(data={"success": False})
    if wh_secret:
        # Only verify the event if there is an endpoint secret defined
        # Otherwise use the basic event deserialized with json
        sig_header = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, wh_secret
            )
        except stripe.error.SignatureVerificationError as e:
            print('⚠️  Webhook signature verification failed.' + str(e))
            return JsonResponse(data={"success": False}, status=400)
        except Exception as e:
            return HttpResponse(content=e, status=400)

    # Get object of handler and set up
    handler = StripeWebhookHandler(request)

    # Map webhook events to handler functions
    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
        'payment_intent.payment_failed': handler.handle_payment_intent_failed,
    }

    # Get type from stripe
    event_type = event['type']

    # If there's a handler, get it from even_map
    # Default handler if not
    event_handler = event_map.get(event_type, handler.handle_event)

    # Call the handler and return the handler's return value
    return event_handler(event)
