import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY


def create_stripe_product(name, description):
    print(name, description)
    stripe_product = stripe.Product.create(name=name, description=description)
    return stripe_product['id']


def create_stripe_price(amount, product):
    print(amount)
    stripe_price = stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        # recurring={"interval": "month"},
        # product_data={"name": "Donation"}
        product=product,
    )
    return stripe_price['id']


def create_stripe_session(stripe_price_id):
    stripe_session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[
            {"price": stripe_price_id,
             "quantity": 1}
        ],
        mode="payment",
    )
    return stripe_session['url'], stripe_session['id'], stripe_session['payment_status']


def get_stripe_session_status(session_id):
    session = stripe.checkout.Session.retrieve(
        session_id,
    )
    return session['payment_status']
