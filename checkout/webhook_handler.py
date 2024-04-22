from django.http import HttpResponse


class StripeWebhookHandler:
    """Handle Stripe webhook events"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """Handle event response"""

        return HttpResponse(
            content=f'Webhook received: {event['type']}',
            status=200
        )