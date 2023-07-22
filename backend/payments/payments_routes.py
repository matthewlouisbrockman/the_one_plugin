"""
Contains the payments routes for hooking up Stripe

There's 3 major routes we need to worry about:
  - Checkout session completed - this links the user's customer Id to the checkout session
  - Invoice Paid - We got money wooo! (we should care about failed payments too but im durnk
  - Change to subscription - this is where we update the user's subscription status

Normally you would stick the dev and prod webhook on different APIs, but instead, since I'm doing both on the same,
I'll just make 2 webhooks that call different helpers.
"""
import os
import stripe

from models.subscriptions import TOPSubscription

from flask import Blueprint, jsonify, request

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY") # this is the secret key from stripe, see stripe developer
endpoint_secret = os.environ.get("STRIPE_ENDPOINT_SECRET") # this is for the webhook, see https://dashboard.stripe.com/webhooks/create

bp = Blueprint("payments", __name__, url_prefix="/payments")

@bp.route("/stripe_webhook", methods=["POST"])
def stripe_webhook():
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

    if event['type'] == 'checkout.session.completed':
        print("Checkout session completed")
        print(event)
        # get the customerid, subscriptionid, and client reference id
        customer_id = event['data']['object']['customer']
        subscription_id = event['data']['object']['subscription']
        client_reference_id = event['data']['object']['client_reference_id']

        # check if the subscription exists
        subscription = TOPSubscription.query.filter_by(subscription_id=subscription_id).first()
        if subscription:
            # update the subscription
            subscription.update(customer_id=customer_id)
        else:
            # create the subscription
            subscription = TOPSubscription(
                user_id=client_reference_id,
                subscription_provider="stripe",
                customer_id=customer_id,
                subscription_id=subscription_id,
            )
            subscription.save()

    if event['type'] == 'invoice.paid':
        print("Invoice paid")
        print(event)
        # get the subscription_id, plan, expires_at, cancel_at_period_end
        subscription_id = event['data']['object']['subscription']
        plan = event['data']['object']['lines']['data'][0]['plan']['id']
        expires_at = event['data']['object']['lines']['data'][0]['period']['end']
        cancel_at_period_end = event['data']['object']['lines']['data'][0]['plan']['cancel_at_period_end']
        customer_id = event['data']['object']['customer']

        # check if the subscription exists
        subscription = TOPSubscription.query.filter_by(subscription_id=subscription_id).first()
        if subscription:
            subscription.update(subscription_plan=plan, expires_at=expires_at, canceled_at=cancel_at_period_end)
        else:
            # create the subscription
            subscription = TOPSubscription(
                subscription_provider="stripe",
                subscription_id=subscription_id,
                customer_id=customer_id,
                subscription_plan=plan,
                expires_at=expires_at,
                canceled_at=cancel_at_period_end
            )
            subscription.save()

    # Handle the event
    print('Unhandled event type {}'.format(event['type']))

    return jsonify(success=True)