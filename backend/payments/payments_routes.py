"""
Contains the payments routes for hooking up Stripe

There's 3 major routes we need to worry about:
  - Checkout session completed - this links the user's customer Id to the checkout session
  - Invoice Paid - We got money wooo! (we should care about failed payments too but im durnk
  - Change to subscription - this is where we update the user's subscription status

Normally you would stick the dev and prod webhook on different APIs, but instead, since I'm doing both on the same,
I'll just make 2 webhooks that call different helpers.
"""
from flask import Blueprint

bp = Blueprint("payments", __name__, url_prefix="/payments")

@bp.route("/recieve_webhook", methods=["POST"])
def recieve_webhook():
    return "We got the webhook!"

@bp.route("/dev_recieve_webhook", methods=["POST"])
def dev_recieve_webhook():
    return "We got the dev webhook!"