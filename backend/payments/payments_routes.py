"""
Contains the payments routes for hooking up Stripe

There's 3 major routes we need to worry about:
  - Checkout session completed - this links the user's customer Id to the checkout session
  - Invoice Paid - We got money wooo! (we should care about failed payments too but im durnk
  - Change to subscription - this is where we update the user's subscription status

Normally you would stick the dev and prod webhook on different APIs, but instead, since I'm doing both on the same,
I'll just make 2 webhooks that call different helpers.
"""
import json
import os
import stripe

from flask import Blueprint, jsonify, request

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY") # this is the secret key from stripe, see stripe developer
endpoint_secret = os.environ.get("STRIPE_ENDPOINT_SECRET") # this is for the webhook, see https://dashboard.stripe.com/webhooks/create

bp = Blueprint("payments", __name__, url_prefix="/payments")

@bp.route("/webhook", methods=["POST"])
def webhook():
    event = None
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    # Handle the event
    print('Unhandled event type {}'.format(event['type']))

    return jsonify(success=True)