import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from .forms import DonationForm
from paypal.standard.forms import PayPalPaymentsForm

# stripe.api_key = settings.STRIPE_SECRET_KEY

def home(request):
    return render(request, "index.html")
def payment_selection(request):
    return render(request, "home.html")

# Stripe donation view
def donate_stripe(request):
    if request.method == "POST":
        form = DonationForm(request.POST)
        if form.is_valid():
            amount = int(float(form.cleaned_data["amount"]) * 100)
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[{
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": "Donation"},
                        "unit_amount": amount,
                    },
                    "quantity": 1,
                }],
                mode="payment",
                success_url=request.build_absolute_uri("/success"),
                cancel_url=request.build_absolute_uri("/cancel"),
            )
            return redirect(session.url, code=303)
    else:
        form = DonationForm()

    return render(request, "donate_stripe.html", {"form": form})

# PayPal donation view
def donate_paypal(request):
    if request.method == "POST":
        form = DonationForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data["amount"]
            paypal_dict = {
                "business": settings.PAYPAL_RECEIVER_EMAIL,
                "amount": str(amount),
                "item_name": "Donation",
                "invoice": "INV-" + str(amount).replace(".", ""),
                "currency_code": "USD",
                "notify_url": request.build_absolute_uri("/paypal/"),
                "return_url": request.build_absolute_uri("/success"),
                "cancel_return": request.build_absolute_uri("/cancel"),
            }
            form_paypal = PayPalPaymentsForm(initial=paypal_dict, button_type="donate")
            return render(request, "process_paypal.html", {"form": form_paypal})
    else:
        form = DonationForm()

    return render(request, "donate_paypal.html", {"form": form})


def success(request):
    return render(request, "success.html")

def cancel(request):
    return render(request, "cancel.html")